import os
import glob
import importlib.util
from telethon import TelegramClient
from telethon.sessions import StringSession
from config import API_ID, API_HASH, SESSION

# تشغيل العميل باستخدام الجلسة المستخرجة
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

def load_plugins():
    # البحث عن كل ملفات الموديولات داخل مجلد plugins
    path = "plugins/*.py"
    files = glob.glob(path)
    for name in files:
        try:
            # تحويل مسار الملف لاسم موديول
            module_spec = importlib.util.spec_from_file_location("plugin", name)
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
            print(f"✅ تم تحميل الموديول: {os.path.basename(name)}")
        except Exception as e:
            print(f"❌ فشل تحميل {os.path.basename(name)} بسبب: {e}")

async def main():
    print("🚀 جاري تشغيل سورس المتمرد التقني...")
    load_plugins()
    # التحقق من الاتصال
    await client.start()
    print("🛡️ السورس شغال الآن! اذهب لتليجرام واكتب .اوامري")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())

