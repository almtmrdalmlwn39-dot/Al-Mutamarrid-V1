import asyncio, os, json, threading, re
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
import config 

# --- [1] محرك ريندر (فتح المنفذ 10000) لضمان العمل 24 ساعة ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "🛡️ Rebel Source is Active"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# --- [2] إعدادات الهوية (المتمرد²⁰⁰³🦅 فقط) ---
REBEL_TITLE = "المتمـــــــــرد²⁰⁰³🦅"
REBEL_SIG_TEXT = "**نحن لا نحمي بياناتك فقط، نحن نمنحك القوة لتكون السيد في عالم لا يعترف إلا بالأقوياء. المتمرد.. أمانٌ لا يُخترق.**"
REBEL_DEV_LINKS = (
    "\n— — — — — — — — — — — —\n"
    "👤 المطور الأول ⇐ **[تواصل هنا](https://t.me/Vi_ti0)**\n"
    "👤 المطور الثاني ⇐ **[تواصل هنا](https://t.me/A0_O7)**\n"
    "— — — — — — — — — — — —"
)
REBEL_IMG = "https://telegra.ph/file/058204663f73359d997f0.jpg"
DB_FILE = "rebel_security.json"
SUDO_USERS = [6467728995] 

client = TelegramClient(StringSession(config.SESSION), config.API_ID, config.API_HASH)

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: pass
    return {"status": True, "counts": {}, "allowed": []}

def save_data(data):
    with open(DB_FILE, "w") as f: json.dump(data, f)

# --- [3] نظام الرد التلقائي وحماية الخاص بالصورة ---
@client.on(events.NewMessage(incoming=True))
async def private_security(event):
    if not event.is_private: return
    data = load_data()
    if event.sender_id in SUDO_USERS or event.sender_id in data.get("allowed", []): return

    u_str = str(event.sender_id)
    counts = data.get("counts", {})
    count = counts.get(u_str, 0) + 1
    counts[u_str] = count; data["counts"] = counts; save_data(data)

    if count == 1:
        rebel_msg = (
            f"**{REBEL_TITLE}**\n\n"
            "- أهلاً بك في معقل المتمرد التقني 🛡️\n"
            "⚠️ **تحذير (1/5):** يمنع السبام والتكرار.\n"
            f"{REBEL_DEV_LINKS}"
        )
        await client.send_file(event.chat_id, REBEL_IMG, caption=rebel_msg)
    elif count >= 5:
        await event.reply("**🚫 تم حظرك نهائياً لتجاوز حد السبام.**")
        await client(functions.contacts.BlockRequest(id=event.sender_id))

# --- [4] حماية القروبات (الدرع العظيم) ---
@client.on(events.ChatAction)
async def group_guard(event):
    data = load_data()
    if event.user_id in SUDO_USERS or event.user_id in data.get("allowed", []): return
    
    if event.user_kicked or event.new_title or event.new_photo:
        try:
            await client(functions.channels.EditBannedRequest(
                event.chat_id, event.user_id, types.ChatBannedRights(until_date=None, view_messages=True)
            ))
            await event.reply(f"**🛡️ {REBEL_TITLE}\n⚠️ تم رصد محاولة تخريب وحظر المخرب فوراً.**")
        except: pass

# --- [5] أوامر المالك (رفع مطور + ايدي بالصورة + الأوامر) ---
@client.on(events.NewMessage(outgoing=True))
async def rebel_commands(event):
    text = event.text
    data = load_data()
    
    if text == ".رفع مطور":
        reply = await event.get_reply_message()
        if reply:
            if "allowed" not in data: data["allowed"] = []
            if reply.sender_id not in data["allowed"]:
                data["allowed"].append(reply.sender_id)
                save_data(data); await event.edit(f"**✅ تم رفع `{reply.sender_id}` مطوراً في السورس.**")
        else: await event.edit("**❌ ارسل الأمر بالرد على الشخص.**")

    elif text == ".ايدي":
        reply = await event.get_reply_message()
        target = reply.sender if reply else await event.get_sender()
        info = f"**{REBEL_TITLE}**\n— — —\n**👤 الاسم:** {target.first_name}\n**🆔 الايدي:** `{target.id}`\n**🎖️ الرتبة:** المالك\n{REBEL_DEV_LINKS}"
        photo = await client.download_profile_photo(target.id)
        await client.send_file(event.chat_id, photo or REBEL_IMG, caption=info); await event.delete()

    elif text == ".الاوامر" or text == ".اوامر الجروب":
        msg = f"**{REBEL_TITLE}**\n— — —\n**١ ⇐** `.ايدي`\n**٢ ⇐** `.رفع مطور`\n**٣ ⇐** `.تنزيل مطور`\n— — —\n{REBEL_DEV_LINKS}"
        await client.send_file(event.chat_id, REBEL_IMG, caption=msg); await event.delete()

async def start_rebel():
    await client.start()
    print("🛡️ REBEL SOURCE IS LIVE")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(start_rebel())
