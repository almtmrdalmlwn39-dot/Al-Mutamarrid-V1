import os
import glob
import importlib.util
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from config import API_ID, API_HASH, SESSION

# --- إضافة نظام Flask للبقاء متصلاً 24 ساعة ---
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "سورس المتمرد شغال بنجاح ✅"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()
# ------------------------------------------

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

def load_plugins():
    path = "plugins/*.py"
    files = glob.glob(path)
    for name in files:
        try:
            module_name = os.path.basename(name).replace(".py", "")
            spec = importlib.util.spec_from_file_location(module_name, name)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # --- التعديل السحري هنا ---
            # هذا الجزء يبحث عن الأوامر داخل الملف ويربطها بالحساب
            for attr in dir(module):
                value = getattr(module, attr)
                if hasattr(value, "callback"):
                    client.add_event_handler(value)
            # ------------------------
            
            print(f"✅ تم تحميل الموديول: {module_name}")
        except Exception as e:
            print(f"❌ فشل تحميل {os.path.basename(name)} بسبب: {e}")

async def main():
    print("🚀 جاري تشغيل سورس المتمرد التقني...")
    
    await client.start()
    load_plugins()

    # --- تشغيل ساعة النبذة تلقائياً من ملف super.py ---
    try:
        from plugins.super import bio_time_updater
        client.loop.create_task(bio_time_updater(client))
        print("🕒 تم بدء تشغيل ساعة النبذة...")
    except:
        pass

    print("🛡️ السورس شغال الآن! جرب أرسل .اوامري")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
