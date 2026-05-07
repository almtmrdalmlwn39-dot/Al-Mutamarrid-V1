import asyncio, os, json, threading, re, glob, importlib
from pathlib import Path
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
import config 

# [1] تشغيل ريندر 24 ساعة
app = Flask(__name__)
@app.route('/')
def health_check(): return "🛡️ Rebel is Live"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()

# [2] الهوية (الصافية باسم المتمرد فقط)
REBEL_TITLE = "المتمرد"
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

# --- [3] ميزة (الرد التلقائي والحماية بالصورة في الخاص) --- 🛡️
@client.on(events.NewMessage(incoming=True))
async def private_guard(event):
    if not event.is_private: return
    data = load_data()
    if event.sender_id in SUDO_USERS or event.sender_id in data.get("allowed", []): return
    
    u_id = str(event.sender_id)
    counts = data.get("counts", {})
    count = counts.get(u_id, 0) + 1
    counts[u_id] = count; data["counts"] = counts; save_data(data)

    if count == 1: # أول رسالة يرسلها الشخص، البوت يرد بالصورة فوراً
        msg = f"**{REBEL_TITLE}**\n\n- مرحباً بك في معقل المتمرد التقني 🛡️\n⚠️ **تنبيه:** يمنع السبام لتجنب الحظر.\n{REBEL_LINK}"
        await client.send_file(event.chat_id, REBEL_IMG, caption=msg)
    elif count >= 5: # الحماية (البلوك التلقائي)
        await event.reply("**🚫 تم حظرك تلقائياً بسبب السبام.**")
        await client(functions.contacts.BlockRequest(id=event.sender_id))

# --- [4] ميزة (الايدي بالصورة + الفحص + الأوامر) --- 📸
@client.on(events.NewMessage(outgoing=True))
async def rebel_commands(event):
    text = event.raw_text
    data = load_data()

    if text.startswith(".فحص"):
        await event.edit(f"**{REBEL_TITLE}**\n**🛡️ درع المتمرد نشط.. الحساب تحت الحماية القصوى.**")

    elif text.startswith(".ايدي"): # الايدي بالصورة الشخصية للمستخدم
        reply = await event.get_reply_message()
        target = reply.sender if reply else await event.get_sender()
        photo = await client.download_profile_photo(target.id)
        info = f"**{REBEL_TITLE}**\n— — —\n👤 **الاسم:** {target.first_name}\n🆔 **الايدي:** `{target.id}`\n{REBEL_LINK}"
        await client.send_file(event.chat_id, photo or REBEL_IMG, caption=info)
        await event.delete()

    elif text.startswith(".رفع مطور"):
        reply = await event.get_reply_message()
        if reply:
            if reply.sender_id not in data["allowed"]:
                data["allowed"].append(reply.sender_id)
                save_data(data); await event.edit(f"**✅ تم رفع `{reply.sender_id}` مطوراً.**")
        else: await event.edit("**❌ ارفع بالرد على الشخص.**")

    elif text.startswith(".الاوامر"): # قائمة الأوامر بالصورة
        cmds = f"**{REBEL_TITLE}**\n— — —\n`.فحص` | `.ايدي` | `.رفع مطور` | `.تنزيل مطور`\n— — —\n{REBEL_LINK}"
        await client.send_file(event.chat_id, REBEL_IMG, caption=cmds)
        await event.delete()

# --- [5] ميزة (استدعاء الأوامر من الملفات الأخرى) --- 📂
def load_plugins():
    # يبحث في مجلد plugins ويشغل كل ملفات الجروبات والحماية الأخرى
    for name in glob.glob("plugins/*.py"):
        try:
            importlib.import_module("plugins." + Path(name).stem)
        except: pass

async def start_rebel():
    load_plugins() # استدعاء الملفات الخارجية عند التشغيل
    await client.start()
    print("🛡️ REBEL SOURCE IS READY")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(start_rebel())
