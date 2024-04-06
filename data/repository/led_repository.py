import sqlite3 as sql
from typing import List

from data.mqtt.led_mqtt import LedMqtt
from domain.led_configuration import LedConfiguration


class LedRepository:
    def __init__(self, filename: str, led_mqtt: LedMqtt):
        self._led_mqtt = led_mqtt
        self._conn = sql.connect(filename, check_same_thread=False)

    async def add_config(self, value: str) -> LedConfiguration:
        cur = self._conn.cursor()
        cur.execute("INSERT INTO led_configurations (value) VALUES (?)", (value,))
        self._conn.commit()
        return LedConfiguration(id=cur.lastrowid, value=value)

    async def get_active_config(self, device_id: int) -> LedConfiguration:
        cur = self._conn.cursor()
        cur.execute("SELECT config_id FROM active_led_configurations WHERE device_id = ?", str(device_id), )
        config_id = cur.fetchone()[0]
        print(config_id)
        config = await self.get_config_by_id(config_id)
        return config

    async def set_active_config(self, config_id: int, device_id: int):
        cur = self._conn.cursor()
        cur.execute(
            "INSERT INTO active_led_configurations (config_id, device_id) VALUES (?, ?)",
            (str(config_id), str(device_id)),
        )
        self._conn.commit()
        config = await self.get_active_config(device_id)
        self._led_mqtt.publish_led_config(config.value, device_id)

    async def get_config_by_id(self, config_id: int) -> LedConfiguration:
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM led_configurations WHERE id = (?)", str(config_id), )
        config = cur.fetchone()
        return LedConfiguration(id=config[0], value=config[1])

    async def get_configs(self) -> List[LedConfiguration]:
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM led_configurations")
        return [LedConfiguration(id=row[0], value=row[1]) for row in cur.fetchall()]

    def close(self):
        self._conn.close()
