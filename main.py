import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

# جلب البيانات من Environment Variables في رندر
API_ID = int(os.environ.get("API_ID", 22610186))
API_HASH = os.environ.get("API_HASH", "184e7fd176413cd0d2425494f1796229")
SESSION = os.environ.get("SESSION_STRING")

# تعريف العميل
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

async def load_plugins():
    import glob
    from pathlib import Path
    import importlib
    
    files = glob.glob("plugins/*.py")
    for name in files:
        module_name = Path(name).stem
        try:
            importlib.import_module(f"plugins.{module_name}")
            print(f"✅ Loaded: {module_name}")
        except Exception as e:
            print(f"❌ Failed to load {module_name}: {e}")

async def start_rebel():
    print("-----------------------------------------")
    print("🛡️  AL-MUTAMARRID SOURCE IS STARTING...  🛡️")
    print("-----------------------------------------")
    
    await client.start()
    await load_plugins()
    
    print("🚀 THE SOURCE IS LIVE ON YOUR ACCOUNT!")
    await client.run_until_disconnected()

if __name__ == "__main__":
    # هذا السطر هو الحل لخطأ الـ Event Loop في النسخ الجديدة
    try:
        asyncio.run(start_rebel())
    except (KeyboardInterrupt, SystemExit):
        pass
