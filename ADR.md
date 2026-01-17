# Architecture Decision Record (ADR)

## Context
The legacy application was built using a monolithic service pattern where business logic, database operations, and API handling were tightly coupled. This made it difficult to:
- Test business rules independently of the database.
- Swap infrastructure components (e.g., changing parsers or databases).
- Scale development across multiple teams.

## Decision
We transitioned the entire codebase (Backend and Frontend) to **Hexagonal Architecture** (Ports and Adapters).

### Principles
1. **Dependency Inversion**: Dependencies point inwards toward the Domain.
2. **Domain Isolation**: Domain entities must remain pure with NO dependencies on external frameworks or databases.
3. **Ports as Protocols**: Application logic interacts with infrastructure via abstract Ports (Protocols in Python).
4. **Adapter Flexibility**: Frameworks, database tools, and UI are simply "details" (Adapters) that can be swapped or updated without touching core logic.

## Consequences
- **Positive**:
    - High testability (100% domain coverage possible without DB mocks).
    - Clearer code organization and developer mental model.
    - Resilience against framework breaking changes (e.g., Pydantic V2 migration affecting primarily the Presentation/Infrastructure layers).
- **Negative**:
    - Increased boilerplate (Mappers and DTOs).
    - Higher initial learning curve for new developers.

## Implementation Details
- **Backend Mapper Pattern**: We use explicit mapper functions (`event_to_domain`, `event_to_persistence`) to translate between ORM models and Domain entities.
- **Frontend Facade Pattern**: Presentation components only interact with Application Facades, ensuring the UI remains "dumb" and reactive (via Signals).
