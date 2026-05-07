import asyncio, os, json, threading, re, glob, importlib
from pathlib import Path
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
import config 

# [1] تشغيل السيرفر لضمان الحالة Live
app = Flask(__name__)
@app.route('/')
def health_check(): return "🛡️ Rebel is Live"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()

# [2] الهوية والبيانات
REBEL_TITLE = "┃ الأمن السيبراني 🛡️"
REBEL_IMG = "https://telegra.ph/file/058204663f73359d997f0.jpg"
REBEL_LINK = "👤 **المطور:** [المتمرد](https://t.me/Vi_ti0)"
SUDO_USERS = [6467728995] 

client = TelegramClient(StringSession(config.SESSION), config.API_ID, config.API_HASH)

# --- [3] محرك الاستدعاء الخارق (هذا اللي ناقصك) ---
def load_plugins():
    # يبحث عن كل الملفات داخل مجلد plugins ويشغلها
    path = "plugins/*.py"
    files = glob.glob(path)
    for name in files:
        shortname = Path(name).stem
        try:
            # ربط الملفات (مثل rebel_auto) بالسورس الأساسي
            importlib.import_module(f"plugins.{shortname}")
            print(f"✅ تم تحميل: {shortname}")
        except Exception as e:
            print(f"❌ خطأ في {shortname}: {e}")

# --- [4] الأوامر الأساسية لضمان الاستجابة ---
@client.on(events.NewMessage(outgoing=True))
async def base_commands(event):
    if event.raw_text == ".فحص":
        await event.edit(f"**🛡️ درع المتمرد نشط.. الأوامر تعمل الآن.**")
    
    elif event.raw_text == ".الاوامر":
        # هنا البوت بيعرض الأوامر الأساسية + المفروض الإضافات تشتغل
        msg = f"**{REBEL_TITLE}**\n— — —\n`.فحص` | `.ايدي` | `.الاوامر` | `.اوامري` \n— — —\n{REBEL_LINK}"
        await client.send_file(event.chat_id, REBEL_IMG, caption=msg)
        await event.delete()

async def start_rebel():
    await client.start()
    load_plugins() # لازم يتحملوا بعد الـ start عشان يتصلوا بالحساب
    print("🛡️ السورس جاهز بكامل أوامره")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(start_rebel())
