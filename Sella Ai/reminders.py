from db import add_reminder, delete_reminder, get_due_reminders, update_reminder_time
from utils import format_time
import time

async def add_new_reminder(db_path, user_id, text, remind_at, repeat_interval=None):
    await add_reminder(db_path, user_id, text, remind_at, repeat_interval)
    return f"Напоминание добавлено на {format_time(remind_at)}" + (f", повтор каждые {repeat_interval//60} мин." if repeat_interval else "")

async def get_and_format_due_reminders(db_path, now):
    reminders = await get_due_reminders(db_path, now)
    result = []
    for r in reminders:
        rid, uid, text, remind_at, repeat = r
        result.append(f"{text} (в {format_time(remind_at)})")
    return result

async def remove_reminder(db_path, reminder_id):
    await delete_reminder(db_path, reminder_id)
    return "Напоминание удалено."

async def snooze_reminder(db_path, reminder_id, minutes):
    new_time = int(time.time()) + minutes*60
    await update_reminder_time(db_path, reminder_id, new_time)
    return f"Отложено на {minutes} минут." 