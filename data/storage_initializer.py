import sqlite3 as sql


def initialize_storage(filename: str):
    conn = sql.connect(filename, check_same_thread=False)

    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS temperatures (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    value REAL NOT NULL,
                    location TEXT
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS led_configurations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    value TEXT NOT NULL,
                    user_id INTEGER
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS active_led_configurations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    config_id INTEGER,
                    device_id TEXT NOT NULL
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login TEXT,
                    password TEXT
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS userDevices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    device_id TEXT
    )''')

    conn.commit()
    cur.close()
    conn.close()
