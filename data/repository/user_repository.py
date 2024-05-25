import sqlite3 as sql


class UserRepository:
    def __init__(self, filename: str):
        self._conn = sql.connect(filename, check_same_thread=False)

    async def register(self, login: str, password: str) -> int | None:
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM users WHERE login = ?", (login,))
        users = cur.fetchall()
        if users is None or len(users) == 0:
            cur.execute(
                "INSERT INTO users (login, password) VALUES (?, ?)",
                (login, password),
            )
            self._conn.commit()
            return cur.lastrowid
        if users[0][2] == password:
            return users[0][0]
        return None

    def close(self):
        self._conn.close()
