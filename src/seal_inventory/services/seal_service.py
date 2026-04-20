"""Service layer for Seal Inventory read operations."""

from __future__ import annotations

from seal_inventory.repositories.seal_repository import SealRepository


class SealService:
    """Coordinate read-only data access use cases."""

    def __init__(self, repository: SealRepository | None = None) -> None:
        self.repository = repository or SealRepository()

    def get_database_health(self) -> bool:
        """Check whether the database can be reached."""
        is_alive = self.repository.check_connection()

        if not is_alive:
            raise RuntimeError("Database is not reachable")

        return True

    def get_tables(self) -> list[str]:
        """Return available tables."""
        tables = self.repository.list_tables()

        if not tables:
            raise ValueError("No tables found in schema")

        return tables

    def get_schema_name(self) -> str:
        """Return the configured source schema name."""
        return self.repository.schema_name

    def get_table_rows(self, table_name: str, limit: int) -> list[dict]:
        """Return a limited set of rows for a given table."""

        if not table_name:
            raise ValueError("Table name is required")

        rows = self.repository.fetch_rows(table_name=table_name, limit=limit)

        return rows

    def get_eseal_inventory(self, limit: int):
        if limit > 1000:
            raise ValueError("Limit cannot exceed 1000")

        return self.repository.get_eseal_inventory(limit=limit)