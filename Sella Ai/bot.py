import asyncio
import time
from telethon import TelegramClient, events, Button
from config import API_ID, API_HASH, DB_PATH, USER_WHITELIST, BOT_TOKEN
from db import init_db, set_state, get_state
from reminders import add_new_reminder, get_and_format_due_reminders, remove_reminder, snooze_reminder
from summary import make_summary
from search import google_search
from utils import log

# --- Глобальные переменные ---
NEW_MESSAGES = {}  # {chat_id: [ {sender, text, timestamp} ] }

# --- Проверка пользователя ---
def is_allowed(user_id):
    return not USER_WHITELIST or str(user_id) in USER_WHITELIST

async def main():
    await init_db(DB_PATH)
    client = TelegramClient('bot_session', API_ID, API_HASH)

    @client.on(events.NewMessage(incoming=True))
    async def handler(event):
        if event.is_private:
            user_id = event.sender_id
            if not is_allowed(user_id):
                await event.respond('Нет доступа.')
                return
            if event.text.startswith('/start'):
                await event.respond('Привет! Я ИИ-бот. Используй меню или команды.')
            elif event.text.startswith('/help'):
                await event.respond('Доступные команды:\n/summary — сводка по группам\n/search <запрос> — поиск в интернете\n/remember <текст> <через сколько минут> [повтор в минутах] — напоминание')
            elif event.text.startswith('/search'):
                q = event.text[7:].strip()
                if not q:
                    await event.respond('Укажите запрос для поиска.')
                else:
                    links = await google_search(q)
                    await event.respond('\n'.join(links))
            elif event.text.startswith('/summary'):
                summaries = []
                for chat_id, msgs in NEW_MESSAGES.items():
                    if msgs:
                        summ = await make_summary(msgs)
                        summaries.append(f'Группа {chat_id}:\n{summ}')
                        NEW_MESSAGES[chat_id] = []
                if summaries:
                    await event.respond('\n\n'.join(summaries))
                else:
                    await event.respond('Нет новых сообщений в группах.')
            elif event.text.startswith('/remember'):
                parts = event.text.split(maxsplit=3)
                if len(parts) < 3:
                    await event.respond('Формат: /remember <текст> <минут> [повтор]')
                else:
                    text = parts[1]
                    try:
                        mins = int(parts[2])
                        repeat = int(parts[3]) if len(parts) > 3 else None
                        remind_at = int(time.time()) + mins*60
                        msg = await add_new_reminder(DB_PATH, user_id, text, remind_at, repeat*60 if repeat else None)
                        await event.respond(msg)
                    except Exception as e:
                        await event.respond('Ошибка: ' + str(e))
            else:
                await event.respond('Неизвестная команда. Используйте /help.')
        elif event.is_group:
            chat_id = event.chat_id
            if chat_id not in NEW_MESSAGES:
                NEW_MESSAGES[chat_id] = []
            NEW_MESSAGES[chat_id].append({
                'sender': (await event.get_sender()).first_name,
                'text': event.text,
                'timestamp': event.date.timestamp()
            })

    # --- Inline-кнопки ---
    @client.on(events.CallbackQuery)
    async def callback(event):
        data = event.data.decode()
        if data.startswith('rem_del_'):
            rid = int(data[8:])
            await remove_reminder(DB_PATH, rid)
            await event.edit('Напоминание удалено.')
        elif data.startswith('rem_snooze_'):
            rid = int(data[11:])
            await snooze_reminder(DB_PATH, rid, 10)
            await event.edit('Отложено на 10 минут.')

    # --- Фоновая задача: напоминания ---
    async def reminder_loop():
        while True:
            now = int(time.time())
            due = await get_and_format_due_reminders(DB_PATH, now)
            for r in due:
                # Здесь можно отправить напоминание пользователю (реализовать через client.send_message)
                log(f'Напоминание: {r}')
            await asyncio.sleep(60)

    # --- Запуск ---
    await client.start(bot_token=BOT_TOKEN)
    asyncio.create_task(reminder_loop())
    print('Бот запущен.')
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main()) 