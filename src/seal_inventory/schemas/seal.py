"""API schemas for SQL Server-backed responses."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from typing import Optional
from datetime import datetime



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

class ESealInventory(BaseModel):
    ID_INVENTORY: int
    ROW_ID: str
    CREATED: Optional[datetime]
    CREATED_BY: Optional[str]
    ESEAL_NUMBER: Optional[str]
    ESEAL_TYPE: Optional[str]
    ESEAL_STATUS: Optional[str]
    OWNER_NAME: Optional[str]
    OWNER_PROVINCE: Optional[str]
    OWNER_REGION: Optional[str]
    ESEAL_LAST_LOCATION_TIME: Optional[datetime]
    ESEAL_OFFLINE_TIME: Optional[datetime]
    LAST_ELECTRICITY_STATUS: Optional[str]
    LAST_TRIP_ROUTE: Optional[str]
    LAST_TRIP_DATE: Optional[datetime]
    LAST_TRIP_STATUS: Optional[str]
    LAST_SEALING_USER: Optional[str]
    LAST_UNSEALING_USER: Optional[str]
    LAST_LATITUDE: Optional[float]
    LAST_LONGITUDE: Optional[float]
    INT_UPDATED_DATE: Optional[datetime]


class ESealInventoryResponse(BaseModel):
    count: int
    data: list[ESealInventory]

class ESealStatsResponse(BaseModel):
    total_seals: int
    active: int
    available: int
    to_change: int
    compensation: int
    maintenance: int