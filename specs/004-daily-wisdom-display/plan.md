# Implementation Plan: Daily Wisdom Display

**Branch**: `004-daily-wisdom-display` | **Date**: 2026-05-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-daily-wisdom-display/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Daily wisdom display feature for React SPA frontend with FastAPI Python backend. The system will display a daily wisdom card on the landing page with UTC-based rotation, 365-day uniqueness guarantee, and copy-to-clipboard functionality. Uses PostgreSQL database with pre-populated wisdom content managed via admin interface.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.12, React 19 (JavaScript)  
**Primary Dependencies**: FastAPI, SQLAlchemy 2.x (async), React Router v7, Zustand, TanStack Query  
**Storage**: PostgreSQL 16 (existing Docker instance)  
**Testing**: pytest (backend), React Testing Library (frontend)  
**Target Platform**: Web browser (desktop/mobile)  
**Project Type**: web-service  
**Performance Goals**: <2s page load, <10s view-and-copy workflow, 99.9% uptime  
**Constraints**: UTC time handling, 365-day wisdom uniqueness, clipboard API support  
**Scale/Scope**: Landing page component, daily wisdom rotation for all users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Golden Rules Compliance

✅ **Rule 1**: Consistency over cleverness - Following React SPA + FastAPI patterns from constitution
✅ **Rule 2**: Fail fast, fail loudly - Error handling with user-friendly messages and retry functionality
✅ **Rule 3**: Everything is a module - Wisdom service as separate module with clear boundaries
✅ **Rule 4**: Observability first - Logging and metrics for wisdom rotation and API performance
✅ **Rule 5**: React is the only UI framework - Using React 19 with JavaScript only
✅ **Rule 6**: No raw SQL - Using SQLAlchemy 2.x async ORM with Alembic migrations

### Stack Compliance

✅ **Frontend**: React 19, React Router v7, Zustand, TanStack Query (matches constitution)
✅ **Backend**: Python 3.12, FastAPI (matches constitution)
✅ **Database**: PostgreSQL 16 with existing Docker instance (matches constitution)
✅ **ORM**: SQLAlchemy 2.x (async) (matches constitution)
✅ **Migrations**: Alembic (matches constitution)
✅ **API Style**: REST via FastAPI (matches constitution)

### Database Rules Compliance

✅ **Connection**: Using provided connection string, no local database creation
✅ **Schema**: Will use dedicated schema (app) for all wisdom objects
✅ **Naming**: Following snake_case conventions for tables and columns
✅ **Models**: Using mapped_column typed style with TimestampMixin
✅ **Migrations**: Using Alembic with proper versioning

**Result**: ✅ PASSED - No constitutional violations identified

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
daily-wisdom-ui/           # React SPA frontend
├── src/
│   ├── components/
│   │   ├── WisdomCard/          # Daily wisdom card component
│   │   │   ├── WisdomCard.jsx
│   │   │   ├── WisdomCard.test.jsx
│   │   │   └── index.js
│   │   └── common/              # Shared UI components
│   ├── pages/
│   │   └── LandingPage.jsx      # Main landing page
│   ├── services/
│   │   └── wisdomService.js    # API client for wisdom endpoints
│   ├── hooks/
│   │   └── useWisdom.js        # Custom hook for wisdom data
│   ├── utils/
│   │   └── clipboard.js        # Clipboard utility functions
│   └── App.jsx

├── public/
└── package.json

daily-wisdom-api/          # FastAPI Python backend
├── src/
│   ├── models/
│   │   └── wisdom.py           # SQLAlchemy wisdom models
│   ├── services/
│   │   └── wisdom_service.py   # Business logic for wisdom rotation
│   ├── api/
│   │   └── endpoints/
│   │       └── wisdom.py       # REST API endpoints
│   ├── schemas/
│   │   └── wisdom.py           # Pydantic models for API
│   └── core/
│       ├── config.py           # Database and app configuration
│       └── database.py         # Database session management
├── alembic/                   # Database migrations
│   ├── versions/
│   └── env.py
├── tests/
│   ├── unit/
│   └── integration/
└── requirements.txt
```

**Structure Decision**: Web application with separate frontend (React SPA) and backend (FastAPI) repositories. Frontend uses component-based architecture with custom hooks and services. Backend follows layered architecture with models, services, API endpoints, and schemas.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
