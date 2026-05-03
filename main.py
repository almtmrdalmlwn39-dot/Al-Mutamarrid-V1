import os
import glob
import importlib
from telethon import TelegramClient
from flask import Flask
from threading import Thread

# --- إعدادات السيرفر لإبقاء البوت حياً ---
app = Flask('')
@app.route('/')
def home(): return "I am alive"

def run(): app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات الحساب (تأكد أنك وضعت بياناتك في config.py) ---
from config import API_ID, API_HASH, SESSION

client = TelegramClient(SESSION, API_ID, API_HASH)

# --- دالة تحميل الملحقات (هنا السر!) ---
def load_plugins():
    path = "plugins/*.py"
    files = glob.glob(path)
    for name in files:
        with open(name) as f:
            path1 = name.replace(".py", "").replace("/", ".").replace("\\", ".")
            importlib.import_module(path1)
            print(f"✅ تم تحميل الموديول: {path1}")

async def start_bot():
    keep_alive()
    load_plugins() # تشغيل الأوامر
    await client.start()
    print("🛡️ سورس المتمرد شغال الآن.. جرب اكتب .اوامري")
    await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(start_bot())
