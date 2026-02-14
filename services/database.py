import sqlite3

class Database:
    def __init__(self, db_name="expense.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            category TEXT,
            type TEXT,
            date TEXT
        )
        """)
        self.conn.commit()

    def add_transaction(self, t):
        self.cursor.execute("""
            INSERT INTO transactions (user_id, amount, category, type, date)
            VALUES (?, ?, ?, ?, ?)
        """, (t.user_id, t.amount, t.category, t.type, t.date))
        self.conn.commit()
