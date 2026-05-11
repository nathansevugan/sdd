# System Architecture

## High-Level Overview

```mermaid
graph TD
    Browser["Browser\n(React SPA)"]
    AppService["App Service\n(FastAPI)"]
    DB[(PostgreSQL)]

    Browser -->|HTTPS REST| AppService
    AppService -->|JPA| DB
```

---

## Hexagonal Architecture (per service)

```mermaid
graph LR
    subgraph Adapters-In
        HTTP[REST Controller]
        MSG[Message Consumer]
    end

    subgraph Core
        UC[Use Case]
        DOM[Domain Model]
    end

    subgraph Adapters-Out
        REPO[JPA Repository]
        EXT[External HTTP Client]
        PUB[Event Publisher]
    end

    HTTP --> UC
    MSG --> UC
    UC --> DOM
    UC --> REPO
    UC --> EXT
    UC --> PUB
```

- **Core** has zero dependency on adapters.
- Ports (interfaces) defined in `core/port/`.

---

## Request Lifecycle

```mermaid
sequenceDiagram
    participant R as React
    participant P as Spring Service
    participant D as PostgreSQL

    R->>P: POST/GET requests
    P->>P: @Valid DTO
    P->>D: INSERT widget
    D-->>P: saved entity
    P-->>R: 201 WidgetResponse
```

---

## Deployment

```mermaid
graph LR
    CI[GitHub Actions CI]
    Registry[Container Registry]
    K8S[Kubernetes Cluster]
    PG[(PostgreSQL\nManaged)]

    CI -->|build & push image| Registry
    Registry -->|pull| K8S
    K8S -->|JDBC| PG
```

- Each service is a Docker image.
- Config via Kubernetes `ConfigMap` + `Secret`.
- Alembic migrations run as a Kubernetes Job on deploy.
