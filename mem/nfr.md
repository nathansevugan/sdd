# Non-Functional Requirements

## Performance

| Metric | Target |
|--------|--------|
| API p95 response time | < 300ms |
| API p99 response time | < 1s |
| Angular initial bundle (gzipped) | < 200KB |
| Angular LCP | < 2.5s |
| DB query time (indexed) | < 50ms |

- Enable `@EnableAsync` + virtual threads (Python 3.12) for I/O-bound work.
- Paginate all list endpoints: default page size 20, max 100.

---

## Availability & Resilience

- Target uptime: **99.9%** (≤ 8.7h downtime/year)
- All services: minimum 2 replicas in production.
- Circuit breakers on all external HTTP calls (Resilience4j).
- Database connection pool monitored — alert at > 80% utilisation.
- Graceful shutdown: `server.shutdown=graceful` in Spring.

---

## Security

- HTTPS everywhere — HTTP redirects to HTTPS.
- JWT expiry: access token 15min, refresh token 7 days.
- Passwords: passlib bcrypt rounds ≥ 12.
- CORS: explicit allowed origins — no wildcard in production.
- Headers: `Content-Security-Policy`, `X-Frame-Options: DENY`, `HSTS`.
- Dependency scanning: Dependabot + OWASP Dependency-Check in CI.

---

## Observability

| Signal | Tool |
|--------|------|
| Logs | Structured JSON → ELK / Loki |
| Metrics | Micrometer → Prometheus → Grafana |
| Traces | OpenTelemetry → Tempo / Jaeger |
| Alerts | Alertmanager / PagerDuty |

Every service must expose `/actuator/health`, `/actuator/metrics`, `/actuator/info`.

---

## Scalability

- Stateless services — session state in JWT only.
- Horizontal scaling via Kubernetes HPA.
- Database read replicas for reporting queries.
- Cache frequently read, rarely written data in Redis (TTL explicit).

---

## Accessibility (Angular)

- WCAG 2.1 AA minimum.
- All interactive elements keyboard-navigable.
- `aria-*` attributes on all custom components.
- Colour contrast ratio ≥ 4.5:1 for text.
- react-aria / Radix UI primitives used for focus traps and live regions.

---

## Testability

| Layer | Minimum Coverage |
|-------|-----------------|
| Use cases (unit) | 90% |
| Controllers (integration) | 80% |
| Angular components | 80% |
| E2E critical paths | 100% |

- Integration tests use **Testcontainers** (real PostgreSQL).
- No mocking of the database in integration tests.
