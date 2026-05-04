import os, glob, importlib, asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from flask import Flask
from threading import Thread

# سيرفر Flask لإبقاء السيرفر حياً
app = Flask('')
@app.route('/')
def home(): return "The Rebel is Online"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# استيراد البيانات من config
from config import API_ID, API_HASH, SESSION
BOT_TOKEN = "8662258332:AAF_B4f_UvP_ZpGD8Bzbu-hu3qpb2COzx3s"

# تعريف الكلاينت والبوت
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
tgbot = TelegramClient("bot_assistant", API_ID, API_HASH)

# تصدير الكلاينت للملحقات
import __main__
__main__.client = client

def load_plugins():
    path = "plugins/*.py"
    for name in glob.glob(path):
        module_name = name.replace(".py", "").replace("/", ".").replace("\\", ".")
        try:
            importlib.import_module(module_name)
            print(f"✅ Loaded: {module_name}")
        except Exception as e:
            print(f"❌ Error in {module_name}: {e}")

async def start_rebel():
    print("⏳ جاري الإقلاع...")
    await client.start()
    await tgbot.start(bot_token=BOT_TOKEN)
    load_plugins()
    print("🛡️ المتمرد يعمل الآن!")
    await asyncio.gather(
        client.run_until_disconnected(),
        tgbot.run_until_disconnected()
    )

if __name__ == '__main__':
    keep_alive()
    asyncio.run(start_rebel())
