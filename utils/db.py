import sqlite3
import threading
from datetime import datetime


# Thread-safe singleton for SQLite database access
class Database:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, db_path: str = "bot.db"):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._conn = sqlite3.connect(
                        db_path,
                        check_same_thread=False,
                        isolation_level=None,
                    )
                    cls._instance._cursor = cls._instance._conn.cursor()
                    cls._instance._init_schema()
        return cls._instance

    def _init_schema(self):
        # create users table
        self._cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                age INTEGER NOT NULL,
                city TEXT NOT NULL,
                date_of_birth TEXT,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        # create questions table
        self._cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                question TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """
        )

    def save_user_profile(
        self,
        user_id: int,
        name: str,
        surname: str,
        age: int,
        city: str,
        date_of_birth: str = None,
        phone: str = None,
    ):
        updated_at = datetime.utcnow().isoformat()
        self._cursor.execute(
            """
            INSERT INTO users (user_id, name, surname, age, city, date_of_birth, phone, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, COALESCE((SELECT created_at FROM users WHERE user_id = ?), CURRENT_TIMESTAMP))
            ON CONFLICT(user_id) DO UPDATE SET
                name=excluded.name,
                surname=excluded.surname,
                age=excluded.age,
                city=excluded.city,
                date_of_birth=excluded.date_of_birth,
                phone=excluded.phone,
                created_at=excluded.created_at
            """,
            (user_id, name, surname, age, city, date_of_birth, phone, user_id),
        )

    def get_user_profile(self, user_id: int):
        self._cursor.execute(
            "SELECT name, surname, age, city, date_of_birth, phone, created_at FROM users WHERE user_id = ?",
            (user_id,),
        )
        row = self._cursor.fetchone()
        if not row:
            return None
        return {
            "name": row[0],
            "surname": row[1],
            "age": row[2],
            "city": row[3],
            "date_of_birth": row[4],
            "phone": row[5],
            "created_at": row[6],
        }

    def save_question(self, user_id: int, question: str):
        self._cursor.execute(
            "INSERT INTO questions (user_id, question) VALUES (?, ?)",
            (user_id, question),
        )

    def get_questions(self, user_id: int):
        self._cursor.execute(
            "SELECT question, created_at FROM questions WHERE user_id = ?", (user_id,)
        )
        return [{"question": r[0], "created_at": r[1]} for r in self._cursor.fetchall()]


# global instance
db = Database()
