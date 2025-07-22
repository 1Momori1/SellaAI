import time
import random
import string
import logging
from config import LOG_PATH

# Форматирование времени в человекочитаемый вид
def format_time(ts: int) -> str:
    return time.strftime('%d.%m.%Y %H:%M', time.localtime(ts))

# Генерация короткого id
def gen_id(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Ограничение длины текста
def limit_text(text: str, max_len=2048) -> str:
    return text if len(text) <= max_len else text[:max_len] + '...'

# Логирование
logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def log(msg: str):
    logging.info(msg) 