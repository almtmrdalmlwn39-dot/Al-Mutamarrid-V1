import asyncio, os, pytz, glob, importlib, sys
from datetime import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
import config # استدعاء ملف الإعدادات

# جلب الجلسة المعرفة في ملف config
SESSION_STRING = config.SESSION 
client = TelegramClient(StringSession(SESSION_STRING), config.API_ID, config.API_HASH)

def z_nums(text):
    n = {'0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'}
    return "".join(n.get(c, c) for c in text)

async def profile_engine():
    while True:
        try:
            tm = z_nums(datetime.now(config.YEMEN_TZ).strftime("%I:%M"))
            await client(UpdateProfileRequest(
                first_name=f"{config.FIXED_NAME} | {tm}",
                about=f"{config.MY_BIO} | {tm}"
            ))
        except: pass
        await asyncio.sleep(60)

def load_plugins():
    for name in glob.glob("plugins/*.py"):
        plugin_name = name.replace("/", ".").replace("\\", ".").replace(".py", "")
        try:
            importlib.import_module(plugin_name)
            print(f"✅ Loaded: {plugin_name}")
        except Exception as e:
            print(f"❌ Error in {plugin_name}: {e}")

async def start_mared():
    # الدخول بالجلسة يمنع طلب الرقم (EOFError)
    await client.start()
    print("🦅 الـمتمرد..")
    asyncio.create_task(profile_engine())
    load_plugins()
    await client.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(start_mared())
    except KeyboardInterrupt:
        pass
