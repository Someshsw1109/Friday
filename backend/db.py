import csv
import sqlite3
from pathlib import Path

try:
    db_path = Path("jarvis.db")
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
        cursor.execute(query)
        query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
        cursor.execute(query)
        query = "CREATE TABLE IF NOT EXISTS contacts(id integer primary key, name VARCHAR(100), phone VARCHAR(20))"
        cursor.execute(query)
        conn.commit()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error creating tables: {str(e)}")
        conn.rollback()
except Exception as e:
    print(f"Error connecting to database: {str(e)}")
    conn = None
    cursor = None