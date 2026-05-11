# Backend — Python & FastAPI

## Stack

| Concern | Choice |
|---------|--------|
| Language | Python 3.12+ |
| Framework | FastAPI |
| ORM | SQLAlchemy 2.x (async) |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| Auth | `python-jose` (JWT) + `passlib` (bcrypt) |
| HTTP Client | `httpx` (async) |
| DI | FastAPI `Depends()` |
| Testing | Pytest + `httpx.AsyncClient` + Testcontainers |
| Task Queue | Celery + Redis |
| Linting | Ruff + mypy (strict) |
| Package Mgmt | `uv` |

---

## Project Structure

```
app/
├── main.py                  # FastAPI app factory
├── core/
│   ├── config.py            # Settings via pydantic-settings
│   ├── security.py          # JWT encode/decode
│   └── dependencies.py      # Shared Depends() factories
├── domain/
│   ├── models/              # SQLAlchemy ORM models
│   └── schemas/             # Pydantic request/response schemas
├── features/
│   └── [feature]/
│       ├── router.py        # APIRouter
│       ├── service.py       # Business logic
│       └── repository.py    # DB access
├── shared/
│   ├── exceptions.py
│   └── middleware.py
└── db/
    ├── session.py           # Async engine + session factory
    └── migrations/          # Alembic versions
```

---

## App Factory

```python
# main.py
from fastapi import FastAPI
from app.features.widgets.router import router as widgets_router
from app.shared.middleware import register_middleware
from app.shared.exceptions import register_exception_handlers

def create_app() -> FastAPI:
    app = FastAPI(title="Speckit API", version="1.0.0")
    register_middleware(app)
    register_exception_handlers(app)
    app.include_router(widgets_router, prefix="/api/v1")
    return app

app = create_app()
```

---

## Router Style

```python
# features/widgets/router.py
from fastapi import APIRouter, Depends, status
from app.features.widgets.service import WidgetService
from app.domain.schemas.widget import WidgetResponse, CreateWidgetRequest
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/widgets", tags=["Widgets"])

@router.get("/", response_model=list[WidgetResponse])
async def list_widgets(svc: WidgetService = Depends()):
    return await svc.list()

@router.post("/", response_model=WidgetResponse, status_code=status.HTTP_201_CREATED)
async def create_widget(
    payload: CreateWidgetRequest,
    svc: WidgetService = Depends(),
    _: dict = Depends(get_current_user),
):
    return await svc.create(payload)
```

- Routers are **thin** — delegate to service immediately.
- All routes use `async def`.

---

## Service Style

```python
# features/widgets/service.py
from fastapi import Depends
from app.features.widgets.repository import WidgetRepository
from app.domain.schemas.widget import CreateWidgetRequest, WidgetResponse
from app.domain.models.widget import Widget

class WidgetService:
    def __init__(self, repo: WidgetRepository = Depends()):
        self.repo = repo

    async def list(self) -> list[WidgetResponse]:
        return [WidgetResponse.model_validate(w) for w in await self.repo.find_all()]

    async def create(self, payload: CreateWidgetRequest) -> WidgetResponse:
        widget = await self.repo.save(Widget(**payload.model_dump()))
        return WidgetResponse.model_validate(widget)
```

---

## Repository Style

```python
# features/widgets/repository.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_session
from app.domain.models.widget import Widget

class WidgetRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def find_all(self) -> list[Widget]:
        result = await self.session.execute(select(Widget))
        return result.scalars().all()

    async def save(self, widget: Widget) -> Widget:
        self.session.add(widget)
        await self.session.commit()
        await self.session.refresh(widget)
        return widget
```

---

## Schemas (Pydantic v2)

```python
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from decimal import Decimal

class CreateWidgetRequest(BaseModel):
    name: str
    price: Decimal

class WidgetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    price: Decimal
```

---

## Exception Handling

```python
# shared/exceptions.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class NotFoundError(Exception):
    def __init__(self, detail: str):
        self.detail = detail

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def not_found(_: Request, exc: NotFoundError):
        return JSONResponse(status_code=404, content={"detail": exc.detail})
```

- RFC 9457-style `{"detail": "..."}` for all errors.
- Never expose tracebacks to clients.

---

## Security

```python
# core/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_token

bearer = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> dict:
    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return payload
```

---

## Config (pydantic-settings)

```python
# core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    class Config:
        env_file = ".env"

settings = Settings()
```

- All config from environment variables — never hardcoded.
