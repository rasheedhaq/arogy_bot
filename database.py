import sqlite3
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: str = "arogy.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # User Profiles Table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT,
                        full_name TEXT,
                        age TEXT,
                        sex TEXT,
                        mobile TEXT,
                        address TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Consultations Table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS consultations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        chief_complaint TEXT,
                        duration TEXT,
                        severity TEXT,
                        associated_symptoms TEXT,
                        diagnosis TEXT,
                        recommended_specialty TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    )
                """)
                
                conn.commit()
                logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")

    def save_user(self, user_id: int, user_data: Dict[str, Any]):
        """Save or update user profile"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if user exists
                cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
                exists = cursor.fetchone()
                
                if exists:
                    cursor.execute("""
                        UPDATE users SET
                        username = ?, full_name = ?, age = ?, sex = ?, mobile = ?, address = ?, updated_at = ?
                        WHERE user_id = ?
                    """, (
                        user_data.get('username'),
                        user_data.get('name'),
                        user_data.get('age'),
                        user_data.get('sex'),
                        user_data.get('mobile'),
                        user_data.get('address'),
                        datetime.now(),
                        user_id
                    ))
                else:
                    cursor.execute("""
                        INSERT INTO users (user_id, username, full_name, age, sex, mobile, address)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        user_id,
                        user_data.get('username'),
                        user_data.get('name'),
                        user_data.get('age'),
                        user_data.get('sex'),
                        user_data.get('mobile'),
                        user_data.get('address')
                    ))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to save user {user_id}: {e}")

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve user profile"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
        except Exception as e:
            logger.error(f"Failed to get user {user_id}: {e}")
            return None

    def log_consultation(self, user_id: int, consultation_data: Dict[str, Any]):
        """Log a consultation session"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO consultations (
                        user_id, chief_complaint, duration, severity, 
                        associated_symptoms, recommended_specialty
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    consultation_data.get('chief_complaint'),
                    consultation_data.get('duration'),
                    consultation_data.get('severity'),
                    json.dumps(consultation_data.get('associated_symptoms', [])),
                    consultation_data.get('specialty')
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to log consultation for user {user_id}: {e}")
