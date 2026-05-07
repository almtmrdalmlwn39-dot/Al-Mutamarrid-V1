import asyncio, os, glob, json, threading, re
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
import config 

# --- [1] حل مشكلة ريندر (المنفذ الوهمي) لمنع التوقف ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "🛡️ Rebel Source is Live"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# --- [2] الهوية والروابط الموحدة (عبارة المتمرد) ---
REBEL_TITLE =  المتمـــــــــرد²⁰⁰³🦅" # العبارة من صورتك
REBEL_SIG_TEXT = "**نحن لا نحمي بياناتك فقط، نحن نمنحك القوة لتكون السيد في عالم لا يعترف إلا بالأقوياء. المتمرد.. أمانٌ لا يُخترق، وهيبةٌ لا تُهزم.**"
REBEL_DEV_LINKS = (
    "\n— — — — — — — — — — — —\n"
    "👤 المطور الأول ⇐ **[تواصل هنا](https://t.me/Vi_ti0)**\n"
    "👤 المطور الثاني ⇐ **[تواصل هنا](https://t.me/A0_O7)**\n"
    "— — — — — — — — — — — —"
)
REBEL_IMG = "https://telegra.ph/file/058204663f73359d997f0.jpg"
DB_FILE = "rebel_security.json"
SUDO_USERS = [6467728995] # ايديك المالك

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

# --- [3] محرك الأوامر (رفع وتنزيل المطورين + الهوية) ---
@client.on(events.NewMessage(outgoing=True))
async def rebel_main_engine(event):
    text = event.text
    data = load_data()
    
    # أوامر إدارة المطورين
    if text == ".رفع مطور":
        reply = await event.get_reply_message()
        if reply and reply.sender_id not in data.get("allowed", []):
            if "allowed" not in data: data["allowed"] = []
            data["allowed"].append(reply.sender_id)
            save_data(data); await event.edit(f"**✅ تم رفع `{reply.sender_id}` مطوراً أساسياً.**")
        else: await event.edit("**❌ يجب الرد على شخص غير مرفوع.**")

    elif text == ".تنزيل مطور":
        reply = await event.get_reply_message()
        if reply and reply.sender_id in data.get("allowed", []):
            data["allowed"].remove(reply.sender_id)
            save_data(data); await event.edit(f"**❌ تم تنزيل `{reply.sender_id}` من الرتبة.**")
        else: await event.edit("**⚠️ الشخص ليس مطوراً.**")

    elif text == ".الاوامر":
        msg = f"**{REBEL_TITLE}**\n— — —\n{REBEL_SIG_TEXT}\n— — —\n**١ ⇐** `.ايدي`\n**٢ ⇐** `.رفع مطور`\n**٣ ⇐** `.تنزيل مطور`\n— — —\n{REBEL_DEV_LINKS}"
        await client.send_file(event.chat_id, REBEL_IMG, caption=msg); await event.delete()

    elif text.startswith(".ايدي"):
        reply = await event.get_reply_message()
        target = reply.sender if reply else await event.get_sender()
        info = f"**{REBEL_TITLE}**\n— — —\n**👤 الاسم:** {target.first_name}\n**🆔 الايدي:** `{target.id}`\n**🎖️ الرتبة:** المالك\n{REBEL_DEV_LINKS}"
        photo = await client.download_profile_photo(target.id)
        await client.send_file(event.chat_id, photo or REBEL_IMG, caption=info); await event.delete()

# --- [4] نظام الترحيب والحماية (تخطي المالك والمطورين) ---
@client.on(events.NewMessage(incoming=True))
async def security_logic(event):
    if not event.is_private: return
    data = load_data()
    # استثناء المالك والمطورين المرفوعين من الحماية
    if not data.get("status") or event.sender_id in SUDO_USERS or event.sender_id in data.get("allowed", []):
        return

    u_str = str(event.sender_id)
    counts = data.get("counts", {})
    count = counts.get(u_str, 0) + 1
    counts[u_str] = count; data["counts"] = counts; save_data(data)

    if count == 1:
        f_name = (await event.get_sender()).first_name or "المستخدم"
        welcome_msg = (
            f"**{REBEL_TITLE}**\n"
            f"**- أهلاً بك يا {f_name} في معقل المتمرد التقني 🛡️**\n"
            f"— — —\n"
            f"{REBEL_SIG_TEXT}\n"
            f"— — —\n"
            f"⚠️ **تحذير ({z_nums(str(count))}/٥):** يمنع السبام والتكرار.\n"
            f"{REBEL_DEV_LINKS}"
        )
        await client.send_file(event.chat_id, REBEL_IMG, caption=welcome_msg)
    elif count >= 5:
        await event.reply(f"**🚫 تم حظرك لتجاوزك حد التكرار.**\n{REBEL_DEV_LINKS}")
        await client(functions.contacts.BlockRequest(id=event.sender_id))

async def start_rebel():
    await client.start()
    print("🛡️ Rebel Source is Ready with All Features")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(start_rebel())
