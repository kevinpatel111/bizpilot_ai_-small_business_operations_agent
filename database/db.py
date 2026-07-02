import sqlite3
import os
import datetime
from typing import List, Dict, Any, Optional
from utils.logger import logger

DB_FILE = os.getenv("DB_PATH", "database/bizpilot.db")

def get_db_connection():
    """Establish connection to SQLite database."""
    # Ensure folder exists
    db_dir = os.path.dirname(DB_FILE)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables."""
    logger.info("Initializing database...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. File Uploads Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS file_uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_type TEXT UNIQUE,
            filename TEXT,
            filepath TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 2. Chat History Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 3. Settings Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully.")

# File upload methods
def register_file(file_type: str, filename: str, filepath: str):
    """Register or update an uploaded file in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO file_uploads (file_type, filename, filepath, uploaded_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(file_type) DO UPDATE SET
                filename=excluded.filename,
                filepath=excluded.filepath,
                uploaded_at=CURRENT_TIMESTAMP
        """, (file_type, filename, filepath))
        conn.commit()
    except Exception as e:
        logger.error(f"Error registering file {filename}: {e}")
    finally:
        conn.close()

def get_registered_files() -> Dict[str, Dict[str, Any]]:
    """Get all currently registered files."""
    conn = get_db_connection()
    cursor = conn.cursor()
    files = {}
    try:
        cursor.execute("SELECT file_type, filename, filepath, uploaded_at FROM file_uploads")
        rows = cursor.fetchall()
        for row in rows:
            files[row["file_type"]] = {
                "filename": row["filename"],
                "filepath": row["filepath"],
                "uploaded_at": row["uploaded_at"]
            }
    except Exception as e:
        logger.error(f"Error fetching registered files: {e}")
    finally:
        conn.close()
    return files

def delete_registered_file(file_type: str):
    """Delete a registered file reference."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM file_uploads WHERE file_type=?", (file_type,))
        conn.commit()
    except Exception as e:
        logger.error(f"Error deleting file record {file_type}: {e}")
    finally:
        conn.close()

# Chat History methods
def add_chat_message(session_id: str, role: str, content: str):
    """Add a message to the session's chat history."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO chat_history (session_id, role, content)
            VALUES (?, ?, ?)
        """, (session_id, role, content))
        conn.commit()
    except Exception as e:
        logger.error(f"Error saving chat message: {e}")
    finally:
        conn.close()

def get_chat_history(session_id: str) -> List[Dict[str, str]]:
    """Retrieve chat history for a session."""
    conn = get_db_connection()
    cursor = conn.cursor()
    history = []
    try:
        cursor.execute("""
            SELECT role, content FROM chat_history 
            WHERE session_id = ? 
            ORDER BY timestamp ASC
        """, (session_id,))
        rows = cursor.fetchall()
        for row in rows:
            history.append({"role": row["role"], "content": row["content"]})
    except Exception as e:
        logger.error(f"Error retrieving chat history: {e}")
    finally:
        conn.close()
    return history

def clear_chat_history(session_id: str):
    """Clear chat history for a session."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM chat_history WHERE session_id = ?", (session_id,))
        conn.commit()
    except Exception as e:
        logger.error(f"Error clearing chat history: {e}")
    finally:
        conn.close()

# Settings methods
def set_setting(key: str, value: str):
    """Set a setting value."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO settings (key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value=excluded.value
        """, (key, value))
        conn.commit()
    except Exception as e:
        logger.error(f"Error saving setting {key}: {e}")
    finally:
        conn.close()

def get_setting(key: str, default: Optional[str] = None) -> Optional[str]:
    """Retrieve a setting value."""
    conn = get_db_connection()
    cursor = conn.cursor()
    val = default
    try:
        cursor.execute("SELECT value FROM settings WHERE key=?", (key,))
        row = cursor.fetchone()
        if row:
            val = row["value"]
    except Exception as e:
        logger.error(f"Error retrieving setting {key}: {e}")
    finally:
        conn.close()
    return val

# Automatically run initialization on import
init_db()
