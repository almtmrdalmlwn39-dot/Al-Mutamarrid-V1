Import asyncio, os, json, threading, re, glob, importlib
from pathlib import Path
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
import config 

# [1] ريندر - لضمان العمل 24 ساعة
app = Flask(__name__)
@app.route('/')
def health_check(): return "🛡️ Rebel is Live"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()

# [2] الهوية والإعدادات
REBEL_TITLE = الامن السيبراني 
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
    return {"allowed": [], "counts": {}}

def save_data(data):
    with open(DB_FILE, "w") as f: json.dump(data, f)

# --- [3] حماية الخاص والرد التلقائي (للمراسلات القادمة incoming) ---
@client.on(events.NewMessage(incoming=True))
async def private_guard(event):
    if not event.is_private: return
    data = load_data()
    # استثناء المالك والمطورين
    if event.sender_id in SUDO_USERS or event.sender_id in data.get("allowed", []): return
    
    u_id = str(event.sender_id)
    counts = data.get("counts", {})
    count = counts.get(u_id, 0) + 1
    counts[u_id] = count; data["counts"] = counts; save_data(data)

    if count == 1:
        await client.send_file(event.chat_id, REBEL_IMG, caption=f"**{REBEL_TITLE}**\n\n- مرحباً بك في معقل المتمرد.. يمنع التكرار.\n{REBEL_LINK}")
    elif count >= 5:
        await event.reply("**🚫 تم حظرك تلقائياً.**")
        await client(functions.contacts.BlockRequest(id=event.sender_id))

# --- [4] أوامر السيطرة (للأوامر التي ترسلها أنت outgoing) ---
@client.on(events.NewMessage(outgoing=True))
async def rebel_commands(event):
    text = event.raw_text
    data = load_data()

    if text == ".فحص":
        await event.edit(f"**{REBEL_TITLE}**\n**🛡️ درع المتمرد نشط.**")

    elif text == ".الاوامر":
        cmds = "**.فحص | .ايدي | .رفع مطور | .تنزيل مطور**"
        await client.send_file(event.chat_id, REBEL_IMG, caption=f"**{REBEL_TITLE}**\n\n{cmds}\n\n{REBEL_LINK}")
        await event.delete()

    elif text == ".ايدي":
        reply = await event.get_reply_message()
        target = reply.sender if reply else await event.get_sender()
        try:
            photo = await client.download_profile_photo(target.id)
            await client.send_file(event.chat_id, photo or REBEL_IMG, caption=f"🆔 الايدي: `{target.id}`")
            await event.delete()
        except:
            await event.edit(f"🆔 الايدي: `{target.id}`")

    elif text.startswith(".رفع مطور"):
        reply = await event.get_reply_message()
        if reply:
            if reply.sender_id not in data["allowed"]:
                data["allowed"].append(reply.sender_id)
                save_data(data); await event.edit(f"**✅ تم رفعه مطوراً.**")
        else: await event.edit("**❌ رد على رسالته.**")

# --- [5] محرك تشغيل "باقي الأوامر" (القروبات وغيرها) ---
def load_plugins():
    path = "plugins/*.py"
    files = glob.glob(path)
    for name in files:
        shortname = Path(name).stem
        try:
            importlib.import_module(f"plugins.{shortname}")
        except: pass

async def start_rebel():
    await client.start()
    load_plugins() # الآن بيستدعي أوامر القروبات بعد ما يشتغل الحساب
    print("🛡️ REBEL READY")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(start_rebel())
