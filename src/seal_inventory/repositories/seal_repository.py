"""Repository layer for SQL Server reads."""

from __future__ import annotations

import os
import re
from typing import Any

from seal_inventory.db.data_warehouse import SqlServerDataWarehouse

IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class SealRepository:
    """Read-only repository for existing SQL Server data."""

    def __init__(
            self,
            data_warehouse: SqlServerDataWarehouse | None = None,
            schema_name: str | None = None,
    ) -> None:
        self.data_warehouse = data_warehouse or SqlServerDataWarehouse()
        self.schema_name = schema_name or os.getenv("DATA_WAREHOUSE_SCHEMA", "dbo")

    def check_connection(self) -> bool:
        """Return True if SQL Server is reachable."""
        try:
            return self.data_warehouse.fetch_scalar("SELECT 1") == 1
        except Exception:
            return False

    def list_tables(self) -> list[str]:
        """Return user tables from the configured schema."""
        query = """
                SELECT TABLE_NAME
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA = ?
                ORDER BY TABLE_NAME \
                """
        return self.data_warehouse.fetch_column(query, (self.schema_name,))

    def fetch_rows(self, table_name: str, limit: int = 100) -> list[dict[str, Any]]:
        """Fetch rows from a table using a bounded limit."""
        safe_table_name = self._quote_identifier(table_name)
        safe_schema_name = self._quote_identifier(self.schema_name)

        bounded_limit = max(1, min(limit, 1000))

        query = f"""
        SELECT TOP ({bounded_limit}) *
        FROM {safe_schema_name}.{safe_table_name}
        """

        return self.data_warehouse.fetch_rows(query)

    def _quote_identifier(self, identifier: str) -> str:
        """Allow only safe SQL identifiers to prevent injection."""
        if not IDENTIFIER_PATTERN.match(identifier):
            raise ValueError(
                "Invalid SQL identifier. Use letters, numbers, and underscores only."
            )
        return f"[{identifier}]"

    def get_eseal_inventory(self, limit: int = 1000) -> list[dict]:
        query = f"""
        SELECT TOP ({limit})
            [ID_INVENTORY],
            [ROW_ID],
            [CREATED],
            [CREATED_BY],
            [ESEAL_NUMBER],
            [ESEAL_TYPE],
            [ESEAL_STATUS],
            [OWNER_NAME],
            [OWNER_PROVINCE],
            [OWNER_REGION],
            [ESEAL_LAST_LOCATION_TIME],
            [ESEAL_OFFLINE_TIME],
            [LAST_ELECTRICITY_STATUS],
            [LAST_TRIP_ROUTE],
            [LAST_TRIP_DATE],
            [LAST_TRIP_STATUS],
            [LAST_SEALING_USER],
            [LAST_UNSEALING_USER],
            [LAST_LATITUDE],
            [LAST_LONGITUDE],
            [INT_UPDATED_DATE]
        FROM [operation].[eseal_inventory_details]
        ORDER BY [CREATED] DESC
        """
        return self.data_warehouse.fetch_rows(query)

    def get_eseal_stats(self) -> dict:
        query = """
                SELECT
                    COUNT(*) AS total_seals,

                    SUM(CASE
                            WHEN ESEAL_STATUS = 'Em Uso' THEN 1
                            ELSE 0
                        END) AS active,

                    SUM(CASE
                            WHEN ESEAL_STATUS = 'Disponivel' THEN 1
                            ELSE 0
                        END) AS available,

                    SUM(CASE
                            WHEN ESEAL_STATUS = 'Por Substituir' THEN 1
                            ELSE 0
                        END) AS to_change,

                    SUM(CASE
                            WHEN ESEAL_STATUS = 'Em Transporte' THEN 1
                            ELSE 0
                        END) AS compensation,

                    SUM(CASE
                            WHEN ESEAL_STATUS IN (
                                                  'Em Transferencia',
                                                  'Em Manutencao',
                                                  'Danificado'
                                ) THEN 1
                            ELSE 0
                        END) AS maintenance

                FROM [operation].[eseal_inventory_details] \
                """

        result = self.data_warehouse.fetch_rows(query)
        return result[0] if result else {}