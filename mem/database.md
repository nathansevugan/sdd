# Database — PostgreSQL

## database
postgres database is already running as a local docker instance. do not create or brew install database locally. use the following connection string to connect to the database:

```
postgresql+asyncpg://daily_wisdom_user:daily_wisdom_user@localhost:5432/daily_wisdom
```

## Version & Driver

| Item | Choice |
|------|--------|
| Database | PostgreSQL 16+ |
| Async driver | `asyncpg` |
| ORM | SQLAlchemy 2.x (async) |
| Migrations | Alembic |
| Sync driver (scripts/CLI only) | `psycopg2` |

---

## Connection & Pooling

Use SQLAlchemy's async engine backed by `asyncpg`. Pool settings via environment variables.

```python
# db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

engine = create_async_engine(
    settings.database_url,   # postgresql+asyncpg://user:pass@host/db
    pool_size=10,
    max_overflow=5,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
    echo=False,
)

async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with async_session_factory() as session:
        yield session
```

- `DATABASE_URL` always from environment — never hardcoded.
- `pool_pre_ping=True` — validates connections before use.
- Pool size baseline: `(2 × CPU cores) + 1`.
- One engine instance per application process — never create per-request.

---

## Schema & Database Object Rules

- All application objects live in a **dedicated schema** (e.g. `app`) — never `public`.
- The `public` schema is revoked from all application users.
- Separate DB users per concern:

| User | Permissions |
|------|-------------|
| `speckit_app` | `SELECT`, `INSERT`, `UPDATE`, `DELETE` on `app.*` |
| `speckit_migrate` | DDL rights on `app.*` — used only by Alembic |
| `speckit_readonly` | `SELECT` only — used for reporting/analytics |

- No stored procedures, no triggers, no database-level functions.
- No views unless approved for reporting purposes.
- Business logic lives exclusively in Python.

---

## Naming Conventions

| Object | Convention | Example |
|--------|-----------|---------|
| Tables | `snake_case`, plural | `widgets`, `user_profiles` |
| Columns | `snake_case` | `created_at`, `deleted_at` |
| Primary keys | `id` (UUID) | `id UUID DEFAULT gen_random_uuid()` |
| Foreign keys | `{table_singular}_id` | `widget_id` |
| Indexes | `idx_{table}_{column}` | `idx_widgets_deleted_at` |
| Constraints | `uq_{table}_{column}` | `uq_users_email` |

---

## SQLAlchemy Model Style

```python
from sqlalchemy import String, Numeric, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from uuid import UUID, uuid4
from datetime import datetime

class Base(DeclarativeBase):
    __table_args__ = {"schema": "app"}   # all models in app schema

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)
```

- All models extend `Base` and `TimestampMixin`.
- Use `mapped_column` typed style (SQLAlchemy 2.x) — no legacy `Column()`.
- Filter soft deletes in every repository query — `where(Model.deleted_at.is_(None))`.
- No bidirectional relationships unless explicitly justified.
- No `lazy="dynamic"` — use `selectinload()` or `joinedload()` explicitly.

---

## Migrations (Alembic)

```
db/
└── migrations/
    ├── env.py
    ├── script.py.mako
    └── versions/
        ├── 001_initial_schema.py
        └── 002_add_user_profiles.py
```

```python
# env.py — target schema
target_metadata = Base.metadata
version_table_schema = "app"
```

```bash
# Apply
alembic upgrade head

# Generate
alembic revision --autogenerate -m "add_user_profiles"
```

- Migrations run as a **pre-deploy step** in CI/CD using `speckit_migrate` user.
- Migration files are **immutable** once merged to `main`.
- Destructive changes (DROP, rename, type change) require a dedicated reviewed PR.
- No raw SQL in migrations unless schema-level DDL is unavoidable.
- No data migrations mixed with schema migrations — keep them separate.

---

## Performance Rules

- Index every foreign key and high-frequency filter column.
- Run `EXPLAIN ANALYZE` for any query touching > 10k rows before merging.
- All list endpoints paginated — no unbounded queries.
- Use `expire_on_commit=False` to avoid implicit re-fetches.
- Never SELECT * in application code — always specify columns via ORM attributes.
