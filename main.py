import os
import glob
import importlib
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession # أضفنا هذا السطر
from flask import Flask
from threading import Thread

# --- إعدادات السيرفر لإبقاء البوت حياً ---
app = Flask('')
@app.route('/')
def home(): return "I am alive"

def run(): app.run(host='0.0.0.0', port=10000) # تم تعديل البورت ليتوافق مع Render

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات الحساب من ملف config ---
from config import API_ID, API_HASH, SESSION

# السطر الذهبي: التعديل الذي سيمنع انهيار السورس
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# --- دالة تحميل الملحقات ---
def load_plugins():
    path = "plugins/*.py"
    files = glob.glob(path)
    for name in files:
        path1 = name.replace(".py", "").replace("/", ".").replace("\\", ".")
        try:
            importlib.import_module(path1)
            print(f"✅ تم تحميل الموديول: {path1}")
        except Exception as e:
            print(f"❌ فشل تحميل {path1}: {e}")

async def start_bot():
    keep_alive()
    print("⏳ جاري تشغيل سورس المتمرد...")
    await client.start()
    load_plugins() # تحميل الأوامر بعد تسجيل الدخول
    print("🛡️ سورس المتمرد شغال الآن بنجاح.. جرب اكتب .الاوامر")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        pass
