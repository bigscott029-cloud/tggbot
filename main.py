#!/usr/bin/env python3
import os
from threading import Thread
from flask import Flask
from telegram.ext import Application

# Keep-alive for Render / Railway
app = Flask(__name__)
@app.route('/')
def home():
    return "Money forever Bot is alive!"

def keep_alive():
    Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))).start()

if __name__ == "__main__":
    keep_alive()
    
    from config.settings import BOT_TOKEN
    from handlers import register_all_handlers
    from jobs.scheduler import setup_jobs

    application = Application.builder().token(BOT_TOKEN).build()
    register_all_handlers(application)
    setup_jobs(application)

    print("Auto Bot (Modular + Coach System) Started!")
    application.run_polling(allowed_updates=["message", "callback_query"])
