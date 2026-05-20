import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

# جلب البيانات من المنصة (Environment Variables)
API_ID = int(os.environ.get("API_ID", 22610186))
API_HASH = os.environ.get("API_HASH", "184e7fd176413cd0d2425494f1796229")
SESSION = os.environ.get("SESSION_STRING") # اسم المتغير في رندر

# إنشاء العميل (حسابك الشخصي)
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

async def main():
    print("-----------------------------------------")
    print("🛡️  AL-MUTAMARRID SOURCE IS STARTING... 🛡️")
    print("-----------------------------------------")
    
    # تشغيل الحساب
    await client.start()
    
    # استخراج وتشغيل كل ملفات المجلد plugins
    import glob
    from pathlib import Path
    import importlib

    files = glob.glob("plugins/*.py")
    for name in files:
        module_name = Path(name).stem
        importlib.import_module(f"plugins.{module_name}")
        print(f"✅ Loaded Module: {module_name}")

    print("🚀 SOURCE IS NOW LIVE ON YOUR ACCOUNT!")
    await client.run_until_disconnected()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
