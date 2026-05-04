import os, glob, importlib, asyncio
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from flask import Flask
from threading import Thread

# --- سيرفر إبقاء البوت حياً ---
app = Flask('')
@app.route('/')
def home(): return "I am alive"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- إعدادات الحساب والبوت ---
from config import API_ID, API_HASH, SESSION
BOT_TOKEN = "8662258332:AAF_B4f_UvP_ZpGD8Bzbu-hu3qpb2COzx3s"

# تعريف الكلاينت والبوت (تصدير العميل لكي تراه الملحقات)
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
tgbot = TelegramClient("bot_assistant", API_ID, API_HASH)

# جعل العميل متاحاً للملحقات
import __main__
__main__.client = client

# --- دالة تحميل الملحقات (معدلة لتعمل صح) ---
def load_plugins():
    path = "plugins/*.py"
    for name in glob.glob(path):
        module_name = name.replace(".py", "").replace("/", ".").replace("\\", ".")
        try:
            importlib.import_module(module_name)
            print(f"✅ تم تحميل الملحق: {module_name}")
        except Exception as e:
            print(f"❌ فشل تحميل {module_name}: {e}")

# --- الدالة الأساسية ---
async def start_services():
    print("⏳ جاري بدء إقلاع سورس المتمرد...")
    await client.start()
    await tgbot.start(bot_token=BOT_TOKEN)
    
    # تحميل الأوامر من plugins بعد تشغيل الكلاينت
    load_plugins()
    
    print("🛡️ السورس الآن Live والأوامر جاهزة!")
    await asyncio.gather(
        client.run_until_disconnected(),
        tgbot.run_until_disconnected()
    )

if __name__ == '__main__':
    keep_alive()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_services())
    except Exception as e:
        print(f"❌ خطأ في التشغيل: {e}")
