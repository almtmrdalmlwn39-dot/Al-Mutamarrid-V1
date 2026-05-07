import asyncio, os, json, threading, re, glob, importlib
from pathlib import Path
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
import config 

# [1] السيرفر اللي ظهر في صورتك إنه شغال
app = Flask(__name__)
@app.route('/')
def health_check(): return "🛡️ Rebel is Live"

def run_flask():
    try:
        app.run(host='0.0.0.0', port=10000)
    except: pass

threading.Thread(target=run_flask, daemon=True).start()

# [2] الهوية (الأمن السيبراني)
REBEL_TITLE = "┃ الأمن السيبراني 🛡️"
REBEL_IMG = "https://telegra.ph/file/058204663f73359d997f0.jpg"
REBEL_LINK = "👤 **المطور:** [المتمرد](https://t.me/Vi_ti0)"
SUDO_USERS = [6467728995] 
DB_FILE = "rebel_security.json"

client = TelegramClient(StringSession(config.SESSION), config.API_ID, config.API_HASH)

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: pass
    return {"allowed": [6467728995], "counts": {}} # المالك مضاف تلقائياً

def save_data(data):
    with open(DB_FILE, "w") as f: json.dump(data, f)

# --- [3] حماية الخاص (Incoming) ---
@client.on(events.NewMessage(incoming=True))
async def private_guard(event):
    if not event.is_private: return
    data = load_data()
    if event.sender_id in SUDO_USERS or event.sender_id in data.get("allowed", []): return
    
    u_id = str(event.sender_id)
    counts = data.get("counts", {})
    count = counts.get(u_id, 0) + 1
    counts[u_id] = count; data["counts"] = counts; save_data(data)

    if count == 1:
        await client.send_file(event.chat_id, REBEL_IMG, caption=f"**{REBEL_TITLE}**\n\n- مرحباً بك في معقل المتمرد.. يمنع التكرار.\n{REBEL_LINK}")
    elif count >= 5:
        await client(functions.contacts.BlockRequest(id=event.sender_id))

# --- [4] الأوامر الرئيسية (Outgoing) ---
@client.on(events.NewMessage(outgoing=True))
async def rebel_commands(event):
    text = event.raw_text
    if text == ".فحص":
        await event.edit(f"**🛡️ درع المتمرد نشط.. الحساب تحت الحماية القصوى.**") #
    elif text == ".الاوامر":
        cmds = "**.فحص | .ايدي | .رفع مطور | .تنزيل مطور**"
        await client.send_file(event.chat_id, REBEL_IMG, caption=f"**{REBEL_TITLE}**\n\n{cmds}\n\n{REBEL_LINK}")
        await event.delete()

# --- [5] محرك الاستدعاء (Plugins) لملفات القروبات وغيرها ---
def load_plugins():
    # يبحث في مجلد plugins ويشغل أي ملف بايثون
    path = "plugins/*.py"
    for name in glob.glob(path):
        shortname = Path(name).stem
        try:
            importlib.import_module(f"plugins.{shortname}")
            print(f"✅ Loaded: {shortname}")
        except: pass

async def start_rebel():
    await client.start()
    load_plugins() # الآن يستدعي ملفات القروبات بعد تسجيل الدخول
    print("🛡️ REBEL READY")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(start_rebel())
