# Speckit Constitution

> Single source of truth for architecture, style, and engineering standards.

---

## Sections

| # | Topic | File |
|---|-------|------|
| 1 | Design System | [design.md](./design.md) |
| 2 | Frontend — React | [frontend-react.md](./frontend-react.md) |
| 3 | Backend — Python & FastAPI | [backend-python.md](./backend-python.md) |
| 4 | Database — PostgreSQL | [database.md](./database.md) |
| 5 | Security | [security.md](./security.md) |
| 6 | Coding Standards | [coding-standards.md](./coding-standards.md) |
| 7 | System Architecture | [architecture.md](./architecture.md) |
| 8 | IoC & Dependency Injection | [ioc.md](./ioc.md) |
| 9 | Aspect-Oriented Programming | [aop.md](./aop.md) |
| 10 | Non-Functional Requirements | [nfr.md](./nfr.md) |
| 11 | Integration Flows | [integrations.md](./integrations.md) |
| 12 | Software Design | [software-design.md](./software-design.md) |
| 13| Deployment | [deployment.md](./deployment.md) |

---

## Stack at a Glance

| Layer | Technology |
|-------|-----------|
| Frontend | React 19, React Router v7, Zustand, TanStack Query |
| Backend | Python 3.12, FastAPI |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy 2.x (async) |
| Migrations | Alembic |
| Auth | python-jose (JWT) + passlib |
| API Style | REST (OpenAPI 3 via FastAPI) |

---

## Golden Rules

1. **Consistency over cleverness** — follow the patterns in this constitution.
2. **Fail fast, fail loudly** — no silent errors.
3. **Everything is a module** — loose coupling, tight cohesion.
4. **Observability first** — logs, metrics, traces on every service.
5. **React is the only UI framework** — JavaScript only, no TypeScript, no other SPA frameworks.
6. **No raw SQL** — use SQLAlchemy ORM; migrations via Alembic only.
