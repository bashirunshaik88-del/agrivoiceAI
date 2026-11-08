import sqlite3
import os

DB_PATH = os.path.join("database", "agri_history.db")

def initialize_database():
    """Creates the database and table if it doesn't exist."""
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS query_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            language TEXT,
            crop TEXT,
            symptom TEXT,
            original_text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_query(language, crop, symptom, original_text):
    """Saves a farmer's query to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO query_history (language, crop, symptom, original_text)
        VALUES (?, ?, ?, ?)
    ''', (language, crop, symptom, original_text))
    conn.commit()
    conn.close()

def get_all_history(limit=5):
    """Retrieves the most recent past queries for display."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT timestamp, language, crop, symptom, original_text 
        FROM query_history 
        ORDER BY id DESC LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows