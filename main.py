import asyncio, os, pytz, glob, importlib, sys, re, json, threading
from datetime import datetime
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.account import UpdateProfileRequest
import google.generativeai as genai
import config 

# --- [1] الهوية والذكاء الاصطناعي ---
REBEL_SIG_TEXT = "نحن لا نحمي بياناتك فقط، نحن نمنحك القوة لتكون السيد في عالم لا يعترف إلا بالأقوياء. المتمرد.. أمانٌ لا يُخترق، وهيبةٌ لا تُهزم."
REBEL_IMG = "https://telegra.ph/file/058204663f73359d997f0.jpg"

# إعداد ذكاء المتمرد في الامن السيبراني 
genai.configure(api_key="AIzaSyDwzx1U-IGgw-Kybz2RVt2N-xtkWrIt7aU")
model = genai.GenerativeModel('gemini-pro')

# --- [2] الإعدادات والسيرفر ---
DB_FILE = "rebel_security.json"
SUDO_USERS = [6467728995] 

app = Flask(__name__) # تم إصلاح الخطأ البرمجي هنا
@app.route('/')
def health_check(): return "🛡️ Rebel Source is Live"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()

client = TelegramClient(StringSession(config.SESSION), config.API_ID, config.API_HASH)

def z_nums(text):
    n = {'0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'}
    return "".join(n.get(c, c) for c in text)

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: pass
    return {"status": True, "counts": {}, "allowed": []}

def save_data(data):
    with open(DB_FILE, "w") as f: json.dump(data, f)

# --- [3] محرك الأوامر (سحب، ايدي، اوامر) ---
@client.on(events.NewMessage(outgoing=True))
async def rebel_engine(event):
    text = event.raw_text
    
    # أمر سحب الأعضاء
    if text.startswith(".سحب"):
        try:
            chat = text.split(" ")[1]
            await event.edit(f"**⏳ جاري سحب الأعضاء من {chat}...**")
            full = await client(GetFullChannelRequest(chat))
            participants = await client.get_participants(full.full_chat.id)
            await event.edit(f"**✅ تم سحب `{len(participants)}` عضو بنجاح.**")
        except: await event.edit("**❌ المعرف خطأ.**")

    # أمر الآيدي بالصورة
    elif text == ".ايدي":
        reply = await event.get_reply_message()
        target = reply.sender if reply else await event.get_sender()
        photo = await client.download_profile_photo(target.id)
        await client.send_file(event.chat_id, photo or REBEL_IMG, caption=f"🆔 الايدي: `{target.id}`")
        await event.delete()

    # أمر عرض الأوامر المطور
    elif text == ".الاوامر":
        all_list = [".سحب", ".ايدي", ".فحص", ".تفعيل الحماية", ".تعطيل الحماية"]
        msg = f"🛡️ **قائمة أوامر المتمرد**\n— — —\n{REBEL_SIG_TEXT}\n— — —\n"
        for i, cmd in enumerate(all_list, 1):
            msg += f"{z_nums(str(i))} ⇐ {cmd}\n"
        await event.edit(msg)

# --- [4] حماية الخاص والرد التلقائي ---
@client.on(events.NewMessage(incoming=True))
async def security_logic(event):
    if not event.is_private or event.sender_id in SUDO_USERS: return
    data = load_data()
    if not data.get("status"): return

    u_str = str(event.sender_id)
    counts = data.get("counts", {})
    count = counts.get(u_str, 0) + 1
    counts[u_str] = count; data["counts"] = counts; save_data(data)

    if count == 1:
        await client.send_file(event.chat_id, REBEL_IMG, caption=f"🛡️ **مرحباً بك.. يمنع التكرار.**\n\n{REBEL_SIG_TEXT}")
    elif count >= 5:
        await event.reply("🚫 **تم حظرك.**")
        await client(functions.contacts.BlockRequest(id=event.sender_id))

# --- [5] التشغيل ---
async def start_rebel():
    await client.start()
    print("🛡️ REBEL SOURCE LOADED")
    await client.run_until_disconnected()

if __name__ == '__main__': # تم إصلاح الشرطات التحتية هنا
    client.loop.run_until_complete(start_rebel())
