# software-design.md

## Principles

### SOLID

-   Single Responsibility Principle
-   Open/Closed Principle
-   Liskov Substitution Principle
-   Interface Segregation Principle
-   Dependency Inversion Principle

### Gang of Four (GoF)

-   Creational: Factory, Abstract Factory, Builder, Prototype, Singleton
-   Structural: Adapter, Bridge, Composite, Decorator, Facade,
    Flyweight, Proxy
-   Behavioral: Chain of Responsibility, Command, Interpreter, Iterator,
    Mediator, Memento, Observer, State, Strategy, Template Method,
    Visitor

### Code Constraints

-   Method/function size: max 10 lines
-   Class size: max 200 lines
-   Enforce Assignment of Responsibility
-   Prefer low coupling and high cohesion
-   Follow clean code practices (naming, readability, testability)

### Python Backend Guidelines

-   Use FastAPI for API layer
-   Use Pydantic for validation
-   Use dependency injection via FastAPI Depends
-   Separate layers: routers, services (use-cases), repositories, models
-   All external integrations behind interfaces (abstract base classes)
-   Implement adapters for integrations (HTTP clients using httpx)
-   Add retry/circuit breaker via libraries (e.g., tenacity)

### Environment Management

-   Use .env for configuration
-   Sensitive variables loaded from environment
-   Use python-dotenv or OS environment directly
