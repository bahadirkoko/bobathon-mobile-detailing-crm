# Normalized Schema Refactor Plan

## Goal
Refactor the current CRM data model from the initial demo-oriented shape into a more normalized relational structure while keeping the existing demo auth flow unchanged. For the hackathon submission, implementation stopped after Stage 3 due to time constraints; Stages 4–6 were explicitly descoped.

## Hackathon final state
The final submitted schema state includes:
- normalized `Customer`
- normalized `Employee`
- normalized `Vehicle`
- new `Package` catalog
- `Appointment.package_id` replacing free-text `service_name`

The following planned work was intentionally not implemented for the submission:
- `AddOn`
- `appointment_add_ons`
- appointment date/time split
- appointment address split
- pricing snapshot refactor beyond current `price_cents`
- expanded appointment photo uploader fields

## Current -> Target table/class mapping

### `customers`
- **Current class:** [`Customer`](app/models/customer.py)
- **Current fields:** `id`, `full_name`, `phone`, `email`, `address`
- **Target class:** [`Customer`](app/models/customer.py)
- **Target fields:** `id`, `first_name`, `last_name`, `phone`, `email`, `default_street_address`, `default_city`, `default_state`, `default_zipcode`, `created_at`, `updated_at`
- **Reason:** split composite name/address fields into atomic attributes

### `employees`
- **Current class:** [`Employee`](app/models/employee.py)
- **Current fields:** `id`, `full_name`, `role`, `phone`, `email`
- **Target class:** [`Employee`](app/models/employee.py)
- **Target fields:** `id`, `first_name`, `last_name`, `role`, `phone`, `email`, `hire_date`, `is_active`, `created_at`
- **Reason:** split name and add employment lifecycle fields

### `vehicles`
- **Current class:** [`Vehicle`](app/models/vehicle.py)
- **Current fields:** `id`, `customer_id`, `make`, `model`, `year`, `color`, `vehicle_size`, `notes`
- **Target class:** [`Vehicle`](app/models/vehicle.py)
- **Target fields:** `id`, `customer_id`, `make`, `model`, `year`, `color`, `vehicle_type`, `created_at`
- **Reason:** align with target schema and remove mixed-purpose `notes`/`vehicle_size` shape

### `packages`
- **Current class:** none
- **Target class:** [`Package`](app/models/package.py)
- **Target fields:** `id`, `name`, `description`, `base_price_cents`, `duration_minutes`, `is_active`, `created_at`
- **Reason:** reusable package catalog should be separated from appointments

### `add_ons`
- **Current class:** none
- **Target class:** [`AddOn`](app/models/add_on.py)
- **Target fields:** `id`, `name`, `description`, `price_cents`, `duration_minutes`, `is_active`, `created_at`
- **Reason:** reusable add-on catalog should be normalized into its own table

### `appointments`
- **Current class:** [`Appointment`](app/models/appointment.py)
- **Current fields:** `id`, `customer_id`, `vehicle_id`, `employee_id`, `scheduled_at`, `service_address`, `status`, `price_cents`, `service_name`, `completed_at`, `created_at`, `updated_at`
- **Target class:** [`Appointment`](app/models/appointment.py)
- **Target fields:** `id`, `employee_id`, `customer_id`, `vehicle_id`, `package_id`, `status`, `appointment_date`, `appointment_time`, `service_street_address`, `service_city`, `service_state`, `service_zipcode`, `base_price_cents`, `discount_cents`, `final_amount_cents`, `started_at`, `completed_at`, `cancelled_at`, `cancellation_reason`, `created_at`, `updated_at`
- **Reason:** remove denormalized service/package fields and split address/scheduling into atomic fields

### `appointment_add_ons`
- **Current class:** none
- **Target class:** [`AppointmentAddOn`](app/models/appointment_add_on.py)
- **Target fields:** `id`, `appointment_id`, `add_on_id`, `price_cents`, `created_at`
- **Reason:** proper many-to-many join with pricing snapshot at time of booking

### `appointment_photos`
- **Current class:** [`AppointmentPhoto`](app/models/appointment.py)
- **Current fields:** `id`, `appointment_id`, `tag`, `file_path`, `created_at`
- **Target class:** [`AppointmentPhoto`](app/models/appointment.py)
- **Target fields:** `id`, `appointment_id`, `employee_id_uploaded`, `photo_tag`, `file_path`, `uploaded_at`
- **Reason:** store uploader employee and align photo tag naming with target schema

### Explicitly excluded tables
- `action_tokens`
- `blocked_dates`

## Exact files expected to change

### Models
- [`app/models/customer.py`](app/models/customer.py)
- [`app/models/employee.py`](app/models/employee.py)
- [`app/models/vehicle.py`](app/models/vehicle.py)
- [`app/models/appointment.py`](app/models/appointment.py)
- [`app/models/enums.py`](app/models/enums.py)
- [`app/models/__init__.py`](app/models/__init__.py)
- new: [`app/models/package.py`](app/models/package.py)
- new: [`app/models/add_on.py`](app/models/add_on.py)
- new: [`app/models/appointment_add_on.py`](app/models/appointment_add_on.py)

### Schemas
- [`app/schemas/customer.py`](app/schemas/customer.py)
- [`app/schemas/employee.py`](app/schemas/employee.py)
- [`app/schemas/vehicle.py`](app/schemas/vehicle.py)
- [`app/schemas/appointment.py`](app/schemas/appointment.py)
- [`app/schemas/__init__.py`](app/schemas/__init__.py)
- new: [`app/schemas/package.py`](app/schemas/package.py)
- new: [`app/schemas/add_on.py`](app/schemas/add_on.py)

