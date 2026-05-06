import asyncio, os, pytz, glob, importlib, sys
from datetime import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
import config 

# --- كود إرضاء منصة ريندر ---
from flask import Flask
import threading

app = Flask(__name__)
@app.route('/')
def health_check():
    return "The Rebel UserBot is Live! 🦅"

def run_flask():
    try:
        app.run(host='0.0.0.0', port=10000)
    except: pass

threading.Thread(target=run_flask, daemon=True).start()

# --- تعريف الكلاينت ---
SESSION_STRING = config.SESSION 
client = TelegramClient(StringSession(SESSION_STRING), config.API_ID, config.API_HASH)

def z_nums(text):
    n = {'0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'}
    return "".join(n.get(c, c) for c in text)

# --- محرك البروفايل الذكي (يسحب اسمك الحالي ولا يلمس العلامات) ---
async def profile_engine():
    while True:
        try:
            # 1. جلب اسمك الحالي من الحساب
            me = await client.get_me()
            full_name = me.first_name if me.first_name else "المتمرد"

            # 2. تنظيف الوقت القديم فقط (يبحث عن آخر علامة | ويحذف ما بعدها)
            if " | " in full_name:
                clean_name = full_name.rsplit(" | ", 1)[0]
            else:
                clean_name = full_name

            # 3. جلب الوقت بتوقيت اليمن وتنسيقه
            tm = z_nums(datetime.now(config.YEMEN_TZ).strftime("%I:%M"))
            
            # 4. تحديث الحساب (اسمك الذي كتبته بيدك + الساعة الجديدة)
            await client(UpdateProfileRequest(
                first_name=f"{clean_name} | {tm}"
            ))
            
            await asyncio.sleep(300) # تحديث كل 5 دقائق
        except Exception as e:
            await asyncio.sleep(300)

def load_plugins():
    if not os.path.exists("plugins"):
        os.makedirs("plugins")
    for name in glob.glob("plugins/*.py"):
        plugin_name = name.replace("/", ".").replace("\\", ".").replace(".py", "")
        if "__init__" in plugin_name: continue
        try:
            importlib.import_module(plugin_name)
        except Exception as e:
            pass

async def start_mared():
    await client.start()
    print("🦅 الـمتمرد يـحلق الآن..")
    load_plugins()
    asyncio.create_task(profile_engine())
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        client.loop.run_until_complete(start_mared())
    except (KeyboardInterrupt, SystemExit):
        pass
