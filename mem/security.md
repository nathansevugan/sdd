# Security

## Authentication

- Stateless JWT — no server-side sessions.
- Access token TTL: **15 minutes**.
- Refresh token TTL: **7 days**, stored in `HttpOnly` cookie.
- JWT signed with `HS256` (symmetric) — secret rotated per environment.
- Library: `python-jose[cryptography]`.

```python
# core/security.py
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings

def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub": subject, "exp": expire}, settings.secret_key, algorithm="HS256")

def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    except JWTError:
        return None
```

---

## Authorisation

- Role-based via JWT claims (`role` field).
- Enforced at the route level using `Depends()`.
- No row-level security in the database — handled in Python service layer.

```python
def require_role(role: str):
    def checker(user: dict = Depends(get_current_user)):
        if user.get("role") != role:
            raise HTTPException(status_code=403, detail="Forbidden")
    return Depends(checker)

@router.delete("/{id}", dependencies=[require_role("admin")])
async def delete_widget(id: UUID, svc: WidgetService = Depends()): ...
```

---

## Password Handling

- Library: `passlib[bcrypt]`
- BCrypt rounds: **12 minimum**.
- Never log, return, or store plaintext passwords.
- Never compare passwords with `==` — always use `passlib.verify()`.

```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

---

## Transport & Headers

- HTTPS enforced everywhere — HTTP redirects to HTTPS in all environments.
- Required response headers on every response:

| Header | Value |
|--------|-------|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` |
| `X-Content-Type-Options` | `nosniff` |
| `X-Frame-Options` | `DENY` |
| `Content-Security-Policy` | defined per environment |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |

```python
# shared/middleware.py
from fastapi import FastAPI
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

def register_middleware(app: FastAPI) -> None:
    app.add_middleware(HTTPSRedirectMiddleware)

    @app.middleware("http")
    async def security_headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response
```

---

## CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,  # explicit list — never ["*"] in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

- `allow_origins` sourced from environment variable — different per env.
- Wildcard (`*`) is banned in staging and production.

---

## Input Validation

- All inbound data validated by **Pydantic v2** before reaching service layer.
- Never trust client-supplied IDs for ownership — always verify against authenticated user.
- File uploads: validate MIME type server-side; reject unexpected types.

---

## Database Security

- Application uses `speckit_app` DB user — `SELECT`, `INSERT`, `UPDATE`, `DELETE` only.
- No DDL permissions for the app user.
- No stored procedures or triggers — no SQL injection surface via dynamic execution.
- Parameterised queries always via SQLAlchemy ORM — raw string interpolation into queries is banned.

---

## Secrets Management

- All secrets via environment variables — never committed to source control.
- `.env` files permitted locally only — excluded via `.gitignore`.
- Production secrets managed via a secrets manager (e.g. AWS Secrets Manager, Vault).
- Rotate `SECRET_KEY` and DB passwords per environment on a schedule.

---

## Dependency & Supply Chain

- `uv` lock file committed — reproducible builds.
- Dependabot enabled for Python and JavaScript dependencies.
- `pip audit` / `safety` run in CI — fail build on known CVEs.
- No unpinned dependencies in production.

---

## React Frontend

- JWT access token stored in **memory only** (Zustand store) — never `localStorage`.
- Refresh token in `HttpOnly` cookie — not accessible to JavaScript.
- All API calls via `apiFetch` wrapper — no direct `fetch` in components.
- CSP configured to block inline scripts and unknown origins.
- `dangerouslySetInnerHTML` banned — no exceptions.
