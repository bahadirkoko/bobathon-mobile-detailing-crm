# PROMPTS.md

This file records user prompts and concise summaries of Bob's responses for the bobathon showcase.

## Planning
- **Prompt:** based on @AGENTS.md, create a detailed implementation plan for the initial repo scaffold. I want:1. A complete file/folder structure backend, templates, tests, config files reflecting the service-layer-first architecture described in AGENTS.md2.The build order: core entities first Customer, Employee, Vehicle, Appointment with full CRUD, before touching Package/AddOn/BlockedDate3. A rough sequence: what gets built first, second, third e.g. models → service layer → routes → MCP tools → templates → tests → CI4. Call out any open decisions you need my input on before implementing
  **Summary:** Produced a detailed scaffold plan in [`initial-scaffold-plan.md`](initial-scaffold-plan.md) covering repository structure, phased build order, and the sequence from models through CI. It also surfaced the remaining decisions needed before implementation.
- **Prompt:** Use a standard app package named `app/`, SQLAlchemy 2.x declarative models, Alembic migrations, server-rendered Jinja2 pages with shared admin/employee templates, and MCP tool names like `customers.list`, `appointments.create`, etc.
  **Summary:** Locked the initial planning defaults so the scaffold plan could be written against a concrete package layout, ORM approach, template strategy, and MCP naming convention.
- **Prompt:** CRM for mobile detailers with public booking, internal operations, auth, employee job updates, and admin visibility into field work; what stack should we use?
  **Summary:** Confirmed the product is buildable and recommended a Python-first stack using FastAPI, SQLAlchemy, PostgreSQL, Jinja2, and HTMX. Advised keeping the first version server-rendered and avoiding SPA complexity.

## Architecture
- **Prompt:** based on the requirements can you create an agents.md for the scope of this project with this required stuff
  **Summary:** Created a scope-level [`AGENTS.md`](AGENTS.md) capturing the required stack, service-layer architecture, MCP reuse rules, testing expectations, and CI direction.

## Scaffolding
- **Prompt:** I updated the agents.md making sure it will work as we wanted, also create a prompts.md for this bobatchon competition save my each prompt there and sumamry of you reply at the end of each step so we can showcase how we utilzied bob
  **Summary:** Read the updated [`AGENTS.md`](AGENTS.md), then created [`PROMPTS.md`](PROMPTS.md) to log prompts and concise outcome summaries for the showcase.

## Implementation
- **Prompt:** Approved with these changes: drop Alembic and use `Base.metadata.create_all()` on startup, switch MCP tool names to snake_case, keep route and MCP tests as smoke tests, store completion photos locally in `static/uploads/`, add a server-rendered report page, confirm admin CRUD scope, keep Docker Compose Postgres locally and in CI, and proceed in Agent mode.
  **Summary:** Updated the approved plan to remove Alembic, adopt snake_case MCP tools, refine the testing scope, add local file photo handling plus report pages, and document the local-storage/local-Postgres demo posture in [`AGENTS.md`](AGENTS.md).
- **Prompt:** Proceed with implementation in Agent mode, sub-task 1 first. Log each meaningful prompt and decision to [`PROMPTS.md`](PROMPTS.md) as you go, with a brief check-in after each sub-task.
  **Summary:** Completed sub-task 1 by scaffolding the initial repository structure: Python project config, Docker Compose Postgres setup, CI workflow, FastAPI app entry point, database/session modules, MCP bootstrap, template directories, and placeholder test packages.

- **Prompt:** There's no .gitignore file in the project root. Create one now with standard Python exclusions plus project-specific ones, keep `app/static/uploads/.gitkeep` tracked, and untrack anything already excluded.
  **Summary:** Added the root [`.gitignore`](.gitignore) with the requested Python and project-specific ignore rules, including the negation for [`app/static/uploads/.gitkeep`](app/static/uploads/.gitkeep). Checked Git tracking after the earlier compile step and there were no excluded files currently tracked.

- **Prompt:** everything seems working good, now lets good start with sub task2, and Log this to PROMPTS.md per the AGENTS.md rule, and mark Sub-task 2 done in initial-scaffold-plan.md when complete.
  **Summary:** Started sub-task 2 to add the core database models, schemas, and startup-driven table creation for the first four entities.

- **Prompt:** Start sub-task 2 and mark it done in [`initial-scaffold-plan.md`](initial-scaffold-plan.md) when complete.
  **Summary:** Completed sub-task 2 by adding the core SQLAlchemy models and enums for customers, employees, vehicles, appointments, and appointment photos, plus the first set of typed Pydantic schemas and startup-compatible metadata registration.

- **Prompt:** everything looks great, lets go build sub task 3 , log this to @PROMPTS.md as well
  **Summary:** Started sub-task 3 to implement the shared service layer, validation rules, and local photo storage interface behind reusable business logic.

- **Prompt:** Build sub-task 3 and log it to [`PROMPTS.md`](PROMPTS.md) as well.
  **Summary:** Completed sub-task 3 by adding reusable CRUD services for customers, employees, vehicles, and appointments, plus service-layer exceptions and a local appointment photo storage service that writes to [`app/static/uploads/`](app/static/uploads/).

- **Prompt:** everything good lets go and build sub task 4 and keep logging to @PROMPTS.md file as well,
  **Summary:** Started sub-task 4 to connect the service layer to FastAPI routes, demo auth/session helpers, and MCP tool definitions.

