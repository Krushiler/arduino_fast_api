import sqlite3 as sql
from typing import List


class TemperatureRepository:
    def __init__(self, filename: str):
        self._conn = sql.connect(filename)

    async def add_temperature(self, temperature: float, location: str | None):
        cur = self._conn.cursor()
        cur.execute(
            "INSERT INTO temperatures (value, location) VALUES (?, ?)",
            (temperature, location),
        )
        self._conn.commit()

    async def get_temperatures(self, location: str) -> List[float]:
        cur = self._conn.cursor()
        cur.execute("SELECT value FROM temperatures WHERE location = ?", (location,))
        return [row[0] for row in cur.fetchall()]

    def close(self):
        self._conn.close()
