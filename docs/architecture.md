# Architecture

## Goal

Expose data that already exists in Microsoft SQL Server through a maintainable
API service.

## Layers

- `api/`: Receives HTTP requests and returns responses.
- `services/`: Coordinates use cases and business logic.
- `repositories/`: Contains SQL queries and database access code.
- `db/`: Owns SQL Server connection and configuration concerns.
- `schemas/`: Defines request and response contracts.

## Design Rules

- Routes should not contain SQL statements.
- Services should not know HTTP framework details.
- Repositories should isolate database-specific logic.
- Credentials must come from environment variables.