- **Prompt:** Build sub-task 4 and keep logging to [`PROMPTS.md`](PROMPTS.md) as well.
  **Summary:** Completed sub-task 4 by wiring JSON CRUD routes, demo user auth helpers, service-error-to-HTTP translation, and snake_case MCP tools that call the same service layer without duplicating business logic.

- **Prompt:** everything seems great, lets build task 5 , and keeping logging to @PROMPTS.md
  **Summary:** Started sub-task 5 to add the server-rendered booking flow, shared dashboard views, report page, and HTMX-based form/list interactions.

- **Prompt:** Build task 5 and keep logging to [`PROMPTS.md`](PROMPTS.md).
  **Summary:** Completed sub-task 5 by adding public booking pages, dashboard/customer/appointment/vehicle/employee views, HTMX partial updates, and a server-rendered appointment report page with labeled photo uploads and shareable report links.

- **Prompt:** Visiting /dashboard in a browser fails with "Missing demo user" since browsers can't send custom X-Demo-User headers on normal navigation. Add a simple login form that sets a signed session cookie via `itsdangerous`, update `get_current_user` to check the cookie first before falling back to `X-Demo-User`, and redirect to `/dashboard` after login.
  **Summary:** Started a browser-friendly demo auth fix by adding a signed session-cookie login flow while preserving the header-based auth path for MCP and tests.

- **Prompt:** Add a simple `/login` route and template that sets a signed session cookie for demo browser access, and update auth to prefer the cookie before the `X-Demo-User` header fallback.
  **Summary:** Completed the browser demo-auth fix by adding a login page, signed `itsdangerous` session cookie handling, logout support, and cookie-first user resolution while preserving header-based auth for MCP and tests.

- **Prompt:** The TemplateResponse argument-order bug is still happening. Grep every `TemplateResponse(` call in `app/`, show every match, fix all of them systematically, compile, and smoke-test `/` and `/login` so no call site is missed.
  **Summary:** Started a full audit of every `TemplateResponse` usage to normalize the argument order against the installed Starlette version, then validate with compile and HTTP smoke tests.

- **Prompt:** Grep every `TemplateResponse(` call site, fix every argument-order bug, compile, and smoke-test `/` and `/login` so no TemplateResponse call site is missed.
  **Summary:** Audited and fixed every `TemplateResponse` call under [`app/`](app), then re-ran grep to confirm the updated call sites. Compile passed, but runtime HTTP smoke tests were blocked in this environment because project dependencies are not installed yet (`fastapi` and `uvicorn` are missing), so the server could not be started here.

- **Prompt:** everything looks good, we might have small bugs and needed improvements later on but for now lets focus on sub task 6, and finalzie it then we can focus on small bugs and fix them
  **Summary:** Started sub-task 6 to add the initial automated test suite and finalize the CI-oriented testing setup before returning to bug fixes.

- **Prompt:** Focus on sub-task 6 and finalize it before returning to smaller bug fixes and improvements.
  **Summary:** Completed sub-task 6 by adding service-layer unit tests for the core entities and photo storage flow, plus lightweight route and MCP smoke tests, while keeping CI aligned with pytest and coverage reporting.

- **Prompt:** Normalize the data model fully, but keep auth out of scope for this refactor. First produce a concrete refactor plan file mapping current classes/tables to target ones, exact files changing, and execution order. After approval, implement in six stages with checkpoints, compileall + pytest + grep after each stage, and reset the local database at the start because there are no migrations.
  **Summary:** Locked the staged normalization strategy and checkpoint workflow. The next step is to create and review a repo-specific refactor plan before any code changes are made.

- **Prompt:** Approve the normalized schema refactor plan and begin Stage 1 only, with a checkpoint before Stage 2.
  **Summary:** Started Stage 1 of the staged normalization refactor: local DB reset plus Customer and Employee normalization, with validation and grep checks required before proceeding.

- **Prompt:** Complete Stage 1 only, then stop and report compileall, pytest, and grep results before moving to Stage 2.
  **Summary:** Stage 1 code changes are in place: Customer and Employee were normalized across models, schemas, service inputs, routes, templates, and service tests. `python3 -m compileall app tests` passed; `pytest` could not run in this environment because the `pytest` command is not installed; leftover `full_name` references remain only in demo auth code, which is intentionally out of scope for this refactor.

- **Prompt:** Answers to open decisions: address, phone, and email should stay simple free-text fields with minimal validation; report page should use a labeled before/after gallery; employee status should be appointment status only. Proceed with implementation in Agent mode, sub-task 1 first, and log progress to [`PROMPTS.md`](PROMPTS.md) as we go.
  **Summary:** Locked the remaining MVP data and UI decisions, then started sub-task 1 to create the initial repository scaffold and configuration surface.


## DevOps/CI
- No entries yet.

## Testing
- No entries yet.

## Prompt Logging Setup
- **Prompt:** I also added prompt logging to the @AGENTS.md and Yes, restructure PROMPTS.md now into sections: Planning, Architecture, Scaffolding, Implementation, DevOps/CI, Testing. Keep entries concise — prompt (or a short paraphrase if long) + 1-2 sentence summary of what it produced. From now on, append each new prompt/response to the correct section as we go.
  **Summary:** Reorganized [`PROMPTS.md`](PROMPTS.md) into the requested sections and added the existing history in a concise showcase-friendly format. From now on, new prompts and outcomes should be appended under the relevant section.