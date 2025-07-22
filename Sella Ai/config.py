import os

API_ID = 24585822
API_HASH = 'd58856a266193af33447eae19acf2f9f'
BOT_TOKEN = '7684724135:AAEWhZ1vf9F5yFh__jKMA8ljnQ0ReojAEIU'
MODEL_PATH = os.getenv('MODEL_PATH', 'models/mistral-7b-instruct-v0.2.Q4_K_M.gguf')
DB_PATH = os.getenv('DB_PATH', 'data/bot.db')
LOG_PATH = os.getenv('LOG_PATH', 'data/bot.log')
USER_WHITELIST = ['824312416']  # id разрешённых пользователей 