### Services
- [`app/services/customers.py`](app/services/customers.py)
- [`app/services/employees.py`](app/services/employees.py)
- [`app/services/vehicles.py`](app/services/vehicles.py)
- [`app/services/appointments.py`](app/services/appointments.py)
- [`app/services/storage.py`](app/services/storage.py)
- [`app/services/__init__.py`](app/services/__init__.py)
- new: [`app/services/packages.py`](app/services/packages.py)
- new: [`app/services/add_ons.py`](app/services/add_ons.py)

### Routes
- [`app/api/dependencies.py`](app/api/dependencies.py)
- [`app/api/routes/customers.py`](app/api/routes/customers.py)
- [`app/api/routes/employees.py`](app/api/routes/employees.py)
- [`app/api/routes/vehicles.py`](app/api/routes/vehicles.py)
- [`app/api/routes/appointments.py`](app/api/routes/appointments.py)
- [`app/api/routes/dashboard.py`](app/api/routes/dashboard.py)
- [`app/api/routes/admin.py`](app/api/routes/admin.py)
- [`app/api/routes/public.py`](app/api/routes/public.py)

### Templates
- [`app/templates/booking/index.html`](app/templates/booking/index.html)
- [`app/templates/booking/_confirmation.html`](app/templates/booking/_confirmation.html)
- [`app/templates/dashboard/index.html`](app/templates/dashboard/index.html)
- [`app/templates/dashboard/customers.html`](app/templates/dashboard/customers.html)
- [`app/templates/dashboard/appointments.html`](app/templates/dashboard/appointments.html)
- [`app/templates/dashboard/vehicles.html`](app/templates/dashboard/vehicles.html)
- [`app/templates/dashboard/employees.html`](app/templates/dashboard/employees.html)
- [`app/templates/dashboard/partials/customer_list.html`](app/templates/dashboard/partials/customer_list.html)
- [`app/templates/dashboard/partials/appointment_list.html`](app/templates/dashboard/partials/appointment_list.html)
- [`app/templates/reports/appointment_report.html`](app/templates/reports/appointment_report.html)

### Tests
- [`tests/conftest.py`](tests/conftest.py)
- [`tests/services/test_customers.py`](tests/services/test_customers.py)
- [`tests/services/test_employees.py`](tests/services/test_employees.py)
- [`tests/services/test_vehicles.py`](tests/services/test_vehicles.py)
- [`tests/services/test_appointments.py`](tests/services/test_appointments.py)
- [`tests/routes/test_pages.py`](tests/routes/test_pages.py)
- possibly [`tests/routes/test_route_imports.py`](tests/routes/test_route_imports.py)
- possibly [`tests/mcp/test_server.py`](tests/mcp/test_server.py)
- new tests for packages/add-ons if needed

## Database reset at start
Because the app uses [`Base.metadata.create_all()`](app/main.py) instead of migrations, start the implementation by resetting the local database state. The safe path for the current repo is:
1. stop containers with `docker compose down -v`
2. delete local `__pycache__` artifacts if needed
3. let the app recreate tables from metadata on next startup/test run

No attempt should be made to preserve existing demo data.

## Execution order

### Stage 1: Normalize Customer and Employee
**Scope**
- split `full_name` into `first_name` + `last_name`
- split customer `address` into `default_street_address`, `default_city`, `default_state`, `default_zipcode`
- add employee `hire_date` and `is_active`

**Files changing first**
- models: `customer.py`, `employee.py`
- schemas: `customer.py`, `employee.py`
- services: `customers.py`, `employees.py`
- routes/templates/tests that read those fields

**Validation after stage**
- `python -m compileall app tests`
- `pytest`
- grep for leftover references: `full_name`, single customer `address`

### Stage 2: Normalize Vehicle
**Scope**
- replace `vehicle_size` with `vehicle_type`
- remove vehicle `notes`
- add `created_at`

**Files changing**
- models: `vehicle.py`
- schemas: `vehicle.py`
- services: `vehicles.py`
- routes/templates/tests using vehicle fields

**Validation after stage**
- compileall
- pytest
- grep for leftover references: `vehicle_size`, `notes`

### Stage 3: Add Package and wire `package_id` into Appointment
**Scope**
- create `Package` model/schema/service
- add `package_id` relationship to appointments
- begin replacing `service_name` with package linkage in routes/services/UI

**Files changing**
- new package model/schema/service
- appointment model/schema/service/routes/templates/tests
- dependencies and MCP server exports if package tools are introduced now

**Checkpoint after stage**
- compileall
- pytest
- grep for leftover references: `service_name`
- stop and report status before continuing

### Stage 4: Add AddOn and `appointment_add_ons` — descoped
Descoped for the hackathon submission due to time constraints. No Stage 4 implementation was started or kept.

### Stage 5: Normalize Appointment — descoped
Descoped for the hackathon submission due to time constraints. Appointment still uses the current interim fields such as `scheduled_at`, `service_address`, and `price_cents`.

### Stage 6: Expand AppointmentPhoto — descoped
Descoped for the hackathon submission due to time constraints. Appointment photos remain in the current interim shape.

## Implementation constraints to preserve
- Keep auth and browser demo login unchanged for this refactor
- Continue using the service layer as the shared business-logic boundary
- Keep MCP tools calling services rather than duplicating logic
- Keep local file photo storage under `app/static/uploads/`
- Keep PostgreSQL as the intended runtime DB, even if some tests use isolated SQLite fixtures

## Definition of done for the refactor
- Stages 1–3 completed with requested checkpoints
- Stages 4–6 explicitly descoped and documented
- Stage 3 state accepted as the final hackathon submission baseline
- `PROMPTS.md` updated at each major decision/checkpoint
