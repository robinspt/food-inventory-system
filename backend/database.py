import sqlite3
import os

DATABASE = 'site.db'
SCHEMA_FILE = 'schema.md' # This is just for reference, we'll hardcode SQL for simplicity

def init_db():
    # Ensure the database file is in the backend directory
    db_path = os.path.join(os.path.dirname(__file__), DATABASE)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
        )
    """)

    # Create food_items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS food_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            production_date DATE NOT NULL,
            expiry_period_value INTEGER NOT NULL,
            expiry_period_unit TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity >= 0),
            storage_location TEXT,
            expiration_date DATE NOT NULL,
            status TEXT NOT NULL DEFAULT 'active',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print(f"Database '{DATABASE}' initialized successfully with users and food_items tables.")

if __name__ == '__main__':
    init_db() 