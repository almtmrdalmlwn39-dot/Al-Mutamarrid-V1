import asyncio, os, pytz, time, glob, importlib
from datetime import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
import config # ملف الإعدادات

# إعداد العميل وجلب الجلسة
SESSION = os.environ.get("TERMUX_SESSION") or ""
client = TelegramClient(StringSession(SESSION), config.API_ID, config.API_HASH)

# زخرفة الأرقام للساعة
def z_nums(text):
    n = {'0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'}
    return "".join(n.get(c, c) for c in text)

# محرك تحديث الساعة والنبذة التلقائي
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

# --- [ محرك تحميل الأوامر الإضافية ] ---
def load_plugins():
    # يبحث عن كل ملفات .py داخل مجلد plugins ويشغلها
    path = "plugins/*.py"
    files = glob.glob(path)
    for name in files:
        plugin_name = name.replace("/", ".").replace("\\", ".").replace(".py", "")
        importlib.import_module(plugin_name)
        print(f"✅ تم تفعيل الأوامر من: {plugin_name}")

# الإقلاع الرئيسي
async def start_mared():
    await client.start()
    print("🦅 الـمتمرد فــرانــكَـَۄ نـشط الآن..")
    
    # تشغيل محرك الساعة في الخلفية
    asyncio.create_task(profile_engine())
    
    # تحميل أوامر الإدارة (admin.py)
    load_plugins()
    
    await client.run_until_disconnected()

if __name__ == '__main__':
    # حل مشكلة Event Loop في بيئة Render
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_mared())
