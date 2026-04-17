"""Unit tests for service behavior."""

from unittest import TestCase
from unittest.mock import Mock

from seal_inventory.services.seal_service import SealService


class SealServiceTests(TestCase):
    """Verify service behavior independently from the database."""

    def test_get_tables_delegates_to_repository(self) -> None:
        repository = Mock()
        repository.list_tables.return_value = ["Seals", "Inventory"]

        service = SealService(repository=repository)
        tables = service.get_tables()

        self.assertEqual(tables, ["Seals", "Inventory"])
        repository.list_tables.assert_called_once_with()

    def test_get_table_rows_delegates_to_repository(self) -> None:
        repository = Mock()
        repository.fetch_rows.return_value = [{"Id": 1, "SealCode": "A-100"}]

        service = SealService(repository=repository)
        rows = service.get_table_rows(table_name="Seals", limit=10)

        self.assertEqual(rows, [{"Id": 1, "SealCode": "A-100"}])
        repository.fetch_rows.assert_called_once_with(table_name="Seals", limit=10)
