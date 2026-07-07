# AGENTS.md

This file provides guidance to agents when working with code in this repository.

- Product scope: build a demo-ready CRM for mobile car detailing businesses with public booking, internal admin/employee operations, and MCP tool access to core workflows.
- Required stack: Python backend with FastAPI, SQLAlchemy ORM, PostgreSQL, Jinja2 templates, and HTMX. Do not introduce React or other SPA frameworks.
- Architecture rule: keep business logic in a service layer. FastAPI routes and MCP tools must both call the same service functions; do not duplicate CRUD or workflow logic.
- MCP rule: use the official Python MCP SDK and expose core CRM operations as tools so an MCP client can manage the system via natural language.
- Data rule: PostgreSQL is the system of record and must run through Docker Compose locally and in CI.
- Code organization: keep routes thin, services focused on business rules, and persistence concerns isolated from HTTP/MCP entry points.
- Public/customer UI is server-rendered with Jinja2 and enhanced with HTMX for interactivity.
- Internal users include business admins and employees/technicians; model authorization accordingly.

## Data Model

### Main entities (build these first)
- **Customer**: name, contact info (phone/email), address
- **Employee**: name, role (admin/technician), contact info
- **Vehicle**: type/size (sedan/SUV/truck), linked to Customer
- **Appointment**: scheduled datetime, service address, status (scheduled/in_progress/completed/cancelled), linked to Customer, Vehicle, and assigned Employee

### Supporting entities (add once main entities work end-to-end)
- **Package**: name, base price, description (e.g. "Basic Wash", "Full Detail") — linked to an Appointment
- **AddOn**: name, price (e.g. "Ceramic Coating", "Interior Deep Clean") — many-to-many with Appointment
- **BlockedDate**: date/time range, reason (optional) — used to prevent booking during unavailable slots (e.g. holidays, employee time off)

Build order: get Customer, Employee, Vehicle, and Appointment fully working (create, read, update, list) with a single flat price field on Appointment first. Only add Package, AddOn, and BlockedDate once that core loop is solid end-to-end (booking → dashboard → MCP tool control all working). Do not block core functionality on the supporting entities.

## Financial & Auth Scope
- Financial tracking scope: limited to price on the Appointment (and later, Package/AddOn pricing once implemented). No invoicing, payments processing, or financial reporting system.
- Auth scope: minimal role flag (admin/employee) via simple session, not a full auth system. No OAuth, no JWT, no password reset flows.

## UI Rules
- Admin and employee dashboards share the same templates; differences are driven by a role flag, not separate template sets or separate applications.
- Public customer booking page requires no authentication.

## Coding Standards
- Type rule: add type hints to all functions.
- Documentation rule: add docstrings to all public functions and classes.
- Error handling rule: handle errors explicitly; do not allow silent failures or swallow exceptions.
- Testing rule: add unit tests for all service-layer logic.
- Testing stack: use pytest and pytest-cov.
- CI requirement: GitHub Actions must install dependencies, start PostgreSQL as a service container, and run tests with coverage.
- Quality target: code should be production-style even though the project is for a time-limited demo.
- Security rule: do not hardcode secrets; use environment variables for credentials and configuration.
- Storage/deployment note: this build intentionally uses local disk photo storage and local Docker Compose PostgreSQL for demo delivery; cloud storage and managed hosting must remain swap-in-later concerns behind service boundaries.
- Network rule: do not recommend binding services to 0.0.0.0 unless the repository later explicitly requires a controlled exception.

## Prompt Logging
- After completing each meaningful task/prompt, append an entry to 
  PROMPTS.md under the appropriate section: the prompt VERBATIM (not 
  paraphrased) if it involved a real decision or non-trivial instruction, 
  plus a 1-2 sentence summary of the outcome. Trivial/mechanical prompts 
  (typo fixes, small tweaks) can be paraphrased briefly instead.

## Meta
- When scaffolding the repo, prefer commands and tooling that work cleanly in local Docker Compose and GitHub Actions.
- If repository files are later added, update this file to replace scope-level guidance with concrete project-specific commands and conventions discovered from code/config.