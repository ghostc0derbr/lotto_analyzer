import sqlite3
import json

DB_FILE = "feedback.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS liked_properties (
            property_key TEXT PRIMARY KEY,
            like_count INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def record_feedback(properties_dict):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    for key, value in properties_dict.items():
        property_key = f"{key}_{value}"
        
        cursor.execute("SELECT like_count FROM liked_properties WHERE property_key = ?", (property_key,))
        result = cursor.fetchone()
        
        if result:
            new_count = result[0] + 1
            cursor.execute("UPDATE liked_properties SET like_count = ? WHERE property_key = ?", (new_count, property_key))
        else:
            cursor.execute("INSERT INTO liked_properties (property_key, like_count) VALUES (?, 1)", (property_key,))
            
    conn.commit()
    conn.close()
    print(f"Feedback registrado no banco de dados para: {properties_dict}")

def get_feedback_weights():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT property_key, like_count FROM liked_properties")
        rows = cursor.fetchall()
        conn.close()
        return dict(rows)
    except sqlite3.OperationalError:
        return {}