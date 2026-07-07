# ARCHITECTURE.md

This document describes the current code layout of the mobile detailing CRM based on the actual repository state.

## High-level structure

### `app/`
Main application package. Uses FastAPI for HTTP routes, SQLAlchemy ORM for persistence, Jinja2 for server-rendered HTML, HTMX in templates for partial updates, and the MCP Python SDK for tool exposure.

- **Contains:** all runtime code
- **Uses:** FastAPI, SQLAlchemy, Jinja2, itsdangerous, MCP SDK
- **Responsible for:** web app, service layer, ORM models, templates, auth, MCP tools
- **Connects to:** `tests/` imports and exercises this package

### `tests/`
Automated tests and fixtures.

- **Contains:** unit tests and smoke tests
- **Uses:** pytest, SQLAlchemy in-memory SQLite, FastAPI TestClient in route smoke tests
- **Responsible for:** validating service logic, basic route behavior, MCP bootstrap
- **Connects to:** imports modules from `app/`

## `app/` folders and files

### `app/main.py`
Creates the FastAPI app, mounts static files, registers the composed router, translates service exceptions into HTTP responses, initializes the MCP server, and creates tables on startup with `Base.metadata.create_all()`.
- **Uses:** FastAPI, Starlette `StaticFiles`, SQLAlchemy metadata
- **Connects to:** `app/api/routes/__init__.py`, `app/db/base.py`, `app/db/session.py`, `app/mcp/server.py`, `app/services/exceptions.py`

### `app/web.py`
Creates the shared `Jinja2Templates` instance used by HTML-rendering routes.
- **Uses:** FastAPI templating / Jinja2
- **Connects to:** all route files that call `templates.TemplateResponse(...)`

### `app/api/`
HTTP-layer code.
- **Contains:** route dependency helpers and all route modules
- **Uses:** FastAPI dependency injection and request handling
- **Responsible for:** translating HTTP requests into service calls
- **Connects to:** `app/services/`, `app/core/auth.py`, `app/web.py`

#### `app/api/dependencies.py`
Small factory functions that return service instances.
- **Uses:** plain Python + FastAPI dependency pattern
- **Responsible for:** keeping route constructors thin and consistent
- **Connects to:** route modules call these to obtain services

#### `app/api/routes/__init__.py`
Composes all route submodules into one `APIRouter`.
- **Uses:** FastAPI `APIRouter`
- **Responsible for:** central route registration order
- **Connects to:** imported by `app/main.py`

#### `app/api/routes/public.py`
Public, unauthenticated booking UI routes. Renders `/` and handles the booking form submission.
- **Uses:** FastAPI, Jinja2 templates, form handling
- **Responsible for:** creating customer + vehicle + appointment in one public flow
- **Connects to:** `CustomerService`, `VehicleService`, `AppointmentService`, `app/templates/booking/*`

#### `app/api/routes/system.py`
Utility and auth-related routes such as `/health`, `/login`, `/logout`, and `/me`.
- **Uses:** FastAPI, Jinja2 templates, signed cookies via auth helpers
- **Responsible for:** browser login flow and health/user introspection
- **Connects to:** `app/core/auth.py`, `app/templates/login.html`

#### `app/api/routes/dashboard.py`
HTML dashboard landing page route for `/dashboard`.
- **Uses:** FastAPI, Jinja2 templates
- **Responsible for:** rendering the shared dashboard home view with summary data
- **Connects to:** all core services and `app/templates/dashboard/index.html`

#### `app/api/routes/admin.py`
Authenticated HTML CRUD pages and HTMX partial endpoints under `/dashboard/...`.
- **Uses:** FastAPI, Jinja2 templates, HTMX-compatible partial responses, file upload handling
- **Responsible for:** customer create/edit pages, appointment create/status updates, vehicle/employee lists, report rendering, photo uploads
- **Connects to:** core services, `app/core/auth.py`, dashboard/report templates

#### `app/api/routes/customers.py`, `employees.py`, `vehicles.py`, `appointments.py`
JSON-style CRUD endpoints for the core entities.
- **Uses:** FastAPI + Pydantic response models
- **Responsible for:** programmatic HTTP CRUD operations separate from the server-rendered UI
- **Connects to:** corresponding service classes and schema modules

### `app/core/`
Shared non-domain infrastructure.

#### `app/core/config.py`
Pydantic settings loader for env-based configuration.
- **Uses:** `pydantic-settings`
- **Responsible for:** app name, database URL, secret key, demo user emails
- **Connects to:** DB setup, auth signing, app startup

#### `app/core/auth.py`
Demo authentication model. Resolves current users from a signed cookie first, then `X-Demo-User` header.
- **Uses:** FastAPI dependency injection, `itsdangerous`
- **Responsible for:** demo-user lookup, session-cookie signing, role enforcement
- **Connects to:** UI routes, JSON routes, `/login` route in `system.py`

