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
    # Render يستخدم المنفذ 8080 غالباً
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# تشغيل السيرفر الوهمي فوراً
keep_alive()
# ------------------------------------------

# تشغيل العميل باستخدام الجلسة المستخرجة
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

def load_plugins():
    # البحث عن كل ملفات الموديولات داخل مجلد plugins
    path = "plugins/*.py"
    files = glob.glob(path)
    for name in files:
        try:
            # تحويل مسار الملف لاسم موديول
            module_name = os.path.basename(name).replace(".py", "")
            spec = importlib.util.spec_from_file_location(module_name, name)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print(f"✅ تم تحميل الموديول: {module_name}")
        except Exception as e:
            print(f"❌ فشل تحميل {os.path.basename(name)} بسبب: {e}")

async def main():
    print("🚀 جاري تشغيل سورس المتمرد التقني...")
    
    # التحقق من الاتصال وبدء العميل
    await client.start()
    
    # تحميل الملحقات بعد بدء العميل لضمان الربط
    load_plugins()
    
    print("🛡️ السورس شغال الآن! اذهب لتليجرام واكتب .اوامري")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # استخدام loop الخاص بـ client لضمان الاستقرار
    client.loop.run_until_complete(main())
