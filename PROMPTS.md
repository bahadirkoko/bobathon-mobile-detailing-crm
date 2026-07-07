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

- **Prompt:** Answers to open decisions: address, phone, and email should stay simple free-text fields with minimal validation; report page should use a labeled before/after gallery; employee status should be appointment status only. Proceed with implementation in Agent mode, sub-task 1 first, and log progress to [`PROMPTS.md`](PROMPTS.md) as we go.
  **Summary:** Locked the remaining MVP data and UI decisions, then started sub-task 1 to create the initial repository scaffold and configuration surface.


## DevOps/CI
- No entries yet.

## Testing
- No entries yet.

## Prompt Logging Setup
- **Prompt:** I also added prompt logging to the @AGENTS.md and Yes, restructure PROMPTS.md now into sections: Planning, Architecture, Scaffolding, Implementation, DevOps/CI, Testing. Keep entries concise — prompt (or a short paraphrase if long) + 1-2 sentence summary of what it produced. From now on, append each new prompt/response to the correct section as we go.
  **Summary:** Reorganized [`PROMPTS.md`](PROMPTS.md) into the requested sections and added the existing history in a concise showcase-friendly format. From now on, new prompts and outcomes should be appended under the relevant section.