from typing import Any, Iterable
from seal_inventory.db.connection import get_connection


class SqlServerDataWarehouse:

    def fetch_scalar(self, query: str, parameters: Iterable[Any] = ()) -> Any:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, *tuple(parameters))
            row = cursor.fetchone()
            return None if row is None else row[0]

    def fetch_rows(self, query: str, parameters: Iterable[Any] = ()) -> list[dict]:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, *tuple(parameters))
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]