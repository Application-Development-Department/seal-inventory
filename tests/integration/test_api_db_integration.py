"""Integration-style checks for repository guardrails."""

from unittest import TestCase

from seal_inventory.repositories.seal_repository import SealRepository


class SealRepositoryTests(TestCase):
    """Verify repository input validation that does not require a live DB."""

    def test_quote_identifier_rejects_invalid_name(self) -> None:
        repository = SealRepository()

        with self.assertRaises(ValueError):
            repository._quote_identifier("dbo.Seals")

    def test_quote_identifier_accepts_simple_name(self) -> None:
        repository = SealRepository()

        self.assertEqual(repository._quote_identifier("Seals"), "[Seals]")
