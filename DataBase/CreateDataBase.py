import sqlite3


def create_conn():
    """
    This function creates a connection to the SQLite database and returns the connection object.
    """
    conn = sqlite3.connect("../data.db")
    return conn


conn = create_conn()
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        chatID INT,
        login TEXT,
        pass TEXT,
        token TEXT
    )
""")

conn.commit()
