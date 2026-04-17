"""API schemas for SQL Server-backed responses."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response schema for health endpoints."""

    status: str
    detail: str


class TableListResponse(BaseModel):
    """Response schema for available database tables."""

    schema_name: str = Field(alias="schema")
    tables: list[str]


class TableRowsResponse(BaseModel):
    """Response schema for generic table row reads."""

    table_name: str
    row_count: int
    rows: list[dict[str, Any]]
