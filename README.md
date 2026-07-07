# Mobile Detailing CRM

A demo-ready CRM for mobile car detailing businesses built with Python, FastAPI, PostgreSQL, SQLAlchemy, Jinja2, and HTMX.

## Problem Statement

Mobile detailing businesses usually manage bookings, customer details, vehicle records, employee scheduling, job progress, and service reports across text messages, notes apps, spreadsheets, and phone calls. That creates a few predictable problems:

- customer and vehicle information gets scattered
- appointment scheduling is hard to track in one place
- admins lack visibility into who is assigned to which job
- field employees need a simple way to update work status and upload before/after photos
- demoing operations to stakeholders is difficult without a single end-to-end system

This project is a focused solution for that problem: a lightweight CRM that combines public booking, internal operations management, employee workflow support, and MCP tool access in one Python-first application.

## Solution Overview

This application provides two main experiences:

1. **Customer-facing booking flow** for creating appointments without authentication
2. **Internal dashboard** for admins and employees to manage customers, vehicles, packages, appointments, employee records, and appointment photo/report workflows

It is intentionally built as a server-rendered app for speed, simplicity, and demo-readiness. Instead of a separate SPA frontend, the UI uses Jinja2 templates with HTMX-enhanced interactions.

## Current Features

### Public booking
- Create a booking from a customer-facing form
- Capture customer details, vehicle details, package selection, and appointment time
- Create the linked customer, vehicle, and appointment records in one flow

### Dashboard and operations
- Dashboard landing page for authenticated internal users
- Customer management
  - create customers
  - edit customers
  - manage customer-owned vehicles directly under each customer
  - create, edit, and delete vehicles from the customer context
- Appointment management
  - create appointments
  - edit appointments
  - update appointment status
  - assign employees to jobs
  - select packages for appointments
- Employee management
  - create employees
  - edit employees
- Package management
  - create packages
  - edit packages
  - delete packages

### Job execution and reporting
- Upload before/after appointment photos
- Store photos on local disk for demo use
- Render a server-side appointment report page
- Track appointment status for operational visibility

### MCP integration
- Exposes core CRM operations through MCP tools
- MCP tools call the same service layer used by HTTP routes
- Supports natural-language-driven management workflows from an MCP client

## Tech Stack

### Backend
- [`FastAPI`](app/main.py) for HTTP routes and application wiring
- [`SQLAlchemy 2.x`](app/db/base.py) for ORM and persistence
- [`PostgreSQL`](docker-compose.yml) as the system of record
- [`Pydantic v2`](pyproject.toml) for request and response schemas

### Frontend
- [`Jinja2`](app/templates) for server-rendered pages
- [`HTMX`](app/templates/base.html) for partial page updates without SPA complexity
- Plain CSS inside the shared base template for simple demo styling

### Architecture
- Service-layer-first design in [`app/services`](app/services)
- Thin FastAPI routes in [`app/api/routes`](app/api/routes)
- Shared business logic reused by both HTTP and MCP entry points
- Startup-driven schema creation via [`Base.metadata.create_all()`](app/main.py:37)

### Tooling and testing
- [`pytest`](pyproject.toml) and [`pytest-cov`](pyproject.toml) for tests
- [`ruff`](pyproject.toml) for linting
- Docker Compose for local PostgreSQL

## Project Structure

```text
app/
  api/           FastAPI dependencies and routes
  core/          configuration and auth helpers
  db/            SQLAlchemy base and session setup
  mcp/           MCP server and tool registration
  models/        ORM models
  schemas/       Pydantic schemas
  services/      business logic layer
  static/        uploads and static assets
  templates/     Jinja2 templates
tests/           service, route, and MCP tests
```

## How the App Works

### Booking flow
A public user fills in the booking form. The backend creates the customer, creates the linked vehicle, and creates the appointment tied to a package and optional employee assignment.

### Internal workflow
An admin or employee logs in through the demo login page, opens the dashboard, and manages operational data from server-rendered pages. HTMX is used for partial updates so common actions refresh only the relevant section of the page.

### MCP workflow
An MCP client can call tools to list, create, and update customers, employees, vehicles, and appointments. This keeps the same business rules available through both UI and tool-driven automation.

## Authentication Model

This project currently uses a **simple demo session-based login** suitable for a showcase environment.

- Browser users log in through [`/login`](app/templates/login.html)
- A signed session cookie is used for demo access
- There are demo admin and employee identities configured by environment variables

This is intentionally minimal and should be treated as demo auth, not a production-grade identity system.

## Local Development Setup

### Requirements
- Python 3.12+
- Docker / Docker Compose
- PostgreSQL via Docker Compose

### 1. Create your environment file

Copy [`.env.example`](.env.example) to [`.env`](.env):

```bash
cp .env.example .env
```

### 2. Start PostgreSQL

```bash
docker compose up -d
```

The database is bound to [`127.0.0.1:5432`](docker-compose.yml:10).

### 3. Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .[dev]
```

### 4. Run the application

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 5. Open the app

- Public booking: `http://127.0.0.1:8000/`
- Login: `http://127.0.0.1:8000/login`
- Dashboard: `http://127.0.0.1:8000/dashboard`

## Demo Credentials

The demo identities come from environment variables in [`.env`](.env):

- `DEMO_ADMIN_EMAIL`
- `DEMO_EMPLOYEE_EMAIL`

Use those values on the login page.

## Useful Commands

### Run tests

```bash
pytest
```

### Run tests with coverage

```bash
pytest --cov=app --cov-report=term-missing
```

### Run lint checks

```bash
ruff check .
```

### Compile the codebase

```bash
python3 -m compileall app tests
```

## Design Decisions

- **Server-rendered first:** faster to build and easier to demo than a split SPA architecture
- **HTMX instead of React:** enough interactivity for dashboard workflows without frontend build complexity
- **Service-layer-first architecture:** makes business rules reusable across UI routes and MCP tools
- **PostgreSQL as the system of record:** keeps the demo aligned with a realistic production-style data layer
- **Local file photo storage:** intentionally simple for demo delivery and can later be swapped behind a service boundary

## Scope Notes

This repository is optimized for a demo/hackathon-style CRM, not a fully hardened production platform. It focuses on the core loop:

- booking
- internal management
- employee assignment
- appointment progress
- before/after proof of work
- MCP-driven operations access

## Who This Project Is For

This README is meant to help:

- judges or reviewers evaluating the product quickly
- developers onboarding into the codebase
- stakeholders who want to understand the business problem and solution
- contributors who need to know how the system is organized
