"""FastAPI application bootstrap."""

from __future__ import annotations

import os

from fastapi import FastAPI

from seal_inventory.api.routes import router, v1_router


def validate_env() -> None:
    """Validate required database settings before startup."""

    required = [
        "DB_DRIVER",
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
    ]

    missing = [var for var in required if not os.getenv(var)]
    if missing:
        raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")


validate_env()

app = FastAPI(
    title=os.getenv("APP_NAME", "Seal Inventory API"),
    version="0.1.0",
    description="API service for retrieving existing records from Microsoft SQL Server.",
)

app.include_router(router)
app.include_router(v1_router)
