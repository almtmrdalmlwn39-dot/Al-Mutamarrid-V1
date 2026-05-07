import asyncio, os, json, threading, re
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
import config 

# --- [1] محرك ريندر (عشان يظل السورس Live 24 ساعة) ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "🛡️ Rebel Source is Live"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

threading.Thread(target=run_flask, daemon=True).start()

# --- [2] إعدادات الهوية والمطورين ---
REBEL_TITLE = "المتمـــــــــرد²⁰⁰³"
REBEL_IMG = "https://telegra.ph/file/058204663f73359d997f0.jpg"
REBEL_DEV_LINKS = (
    "\n— — — — — — — — — — — —\n"
    "👤 المطور الأول ⇐ **[تواصل هنا](https://t.me/Vi_ti0)**\n"
    "👤 المطور الثاني ⇐ **[تواصل هنا](https://t.me/A0_O7)**\n"
    "— — — — — — — — — — — —"
)
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

# --- [3] نظام الرد التلقائي وحماية الخاص (الرد بالصورة) ---
@client.on(events.NewMessage(incoming=True))
async def private_handler(event):
    if not event.is_private: return
    data = load_data()
    # استثناء المالك والمطورين من الحماية
    if event.sender_id in SUDO_USERS or event.sender_id in data.get("allowed", []): return

    u_id = str(event.sender_id)
    counts = data.get("counts", {})
    count = counts.get(u_id, 0) + 1
    counts[u_id] = count; data["counts"] = counts; save_data(data)

    if count == 1:
        welcome = f"**{REBEL_TITLE}**\n\n- أهلاً بك في معقل المتمرد التقني 🛡️\n⚠️ تحذير (1/5): يمنع السبام والتكرار.\n{REBEL_DEV_LINKS}"
        await client.send_file(event.chat_id, REBEL_IMG, caption=welcome)
    elif count >= 5:
        await event.reply("**🚫 تم حظرك تلقائياً لتجاوز حد الرسائل.**")
        await client(functions.contacts.BlockRequest(id=event.sender_id))

# --- [4] حماية القروبات (الدرع ضد الهكر والتفليش) ---
@client.on(events.ChatAction)
async def group_protection(event):
    data = load_data()
    if event.user_id in SUDO_USERS or event.user_id in data.get("allowed", []): return
    
    # إذا حاول شخص طرد عضو أو تغيير معلومات القروب
    if event.user_kicked or event.new_title or event.new_photo:
        try:
            await client(functions.channels.EditBannedRequest(
                event.chat_id, event.user_id, types.ChatBannedRights(until_date=None, view_messages=True)
            ))
            await event.reply(f"**🛡️ {REBEL_TITLE}**\n⚠️ تم كشف محاولة تخريب وحظر المخرب فوراً.")
        except: pass

# --- [5] أوامر المالك والمطورين (تم استرجاعها كاملة) ---
@client.on(events.NewMessage(outgoing=True))
async def owner_commands(event):
    text = event.raw_text
    data = load_data()

    if text.startswith(".فحص"):
        await event.edit(f"**{REBEL_TITLE}**\n**✅ السورس والدرع شغالين 100% يا متمرد.**")

    elif text.startswith(".ايدي"):
        reply = await event.get_reply_message()
        target = reply.sender if reply else await event.get_sender()
        photo = await client.download_profile_photo(target.id)
        info = f"**{REBEL_TITLE}**\n— — —\n👤 **الاسم:** {target.first_name}\n🆔 **الايدي:** `{target.id}`\n🎖️ **الرتبة:** المالك\n{REBEL_DEV_LINKS}"
        await client.send_file(event.chat_id, photo or REBEL_IMG, caption=info)
        await event.delete()

    elif text.startswith(".رفع مطور"):
        reply = await event.get_reply_message()
        if reply:
            if reply.sender_id not in data["allowed"]:
                data["allowed"].append(reply.sender_id)
                save_data(data); await event.edit(f"**✅ تم رفع `{reply.sender_id}` مطوراً بنجاح.**")
        else: await event.edit("**❌ ارفع بالرد على الشخص.**")

    elif text.startswith(".الاوامر"):
        cmds = f"**{REBEL_TITLE}**\n— — —\n`.فحص` | `.ايدي` | `.رفع مطور` | `.تنزيل مطور`\n— — —\n{REBEL_DEV_LINKS}"
        await client.send_file(event.chat_id, REBEL_IMG, caption=cmds)
        await event.delete()

async def start_rebel():
    await client.start()
    print("🛡️ REBEL SOURCE IS FULLY ACTIVE")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(start_rebel())
