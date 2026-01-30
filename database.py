import sqlite3

def create_db():
    conn = sqlite3.connect("emergency.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emergency_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            speed INTEGER,
            door_locked BOOLEAN,
            latitude REAL,
            longitude REAL,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()



def insert_log(timestamp, speed, door_locked, latitude, longitude, message):
    conn = sqlite3.connect("emergency.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO emergency_logs (timestamp, speed, door_locked, latitude, longitude, message)
VALUES (?, ?, ?, ?, ?, ?)
    """, (timestamp, speed, door_locked, message))

    conn.commit()
    conn.close()


def fetch_logs():
    conn = sqlite3.connect("emergency.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emergency_logs")
    logs = cursor.fetchall()

    conn.close()
    return logs
