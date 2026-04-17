import os
from contextlib import contextmanager
from typing import Generator

import pyodbc

pyodbc.pooling = True  # enable pooling globally


def build_connection_string() -> str:
    trust = os.getenv("DB_TRUST_SERVER_CERTIFICATE", "true").lower() in ("1", "true", "yes")

    return (
        f"DRIVER={{{os.getenv('DB_DRIVER')}}};"
        f"SERVER={os.getenv('DB_HOST')},{os.getenv('DB_PORT')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_USER')};"
        f"PWD={os.getenv('DB_PASSWORD')};"
        f"TrustServerCertificate={'yes' if trust else 'no'};"
    )


def create_connection() -> pyodbc.Connection:
    return pyodbc.connect(build_connection_string(), timeout=10)


@contextmanager
def get_connection() -> Generator[pyodbc.Connection, None, None]:
    connection = create_connection()
    try:
        yield connection
    finally:
        connection.close()