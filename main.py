import asyncio, os, pytz, time, glob, importlib
from datetime import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
import config # تأكد من وجود ملف config.py

# إعداد العميل
SESSION = os.environ.get("TERMUX_SESSION") or ""
client = TelegramClient(StringSession(SESSION), config.API_ID, config.API_HASH)

def z_nums(text):
    n = {'0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'}
    return "".join(n.get(c, c) for c in text)

# محرك تحديث الساعة والنبذة
async def profile_engine():
    while True:
        try:
            now = datetime.now(config.YEMEN_TZ).strftime("%I:%M")
            tm = z_nums(now)
            await client(UpdateProfileRequest(
                first_name=f"{config.FIXED_NAME} | {tm}",
                about=f"{config.MY_BIO} | {tm}"
            ))
        except: pass
        await asyncio.sleep(60)

# محرك تحميل ملفات الأوامر (Plugins)
def load_plugins():
    path = "plugins/*.py"
    files = glob.glob(path)
    for name in files:
        plugin_name = name.replace("/", ".").replace("\\", ".").replace(".py", "")
        try:
            importlib.import_module(plugin_name)
            print(f"✅ تم تحميل: {plugin_name}")
        except Exception as e:
            print(f"❌ خطأ في تحميل {plugin_name}: {e}")

async def start_mared():
    await client.start()
    print("🦅 الـمتمرد فــرانــكَـَۄ نـشط الآن..")
    
    # تشغيل الساعة وتحميل الأوامر
    asyncio.create_task(profile_engine())
    load_plugins()
    
    await client.run_until_disconnected()

# --- [ الجزء المعدل لحل مشكلة RuntimeError ] ---
if __name__ == '__main__':
    try:
        # المحاولة الأولى باستخدام asyncio.run
        asyncio.run(start_mared())
    except RuntimeError:
        # حل بديل في حال وجود حلقة تعمل بالفعل (كما يحدث في Render)
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(start_mared())
        else:
            loop.run_until_complete(start_mared())
    except (KeyboardInterrupt, SystemExit):
        pass
