import asyncio, os, glob, json, threading, re
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
import config 

# --- [1] حل مشكلة ريندر (المنفذ الوهمي) ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "🛡️ Rebel Source is Live"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# --- [2] الهوية والروابط الموحدة ---
REBEL_SIG_TEXT = "**نحن لا نحمي بياناتك فقط، نحن نمنحك القوة لتكون السيد في عالم لا يعترف إلا بالأقوياء. المتمرد.. أمانٌ لا يُخترق، وهيبةٌ لا تُهزم.**"
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

def z_nums(text):
    n = {'0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'}
    return "".join(n.get(c, c) for c in text)

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: pass
    return {"status": True, "counts": {}}

def save_data(data):
    with open(DB_FILE, "w") as f: json.dump(data, f)

# --- [3] محرك الأوامر (للخارج فقط) ---
@client.on(events.NewMessage(outgoing=True))
async def rebel_main_engine(event):
    text = event.text
    if text == ".الاوامر":
        msg = f"**🛡️ معقل المتمرد 🦅**\n— — —\n{REBEL_SIG_TEXT}\n— — —\n**١ ⇐** `.ايدي`\n**٢ ⇐** `.تفعيل الحماية`\n— — —\n{REBEL_DEV_LINKS}"
        await client.send_file(event.chat_id, REBEL_IMG, caption=msg); await event.delete()
    elif text.startswith(".ايدي"):
        reply = await event.get_reply_message()
        target = reply.sender if reply else await event.get_sender()
        info = f"**👤 الاسم:** {target.first_name}\n**🆔 الايدي:** `{target.id}`\n**🎖️ الرتبة:** المالك\n{REBEL_DEV_LINKS}"
        photo = await client.download_profile_photo(target.id)
        await client.send_file(event.chat_id, photo or REBEL_IMG, caption=info); await event.delete()

# --- [4] نظام الترحيب والحماية المدمج (مع الصورة) ---
@client.on(events.NewMessage(incoming=True))
async def security_logic(event):
    if not event.is_private: return
    data = load_data()
    if not data.get("status") or event.sender_id in SUDO_USERS: return

    u_str = str(event.sender_id)
    counts = data.get("counts", {})
    count = counts.get(u_str, 0) + 1
    counts[u_str] = count; data["counts"] = counts; save_data(data)

    sender = await event.get_sender()
    f_name = sender.first_name if sender.first_name else "المستخدم"

    if count == 1:
        # الترحيب الفخم بالصورة من أول رسالة
        welcome_msg = (
            f"**- أهلاً بك يا {f_name} في معقل المتمرد التقني 🛡️**\n"
            f"— — —\n"
            f"{REBEL_SIG_TEXT}\n"
            f"— — —\n"
            f"⚠️ **تحذير ({z_nums(str(count))}/٥):** يمنع السبام والتكرار.\n"
            f"{REBEL_DEV_LINKS}"
        )
        await client.send_file(event.chat_id, REBEL_IMG, caption=welcome_msg)
    elif count >= 5:
        # الحظر النهائي
        await event.reply(f"**🚫 تم حظرك لتجاوزك حد التكرار.**\n{REBEL_DEV_LINKS}")
        await client(functions.contacts.BlockRequest(id=event.sender_id))

async def start_rebel():
    await client.start()
    print("🛡️ Rebel Source is Ready with Image Welcome")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(start_rebel())
