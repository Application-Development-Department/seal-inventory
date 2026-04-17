# Seal Inventory

Seal Inventory is structured as an API service that connects to Microsoft SQL
Server, reads existing records, and exposes them through HTTP endpoints.

## Intended Flow

```text
Client -> API routes -> services -> repositories -> SQL Server
```

## Structure

```text
Seal Inventory/
|-- config/
|   `-- settings.example.env     # Example environment variables
|-- docs/
|   `-- architecture.md          # High-level system design
|-- scripts/                     # Local utility scripts
|-- src/
|   `-- seal_inventory/
|       |-- api/                 # API app bootstrap and routes
|       |-- core/                # Shared domain constants and rules
|       |-- db/                  # SQL Server configuration and connections
|       |-- repositories/        # SQL query layer
|       |-- schemas/             # API request and response schemas
|       |-- services/            # Use-case orchestration
|       `-- utils/               # Shared helpers
`-- tests/
    |-- integration/             # API and database integration tests
    `-- unit/                    # Fast isolated logic tests
```

## Notes

- Keep secrets in environment variables, not in source files.
- Keep SQL access inside `repositories/`.
- Keep connection setup and pooling inside `db/`.
- Keep route handlers thin and move business logic into `services/`.

## Run

1. Copy `config/settings.example.env` into a local `.env` file or set the same
   variables in your environment.
2. Install project dependencies from `pyproject.toml`.
3. Start the API with:

```text
uvicorn seal_inventory.api.app:app --reload
```

## Initial Endpoints

- `GET /health`
- `GET /db/health`
- `GET /tables`
- `GET /tables/{table_name}/rows?limit=100`