### `app/db/`
Database primitives.

#### `app/db/base.py`
Declares the SQLAlchemy `DeclarativeBase`.
- **Uses:** SQLAlchemy ORM
- **Responsible for:** common model base class
- **Connects to:** every ORM model module

#### `app/db/session.py`
Creates the SQLAlchemy engine and request-scoped session generator.
- **Uses:** SQLAlchemy engine/sessionmaker
- **Responsible for:** DB connections and FastAPI session dependency
- **Connects to:** route modules, MCP server, startup table creation

#### `app/db/__init__.py`
Convenience exports for DB primitives.

### `app/models/`
SQLAlchemy ORM layer.

#### `app/models/enums.py`
Enum definitions for employee role, appointment status, and appointment photo tag.
- **Uses:** Python `StrEnum`
- **Connects to:** ORM models, schemas, services, routes

#### `app/models/customer.py`
Customer table and relationships to vehicles and appointments.
- **Uses:** SQLAlchemy ORM
- **Connects to:** `Vehicle`, `Appointment`, customer service, customer schemas

#### `app/models/employee.py`
Employee table and relationship to appointments.
- **Uses:** SQLAlchemy ORM
- **Connects to:** `Appointment`, employee service, employee schemas

#### `app/models/vehicle.py`
Vehicle table linked to a customer and related appointments.
- **Uses:** SQLAlchemy ORM
- **Connects to:** `Customer`, `Appointment`, vehicle service, vehicle schemas

#### `app/models/appointment.py`
Appointment table plus `AppointmentPhoto` table.
- **Uses:** SQLAlchemy ORM
- **Responsible for:** scheduling, assignment, completion metadata, local photo metadata
- **Connects to:** `Customer`, `Employee`, `Vehicle`, appointment service, appointment/report templates

#### `app/models/__init__.py`
Exports all ORM models so importing `app.models` registers metadata before `create_all()` runs.

### `app/schemas/`
Pydantic models for validation and serialization.

#### `app/schemas/base.py`
Shared `ORMBaseModel` with `from_attributes=True`.
- **Uses:** Pydantic
- **Responsible for:** easy SQLAlchemy-to-schema conversion
- **Connects to:** all schema modules

#### `app/schemas/customer.py`, `employee.py`, `vehicle.py`, `appointment.py`
Create/update/read schema classes for each core entity.
- **Uses:** Pydantic
- **Responsible for:** input validation and response serialization at route and MCP boundaries
- **Connects to:** route modules, MCP server, service payload creation

#### `app/schemas/__init__.py`
Convenience exports for schema classes.

### `app/services/`
Business-logic layer. This is the core architectural boundary shared by HTTP routes and MCP tools.

#### `app/services/exceptions.py`
Defines `ServiceError`, `NotFoundError`, and `ValidationError`.
- **Uses:** plain Python exceptions
- **Responsible for:** explicit, reusable service error signaling
- **Connects to:** `app/main.py` exception handlers, all services

#### `app/services/customers.py`
CRUD logic for customers.
- **Uses:** SQLAlchemy Session + ORM models
- **Connects to:** customer routes, MCP customer tools

#### `app/services/employees.py`
CRUD logic for employees.
- **Uses:** SQLAlchemy Session + ORM models
- **Connects to:** employee routes, MCP employee tools

#### `app/services/vehicles.py`
CRUD logic for vehicles, including customer-existence validation.
- **Uses:** SQLAlchemy Session + `CustomerService`
- **Connects to:** vehicle routes, MCP vehicle tools, appointment validation indirectly

#### `app/services/storage.py`
Local file-storage adapter for appointment photos.
- **Uses:** Python `pathlib`, filesystem writes
- **Responsible for:** writing uploaded image bytes to `app/static/uploads/` and returning `AppointmentPhoto` objects
- **Connects to:** `AppointmentService`, report/photo-upload flows

#### `app/services/appointments.py`
Main appointment business logic.
- **Uses:** SQLAlchemy Session, eager loading, dependent services, storage service
- **Responsible for:** appointment CRUD, relationship validation, completion timestamps, photo saving
- **Connects to:** appointment JSON routes, dashboard UI routes, report page, MCP appointment tools

#### `app/services/__init__.py`
Exports service classes and common exceptions.

### `app/mcp/`
MCP integration layer.

#### `app/mcp/server.py`
Creates the `FastMCP` server and registers snake_case tools like `create_customer`, `list_appointments`, and `update_appointment_status`.
- **Uses:** MCP Python SDK, SQLAlchemy sessions, Pydantic schemas
- **Responsible for:** exposing the same business operations to MCP clients
- **Connects to:** service layer only; it does not duplicate business logic

### `app/static/`
Static file tree served by FastAPI.

#### `app/static/uploads/.gitkeep`
Placeholder so the upload directory exists in Git.
- **Responsible for:** ensuring photo uploads have a checked-in folder target

### `app/templates/`
Server-rendered Jinja2 templates.

#### `app/templates/base.html`
Shared layout, nav, styling, and HTMX script include.
- **Uses:** Jinja2, HTMX
- **Connects to:** inherited by all page templates

#### `app/templates/login.html`
Demo login page for browser access.
- **Connects to:** `/login` route in `system.py`

#### `app/templates/booking/`
Public booking UI.
- `index.html`: main booking form
- `_confirmation.html`: HTMX confirmation fragment returned after booking

#### `app/templates/dashboard/`
Authenticated dashboard pages.
- `index.html`: dashboard landing page with quick stats and recent appointments
- `customers.html`: customer admin page
- `appointments.html`: appointment admin page
- `vehicles.html`: vehicle list page
- `employees.html`: employee list page
- `partials/customer_list.html`: HTMX refresh target for customer list/editing
- `partials/appointment_list.html`: HTMX refresh target for appointment list/status updates

#### `app/templates/reports/appointment_report.html`
Completed-appointment report page with shareable link and labeled photo gallery/upload form.

#### Empty folders currently present
- `app/templates/appointments/`
- `app/templates/public/`
These currently do not contain active templates.

## `tests/` folders and files

### `tests/conftest.py`
Shared pytest fixtures.
- **Uses:** pytest, in-memory SQLite, temporary filesystem paths
- **Responsible for:** isolated DB session fixture, upload directory fixture, and prebuilt service fixtures
- **Connects to:** all service tests

### `tests/services/`
Core unit tests for the service layer.
- `test_customers.py`: customer create/update/not-found behavior
- `test_employees.py`: employee create/update/not-found behavior
- `test_vehicles.py`: vehicle create/update plus customer validation
- `test_appointments.py`: appointment create/update/status/photo flow and relationship validation

### `tests/routes/`
Lightweight route smoke coverage.
- `test_route_imports.py`: verifies route modules import cleanly
- `test_pages.py`: simple `/health` and `/login` smoke checks through `TestClient`

### `tests/mcp/`
Lightweight MCP smoke coverage.
- `test_server.py`: verifies MCP server bootstrap returns a server instance

## Typical browser page request flow

For a normal dashboard page load, the browser requests `/dashboard`, which is handled by `app/main.py` through the composed router in `app/api/routes/__init__.py`. The specific route function lives in `app/api/routes/dashboard.py`, which first resolves the current user via `app/core/auth.py`, then gets a database session from `app/db/session.py`, then asks the service layer (`CustomerService`, `VehicleService`, `EmployeeService`, `AppointmentService`) for the data it needs. Those services query SQLAlchemy ORM models from `app/models/` using the schemas and eager-loading patterns already defined. Finally, `dashboard.py` renders `app/templates/dashboard/index.html` through the shared Jinja2 `templates` object in `app/web.py`, and FastAPI returns the HTML response.

## MCP tool call flow

For an MCP call such as `create_appointment`, the MCP client talks to the server built in `app/mcp/server.py`. That module opens a SQLAlchemy session using `SessionLocal` from `app/db/session.py`, validates the input payload with the relevant Pydantic schema from `app/schemas/appointment.py`, and then calls directly into `AppointmentService` in `app/services/appointments.py`. The service performs all relationship validation and persistence using ORM models from `app/models/`. Once the service returns, `server.py` converts the ORM result back into a Pydantic read model and dumps it to plain JSON-compatible data for the MCP response. The key architectural rule is that MCP tools reuse the same service layer as web routes.

## Where do I make common changes?

### Add a new field to `Appointment`
1. Update the ORM model in `app/models/appointment.py`
2. Update create/update/read schemas in `app/schemas/appointment.py`
3. Update any business rules in `app/services/appointments.py`
4. Update JSON routes in `app/api/routes/appointments.py` if input/output handling changes
5. Update dashboard/report/public templates in `app/templates/` if the field should be shown or edited
6. Add or update tests in `tests/services/test_appointments.py` and any smoke tests that touch it

### Add a new browser page
1. Add the route in the relevant file under `app/api/routes/`
2. Create the Jinja2 template under `app/templates/`
3. If it needs business logic, add or extend a service in `app/services/`
4. If it needs validated form/response structures, update `app/schemas/`

### Add a new MCP tool
1. Add or extend business logic in `app/services/`
2. Add/extend any needed schemas in `app/schemas/`
3. Register the new tool in `app/mcp/server.py`
4. Add a smoke test in `tests/mcp/test_server.py` or a new MCP test file

### Change demo authentication behavior
1. Edit session/header logic in `app/core/auth.py`
2. Adjust login/logout routes in `app/api/routes/system.py`
3. Update the login UI in `app/templates/login.html` if needed
