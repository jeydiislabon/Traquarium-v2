"""
data_model.py
-------------
Data persistence layer using SQLite (stdlib sqlite3).

Schema — readings table:
    id          INTEGER PRIMARY KEY AUTOINCREMENT
    timestamp   TEXT    NOT NULL
    tank_name   TEXT    NOT NULL
    tan         REAL    NOT NULL   -- Total Ammonia Nitrogen (mg/L)
    ph          REAL    NOT NULL
    temperature REAL    NOT NULL
    nh3         REAL    NOT NULL   -- Computed un-ionized NH3 (mg/L)
    toxicity    TEXT    NOT NULL   -- Safe / Caution / Critical Toxic
    kh          REAL               -- Carbonate Hardness (optional, logged only)
    gh          REAL               -- General Hardness   (optional, logged only)

Per-user database: users/<username>/readings.db
"""

import sqlite3
import os
from datetime import datetime


# ---------------------------------------------------------------------------
# Domain data class
# ---------------------------------------------------------------------------

class WaterReading:
    """Represents one logged water quality reading."""

    def __init__(self, tank_name: str, tan: float, ph: float,
                 temperature: float, nh3: float, toxicity: str,
                 kh: float = None, gh: float = None,
                 timestamp: str = None, reading_id: int = None):
        self.id          = reading_id
        self.timestamp   = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M")
        self.tank_name   = tank_name
        self.tan         = tan          # Total Ammonia Nitrogen (mg/L)
        self.ph          = ph
        self.temperature = temperature
        self.nh3         = nh3          # Computed NH3 (mg/L)
        self.toxicity    = toxicity
        self.kh          = kh           # Carbonate Hardness (optional)
        self.gh          = gh           # General Hardness   (optional)

    def to_dict(self):
        return {
            "id":          self.id,
            "timestamp":   self.timestamp,
            "name":        self.tank_name,   # kept as "name" for UI compatibility
            "tank_name":   self.tank_name,
            "tan":         self.tan,
            "pH":          self.ph,
            "ph":          self.ph,
            "temperature": self.temperature,
            "nh3":         self.nh3,
            "toxicity":    self.toxicity,
            "kh":          self.kh,
            "gh":          self.gh,
        }


# ---------------------------------------------------------------------------
# Manager
# ---------------------------------------------------------------------------

class ReadingManager:
    """Handles all SQLite CRUD operations for a single user's readings."""

    _CREATE_TABLE = """
        CREATE TABLE IF NOT EXISTS readings (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT    NOT NULL,
            tank_name   TEXT    NOT NULL,
            tan         REAL    NOT NULL,
            ph          REAL    NOT NULL,
            temperature REAL    NOT NULL,
            nh3         REAL    NOT NULL,
            toxicity    TEXT    NOT NULL,
            kh          REAL,
            gh          REAL
        )
    """

    def __init__(self, username: str = None):
        self.username  = username
        self.db_path   = None
        self._readings = []   # in-memory cache

        if username:
            base_dir  = os.path.join(os.getcwd(), "users")
            user_dir  = os.path.join(base_dir, username)
            os.makedirs(user_dir, exist_ok=True)
            self.db_path = os.path.join(user_dir, "readings.db")
            self._init_db()
            self.load_readings()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _connect(self):
        """Return a new SQLite connection with WAL mode for safety."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        return conn

    def _init_db(self):
        """Create the readings table if it does not exist."""
        with self._connect() as conn:
            conn.execute(self._CREATE_TABLE)
            conn.commit()

    # ------------------------------------------------------------------
    # Public CRUD API
    # ------------------------------------------------------------------

    def add_reading(self, reading: WaterReading):
        """Insert a new reading and refresh the in-memory cache."""
        sql = """
            INSERT INTO readings
                (timestamp, tank_name, tan, ph, temperature, nh3, toxicity, kh, gh)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        with self._connect() as conn:
            conn.execute(sql, (
                reading.timestamp,
                reading.tank_name,
                reading.tan,
                reading.ph,
                reading.temperature,
                reading.nh3,
                reading.toxicity,
                reading.kh,
                reading.gh,
            ))
            conn.commit()
        self.load_readings()

    def update_reading(self, reading_id: int, tank_name: str, tan: float,
                       ph: float, temperature: float, nh3: float,
                       toxicity: str, kh: float = None, gh: float = None):
        """Update an existing reading by its primary key."""
        sql = """
            UPDATE readings
            SET tank_name=?, tan=?, ph=?, temperature=?, nh3=?, toxicity=?,
                kh=?, gh=?
            WHERE id=?
        """
        with self._connect() as conn:
            conn.execute(sql, (tank_name, tan, ph, temperature, nh3,
                               toxicity, kh, gh, reading_id))
            conn.commit()
        self.load_readings()

    def delete_reading(self, reading_id: int):
        """Delete a reading by its primary key."""
        with self._connect() as conn:
            conn.execute("DELETE FROM readings WHERE id=?", (reading_id,))
            conn.commit()
        self.load_readings()

    def get_all(self):
        """Return all readings as a list of dicts (for UI consumption)."""
        return [r.to_dict() for r in self._readings]

    def load_readings(self):
        """Reload the in-memory cache from the database."""
        if not self.db_path:
            return
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM readings ORDER BY id ASC"
            ).fetchall()
        self._readings = [
            WaterReading(
                tank_name  = row["tank_name"],
                tan        = row["tan"],
                ph         = row["ph"],
                temperature= row["temperature"],
                nh3        = row["nh3"],
                toxicity   = row["toxicity"],
                kh         = row["kh"],
                gh         = row["gh"],
                timestamp  = row["timestamp"],
                reading_id = row["id"],
            )
            for row in rows
        ]

    def clear_readings(self):
        """Delete all readings for this user."""
        with self._connect() as conn:
            conn.execute("DELETE FROM readings")
            conn.commit()
        self._readings.clear()

    # Kept for backward compatibility with history_page save logic
    @property
    def file_path(self):
        """Legacy property — returns db_path so old code referencing
        file_path does not break immediately."""
        return self.db_path
