import sqlite3
import time
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("LOG_DB_PATH", "logs.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interaction_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            model_type TEXT,
            model_name TEXT,
            prompt TEXT,
            response TEXT,
            latency REAL,
            tokens_used INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def log_interaction(model_type, model_name, prompt, response, latency, tokens=0):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO interaction_logs (model_type, model_name, prompt, response, latency, tokens_used)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (model_type, model_name, prompt, response, latency, tokens))
    conn.commit()
    conn.close()

def get_logs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM interaction_logs ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows
