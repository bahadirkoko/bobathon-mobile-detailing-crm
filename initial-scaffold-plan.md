# Initial Scaffold Plan

## Overview
Create the initial repository scaffold for a mobile detailing CRM using a service-layer-first architecture. The scaffold should establish a single Python application package at `app/`, shared domain services reused by FastAPI routes and MCP tools, server-rendered Jinja2 templates enhanced with HTMX, PostgreSQL persistence via SQLAlchemy 2.x with schema creation through `Base.metadata.create_all()` on startup, and a test/CI foundation that supports the core entities before any supporting features.

## Sub-task 1
**Intent**
Define the repository skeleton and configuration surface so implementation starts from a stable structure that supports local development, testing, templates, MCP integration, and CI without later reorganization.

**Expected Outcomes**
- Root-level config files exist for Python dependencies, formatting/linting, environment setup, Docker Compose, and GitHub Actions.
- The `app/` package layout clearly separates API routes, services, models, schemas, templates, MCP tools, and shared infrastructure.
- The `tests/` layout mirrors the service-first architecture.

**Todo List**
1. Create root files for dependency management, test configuration, lint/format configuration, Docker Compose, environment example, and CI workflow definitions.
2. Create the `app/` package with subpackages for `api/routes`, `core`, `db`, `models`, `schemas`, `services`, `mcp`, `templates`, and `static/uploads`.
3. Create template folders for public booking, shared dashboard views, and appointment reports, with role-specific rendering handled by template context rather than separate admin/employee template trees.
4. Create `tests/` folders for services, routes, and MCP smoke tests, with service tests prioritized first.
5. Add placeholder module entry points for the FastAPI app, MCP server, SQLAlchemy metadata, and startup schema initialization.

**Relevant Context**
- [`AGENTS.md`](AGENTS.md)

**Status**
[x] done

## Sub-task 2
**Intent**
Establish the domain model and persistence foundation for the core entities only, matching the required build order and avoiding scope creep into package, add-on, or blocked-date features.

**Expected Outcomes**
- SQLAlchemy 2.x models exist for Customer, Employee, Vehicle, and Appointment.
- Relationships and shared database infrastructure support CRUD and assignment workflows.
- Startup-driven schema initialization can create the initial core tables without Alembic.

**Todo List**
1. Define shared SQLAlchemy base, session management, and database settings in `app/db` and `app/core`.
2. Implement core models for Customer, Employee, Vehicle, and Appointment in `app/models`.
3. Add supporting enums or constants needed for appointment status and employee role flags.
4. Define initial Pydantic schemas for create, update, read, and list use cases for each core entity.
5. Add startup schema initialization using `Base.metadata.create_all()` targeting only the core tables.
6. Add the appointment photo path field and report-page-ready completion data needed for the completed appointment workflow.
7. Defer Package, AddOn, and BlockedDate models until the core loop works end to end.

**Relevant Context**
- [`AGENTS.md`](AGENTS.md:14)
- [`AGENTS.md`](AGENTS.md:27)

**Status**
[x] done

## Sub-task 3
**Intent**
Build the service layer first so all business rules, validation, and CRUD behavior are defined in one place and can be reused by HTTP and MCP entry points.

**Expected Outcomes**
- Each core entity has a dedicated service module encapsulating CRUD and domain validation.
- Services expose stable functions or classes that do not depend on FastAPI request objects or MCP tool interfaces.
- Error paths are explicit and testable.

**Todo List**
1. Create service modules for customers, employees, vehicles, and appointments under `app/services`.
2. Add explicit validation rules for core relationships, such as vehicle ownership and single-employee appointment assignment, without scheduling-conflict checks.
3. Add a simple file-storage service interface for appointment completion photos that saves under `static/uploads/` and returns stored paths.
4. Define application-level exceptions and error mapping utilities in `app/core` or `app/services`.
5. Ensure service signatures are fully typed and documented, with repository/session dependencies passed explicitly.
6. Keep service APIs suitable for direct reuse from routes, MCP handlers, and future background jobs.

**Relevant Context**
- [`AGENTS.md`](AGENTS.md:7)
- [`AGENTS.md`](AGENTS.md:38)
- [`AGENTS.md`](AGENTS.md:40)

**Status**
[ ] pending

## Sub-task 4
**Intent**
Expose the service layer through web routes first and then MCP tools, preserving a single source of business logic and enabling both UI and natural-language control.

