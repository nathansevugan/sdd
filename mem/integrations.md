# Integration Flows

## Auth Flow

```mermaid
sequenceDiagram
    participant A as Angular
    participant API as FastAPI
    participant DB as PostgreSQL

    A->>API: POST /auth/login {email, password}
    API->>DB: SELECT user WHERE email=?
    DB-->>API: User record
    API->>API: BCrypt verify password
    API-->>A: {accessToken, refreshToken}
    A->>A: Store token in memory (not localStorage)
    A->>API: GET /api/v1/widgets\nAuthorization: Bearer <token>
    API->>API: JwtFilter validates signature + expiry
    API-->>A: 200 OK
```

---

## Token Refresh Flow

```mermaid
sequenceDiagram
    participant A as Angular (authInterceptor)
    participant API as FastAPI

    A->>API: Any request (expired token)
    API-->>A: 401 Unauthorized
    A->>API: POST /auth/refresh {refreshToken}
    API-->>A: {accessToken}
    A->>API: Retry original request
    API-->>A: 200 OK
```

---

## Data Mutation Flow (Angular → DB)

```mermaid
flowchart TD
    UI[Component] -->|dispatch action| Store[Zustand + TanStack Query]
    Store -->|rxMethod| Service[Angular Service]
    Service -->|HttpClient POST| API[Spring Controller]
    API -->|@Valid| UseCase[Use Case]
    UseCase -->|save| Repo[JPA Repository]
    Repo -->|SQL INSERT| DB[(PostgreSQL)]
    DB --> Repo --> UseCase --> API
    API -->|201 + body| Service
    Service -->|patchState| Store
    Store -->|signal update| UI
```

---

## External Integration Pattern

For any third-party API:

```mermaid
flowchart LR
    UC[Use Case] --> Port[OutboundPort interface]
    Port --> Adapter[HTTP Adapter]
    Adapter -->|WebClient| Ext[External API]
    Adapter -->|on failure| Fallback[Fallback / Circuit Breaker]
```

- All external calls behind an interface (port).
- Use **Resilience4j** `@CircuitBreaker` + `@Retry`.
- Timeouts configured explicitly — never rely on defaults.

```java
@CircuitBreaker(name = "externalService", fallbackMethod = "fallback")
@Retry(name = "externalService")
public ExternalResponse call(Request req) { ... }
```
