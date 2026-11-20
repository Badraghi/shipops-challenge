"""Small PostgreSQL-backed store. The schema is provisioned in Phase 1's DB deploy."""

import os
from typing import Protocol


class ItemStore(Protocol):
    def ping(self) -> None: ...

    def create_item(self, name: str) -> tuple[int, str]: ...

    def get_item(self, item_id: int) -> tuple[int, str] | None: ...


class PostgresItemStore:
    def __init__(self, dsn: str) -> None:
        self.dsn = dsn

    def _connect(self):
        if not self.dsn:
            raise RuntimeError("DATABASE_URL is not configured")
        import psycopg
        return psycopg.connect(self.dsn, connect_timeout=3)

    def ping(self) -> None:
        with self._connect() as connection:
            connection.execute("SELECT 1").fetchone()

    def create_item(self, name: str) -> tuple[int, str]:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO items (name) VALUES (%s) RETURNING id, name",
                    (name,),
                )
                item = cursor.fetchone()
                assert item is not None
                return int(item[0]), str(item[1])

    def get_item(self, item_id: int) -> tuple[int, str] | None:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name FROM items WHERE id = %s", (item_id,))
                result = cursor.fetchone()
                if result is None:
                    return None
                return int(result[0]), str(result[1])


def get_store() -> ItemStore:
    return PostgresItemStore(os.getenv("DATABASE_URL", ""))
