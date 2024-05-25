import sqlite3 as sql


class DeviceRepository:
    def __init__(self, filename: str):
        self._conn = sql.connect(filename, check_same_thread=False)

    async def add_device(self, user_id: int, device_id: str):
        cur = self._conn.cursor()
        cur.execute(
            "INSERT INTO userDevices (user_id, device_id) VALUES (?, ?)",
            (user_id, device_id),
        )
        self._conn.commit()

    def close(self):
        self._conn.close()
