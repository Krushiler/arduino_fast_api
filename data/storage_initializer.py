import sqlite3 as sql


def initialize_storage(filename: str):
    conn = sql.connect(filename, check_same_thread=False)

    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS temperatures (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    value REAL NOT NULL,
                    location TEXT
                )''')

    conn.commit()
    cur.close()
    conn.close()
