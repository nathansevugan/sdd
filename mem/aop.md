# Aspect-Oriented Programming

## Python (Backend)

Python achieves AOP-style cross-cutting concerns via decorators and middleware.

| Concern | Mechanism |
|---------|-----------|
| Audit logging | Custom decorator |
| Performance tracing | `@trace` decorator / OpenTelemetry |
| Auth checks | `Depends(get_current_user)` |
| Retry logic | `tenacity` library |
| Transactions | SQLAlchemy session context |

### Custom Audit Decorator

```python
# shared/decorators.py
import functools
import logging

logger = logging.getLogger(__name__)

def audit_log(action: str):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            logger.info("audit", extra={"action": action, "result": str(result)})
            return result
        return wrapper
    return decorator

# Usage
@audit_log(action="WIDGET_CREATED")
async def create(self, payload: CreateWidgetRequest) -> WidgetResponse:
    ...
```

### Middleware (global cross-cutting)

```python
# shared/middleware.py
from fastapi import FastAPI, Request
import time

def register_middleware(app: FastAPI) -> None:

    @app.middleware("http")
    async def timing_middleware(request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start
        response.headers["X-Response-Time"] = f"{duration:.4f}s"
        return response
```

### Retry (tenacity)

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
async def call_external_api(payload: dict) -> dict:
    ...
```

### Rules

- Decorators handle **infrastructure concerns only** — no business logic.
- Keep decorators stateless and side-effect-free (except logging).
- Middleware registered in `register_middleware()` only — not scattered across files.

---

## Angular (Frontend)

| Concern | Mechanism |
|---------|-----------|
| HTTP logging/auth | `HttpInterceptorFn` |
| Route guards | `CanActivateFn` |
| Error boundary | `ErrorHandler` override |

---

## React (Frontend) — Updated

| Concern | Mechanism |
|---------|-----------|
| HTTP auth/errors | Custom `apiFetch` wrapper |
| Route protection | Loader `redirect()` in React Router v7 |
| Error boundary | `<ErrorBoundary>` component (react-error-boundary) |
| Loading states | TanStack Query `isPending` + Suspense |

```jsx
// Route-level auth guard via loader
export async function loader() {
  const token = getToken()
  if (!token) throw redirect('/login')
  return null
}
```
