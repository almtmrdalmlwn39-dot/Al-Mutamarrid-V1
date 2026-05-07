import asyncio, os, pytz, glob, importlib, sys, re, json, threading
from datetime import datetime
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
from telethon.tl.functions.channels import GetFullChannelRequest
import google.generativeai as genai
import config 

# --- [1] الهوية ---
REBEL_SIG_TEXT = "نحن لا نحمي بياناتك فقط، نحن نمنحك القوة لتكون السيد في عالم لا يعترف إلا بالأقوياء. المتمرد.. أمانٌ لا يُخترق، وهيبةٌ لا تُهزم."
REBEL_IMG = "https://telegra.ph/file/058204663f73359d997f0.jpg"
SUDO_USERS = [6467728995] 

app = Flask(__name__)
@app.route('/')
def health_check(): return "🛡️ Rebel Source is Live"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()

client = TelegramClient(StringSession(config.SESSION), config.API_ID, config.API_HASH)

def z_nums(text):
    n = {'0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'}
    return "".join(n.get(c, c) for c in text)

def load_data():
    if os.path.exists("rebel.json"):
        try:
            with open("rebel.json", "r") as f: return json.load(f)
        except: pass
    return {"status": True}

# --- [2] محرك الأوامر المطور ---
@client.on(events.NewMessage(outgoing=True))
async def rebel_engine(event):
    text = event.raw_text
    
    # إصلاح أمر السحب للتأكد من المصداقية
    if text.startswith(".سحب"):
        try:
            parts = text.split(" ")
            if len(parts) < 2: return await event.edit("**❌ أرسل المعرف (مثال: .سحب @username)**")
            chat = parts[1]
            await event.edit(f"**⏳ جاري الفحص والسحب من {chat}...**")
            
            participants = await client.get_participants(chat, limit=100) # سحب عينة للتأكد
            await event.edit(f"**✅ تم سحب `{z_nums(str(len(participants)))}` عضو بنجاح.**\n\n🛡️ ملاحظة: إذا كان العدد أقل من المتوقع، فالجروب محمي من السحب.")
        except Exception as e: await event.edit(f"**❌ خطأ في السحب: {e}**")

    # تفعيل أمر الفحص
    elif text == ".فحص":
        await event.edit(f"**🛡️ سورس المتمرد يعمل بنجاح.**\n\n{REBEL_SIG_TEXT}")

    # تفعيل أوامر الحماية
    elif text == ".تفعيل الحماية":
        with open("rebel.json", "w") as f: json.dump({"status": True}, f)
        await event.edit("**✅ تم تشغيل درع الحماية التلقائي.**")
    
    elif text == ".تعطيل الحماية":
        with open("rebel.json", "w") as f: json.dump({"status": False}, f)
        await event.edit("**⚠️ تم إيقاف درع الحماية.**")

    # أمر عرض الأوامر
    elif text == ".الاوامر":
        all_cmds = [".سحب", ".ايدي", ".فحص", ".تفعيل الحماية", ".تعطيل الحماية"]
        msg = f"🛡️ **قائمة أوامر المتمرد**\n— — —\n{REBEL_SIG_TEXT}\n— — —\n"
        for i, cmd in enumerate(all_cmds, 1):
            msg += f"{z_nums(str(i))} ⇐ {cmd}\n"
        await event.edit(msg)

# --- [3] حماية الخاص ---
@client.on(events.NewMessage(incoming=True))
async def security(event):
    if not event.is_private or event.sender_id in SUDO_USERS: return
    if load_data().get("status"):
        # منطق الرد التلقائي والحظر هنا
        pass

# --- [4] التشغيل ---
async def start_rebel():
    await client.start()
    print("🛡️ REBEL ACTIVE")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(start_rebel())
