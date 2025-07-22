import aiosqlite
import asyncio
from typing import List, Optional, Tuple

DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    remind_at INTEGER NOT NULL,
    repeat_interval INTEGER DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS user_memory (
    user_id INTEGER PRIMARY KEY,
    data TEXT
);

CREATE TABLE IF NOT EXISTS state (
    key TEXT PRIMARY KEY,
    value TEXT
);
"""

async def init_db(db_path: str):
    async with aiosqlite.connect(db_path) as db:
        await db.executescript(DB_SCHEMA)
        await db.commit()

# --- Напоминания ---
async def add_reminder(db_path: str, user_id: int, text: str, remind_at: int, repeat_interval: Optional[int]=None):
    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            "INSERT INTO reminders (user_id, text, remind_at, repeat_interval) VALUES (?, ?, ?, ?)",
            (user_id, text, remind_at, repeat_interval)
        )
        await db.commit()

async def get_due_reminders(db_path: str, now: int) -> List[Tuple]:
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT id, user_id, text, remind_at, repeat_interval FROM reminders WHERE remind_at <= ?", (now,)) as cursor:
            rows = await cursor.fetchall()
            return [tuple(row) for row in rows]

async def delete_reminder(db_path: str, reminder_id: int):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
        await db.commit()

async def update_reminder_time(db_path: str, reminder_id: int, new_time: int):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("UPDATE reminders SET remind_at = ? WHERE id = ?", (new_time, reminder_id))
        await db.commit()

# --- User memory ---
async def set_user_memory(db_path: str, user_id: int, data: str):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("REPLACE INTO user_memory (user_id, data) VALUES (?, ?)", (user_id, data))
        await db.commit()

async def get_user_memory(db_path: str, user_id: int) -> Optional[str]:
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT data FROM user_memory WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None

# --- State ---
async def set_state(db_path: str, key: str, value: str):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("REPLACE INTO state (key, value) VALUES (?, ?)", (key, value))
        await db.commit()

async def get_state(db_path: str, key: str) -> Optional[str]:
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT value FROM state WHERE key = ?", (key,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None 