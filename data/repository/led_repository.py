import sqlite3 as sql
from typing import List

from domain.led_configuration import LedConfiguration


class LedRepository:
    def __init__(self, filename: str):
        self._conn = sql.connect(filename, check_same_thread=False)

    async def add_config(self, value: str) -> LedConfiguration:
        cur = self._conn.cursor()
        cur.execute("INSERT INTO led_configurations (value) VALUES (?)", (value,))
        self._conn.commit()
        return LedConfiguration(id=cur.lastrowid, value=value)

    async def get_active_config(self, device_id: int) -> LedConfiguration:
        cur = self._conn.cursor()
        cur.execute("SELECT config_id FROM active_led_configurations WHERE device_id = ?", device_id,)
        config_id = cur.fetchone()
        cur.execute("SELECT * FROM led_configurations WHERE id = (?)", config_id,)
        config = cur.fetchone()
        return LedConfiguration(id=config[0], value=config[1])

    async def set_active_config(self, config_id: int, device_id: int):
        cur = self._conn.cursor()
        cur.execute(
            "INSERT INTO active_led_configurations (config_id, device_id) VALUES (?, ?)",
            (config_id, device_id),
        )
        self._conn.commit()

    async def get_configs(self) -> List[LedConfiguration]:
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM led_configurations")
        return [LedConfiguration(id=row[0], value=row[1]) for row in cur.fetchall()]

    def close(self):
        self._conn.close()
