import os
import sqlite3
import uuid
from pathlib import Path

DB_FILE = "sql_app.db"
MIGRATIONS_DIR = "sql_migrations"

def run_migrations():
    print(f"Checking migrations in {MIGRATIONS_DIR}...")
    
    # 1. Connect
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Enable foreign keys for SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 2. Ensure migrations table exists (Bootstrapping)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS t_migrations (
        id CHAR(36) PRIMARY KEY,
        filename VARCHAR NOT NULL UNIQUE,
        applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    
    # 3. Get applied migrations
    cursor.execute("SELECT filename FROM t_migrations")
    applied = set(row[0] for row in cursor.fetchall())
    
    # 4. Get all sql files
    files = sorted([f for f in os.listdir(MIGRATIONS_DIR) if f.endswith(".sql")])
    
    for filename in files:
        if filename in applied:
            print(f"Skipping {filename} (Already applied)")
            continue
            
        print(f"Applying {filename}...")
        file_path = os.path.join(MIGRATIONS_DIR, filename)
        
        with open(file_path, "r") as f:
            sql_script = f.read()
            
        try:
            cursor.executescript(sql_script)
            
            # Record success
            migration_id = str(uuid.uuid4())
            cursor.execute("INSERT INTO t_migrations (id, filename) VALUES (?, ?)", (migration_id, filename))
            conn.commit()
            print(f"Successfully applied {filename}")
            
        except Exception as e:
            print(f"FAILED to apply {filename}: {e}")
            conn.rollback()
            break
            
    conn.close()
    print("Migration check complete.")

if __name__ == "__main__":
    run_migrations()