**Expected Outcomes**
- FastAPI routes provide CRUD screens and form handlers for the core entities.
- MCP tools mirror the core operations using snake_case names such as `create_customer`, `list_appointments`, and `update_appointment_status`.
- No business logic is duplicated between routes and MCP tool definitions.

**Todo List**
1. Add FastAPI routers for public booking, internal dashboard CRUD flows, and appointment completion/report flows over the core entities.
2. Wire shared dependency helpers for database sessions and minimal role-based session checks backed by hardcoded demo users.
3. Add MCP server bootstrap and tool definitions under `app/mcp`, with each tool delegating directly to the corresponding service.
4. Standardize MCP tool naming around snake_case action names such as `create_appointment` and `list_customers`.
5. Add response shaping helpers only where route or MCP transport requirements differ from service return values.

**Relevant Context**
- [`AGENTS.md`](AGENTS.md:7)
- [`AGENTS.md`](AGENTS.md:8)
- [`AGENTS.md`](AGENTS.md:31)
- [`AGENTS.md`](AGENTS.md:34)

**Status**
[ ] pending

## Sub-task 5
**Intent**
Add the server-rendered UI layer for the public booking flow and shared internal dashboard, using HTMX for progressive interactivity without introducing a SPA.

**Expected Outcomes**
- Public booking pages exist for creating appointments against the core data model.
- Shared dashboard templates support both admin and employee views through context-driven rendering.
- Completed appointments expose a server-rendered report page with before and after photos and a shareable link shown in the admin dashboard.
- HTMX partials support common CRUD interactions without duplicating full-page templates.

**Todo List**
1. Create base templates, layout partials, and shared dashboard components in `app/templates`.
2. Implement public booking pages for customer and appointment creation around the simplified core flow.
3. Implement internal list/detail/form templates for customer create/search/edit, appointment create/search/edit, and list views for vehicles and employees.
4. Implement the completed appointment report page and admin dashboard share-link display for completed appointments.
5. Add HTMX partial endpoints and fragments for create/update flows, inline status changes, and filtered lists where useful.
6. Keep role-specific differences in conditional blocks and view models instead of separate template trees.

**Relevant Context**
- [`AGENTS.md`](AGENTS.md:11)
- [`AGENTS.md`](AGENTS.md:27)
- [`AGENTS.md`](AGENTS.md:34)
- [`AGENTS.md`](AGENTS.md:35)

**Status**
[ ] pending

## Sub-task 6
**Intent**
Add validation, automated tests, and CI last in the scaffold sequence so every earlier layer is covered before supporting features are introduced.

**Expected Outcomes**
- Unit tests cover all service-layer logic for the core entities and appointment photo handling.
- Route and MCP tests provide a small set of happy-path smoke coverage.
- GitHub Actions runs the test suite with PostgreSQL and coverage reporting without threshold gating.

**Todo List**
1. Write service-layer unit tests first for customers, employees, vehicles, appointments, and appointment photo persistence, including relationship and validation failures.
2. Add a handful of route smoke tests for public booking, dashboard CRUD behavior, and completed appointment report rendering.
3. Add a handful of MCP smoke tests that verify each tool calls the shared service layer correctly.
4. Configure pytest, coverage reporting, and test fixtures for isolated database setup.
5. Add a GitHub Actions workflow that installs dependencies, starts PostgreSQL as a service container, initializes the schema, and executes tests with coverage reporting.
6. Keep supporting entities out of scope until these tests pass for the core loop.

**Relevant Context**
- [`AGENTS.md`](AGENTS.md:41)
- [`AGENTS.md`](AGENTS.md:42)
- [`AGENTS.md`](AGENTS.md:43)

**Status**
[ ] pending

## Open Decisions Confirmed
- Use `app/` as the main application package.
- Use SQLAlchemy 2.x declarative models.
- Use `Base.metadata.create_all()` on startup instead of Alembic.
- Use shared admin/employee templates with role-based rendering via template context.
- Use snake_case MCP tool names such as `create_appointment` and `list_customers`.
- Store appointment price as integer cents.
- Use one employee per appointment initially.
- Skip scheduling-conflict validation.
- Use hardcoded demo auth users.
- Store appointment completion photos as local files under `static/uploads/` behind a service-layer interface.

## Open Decisions Requiring User Input Before Implementation
- Exact field definitions for the core entities, especially address structure and phone/email constraints.
- Whether the report page should distinguish before and after photo slots explicitly or support a simple gallery with labeled uploads.
- Whether employee live status should be limited to appointment status updates in this build or include additional activity notes.