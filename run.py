from terminal import Terminal
from telegram_bot import TelegramBot
from database import Database
from gpt_client import GPTClient
from setup import TELEGRAM_API, OPENAI_API, DB_NAME
import threading

if __name__ == '__main__':
    terminal = Terminal()

    db = Database(DB_NAME, terminal)
    db.connect()
    db.create_history_table()

    terminal_thread = threading.Thread(target=terminal.run_admin_terminal, args=(terminal, db))
    terminal_thread.start()

    gpt = GPTClient(OPENAI_API, db, terminal)

    bot = TelegramBot(TELEGRAM_API, gpt, db, terminal)
    bot.start_bot()