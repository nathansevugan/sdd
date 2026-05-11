# IoC & Dependency Injection

## FastAPI `Depends()` (Backend)

FastAPI's `Depends()` is the DI mechanism — no external container needed.

### Class-Based Dependencies (preferred)

```python
class WidgetService:
    def __init__(self, repo: WidgetRepository = Depends()):
        self.repo = repo

@router.get("/")
async def list_widgets(svc: WidgetService = Depends()):
    return await svc.list()
```

### Function-Based Dependencies

```python
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> dict:
    return decode_token(credentials.credentials)
```

### Scoping

| Scope | How |
|-------|-----|
| Per-request (default) | `Depends()` |
| App singleton | Instantiate in `lifespan` or module-level |
| Override in tests | `app.dependency_overrides[dep] = mock_dep` |

### Rules

- Never instantiate services manually inside routes.
- Never use global mutable state — pass deps explicitly.
- Keep dependency chains ≤ 3 levels deep.

---

## React (Frontend)

React has no DI container — dependencies flow via hooks and context.

### Custom Hooks as Services

```jsx
// shared/hooks/useAuth.js
import { useAuthStore } from '../store/authStore'

export function useAuth() {
  const token = useAuthStore(s => s.token)
  const logout = useAuthStore(s => s.logout)
  return { token, logout, isAuthenticated: !!token }
}

// Usage in component
function Header() {
  const { isAuthenticated, logout } = useAuth()
  ...
}
```

### Context for Cross-Cutting Deps

```jsx
// Only for truly global concerns (theme, locale, auth)
const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(null)
  return <AuthContext.Provider value={{ token, setToken }}>{children}</AuthContext.Provider>
}

export const useAuthContext = () => useContext(AuthContext)
```

### Rules

- Prefer **custom hooks** over context for feature-level state.
- Context only for app-level concerns: auth, theme, locale.
- TanStack Query replaces service-layer DI for server state.
- Mock hooks in tests via `vi.mock()` — no DI container needed.
