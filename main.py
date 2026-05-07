import asyncio, os, json, threading, re
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
import config 

# --- [1] إصلاح إقلاع ريندر (فتح المنفذ 10000) ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "🛡️ Rebel Source is Active"

def run_flask():
    # ريندر يحتاج ربط منفذ ليعتبر الإقلاع ناجحاً
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# --- [2] الهوية والبيانات ---
REBEL_TITLE = " المتمـــــــــرد²⁰⁰³🦅"
REBEL_SIG_TEXT = "**نحن لا نحمي بياناتك فقط، نحن نمنحك القوة لتكون السيد في عالم لا يعترف إلا بالأقوياء. المتمرد.. أمانٌ لا يُخترق.**"
REBEL_IMG = "https://telegra.ph/file/058204663f73359d997f0.jpg"
DB_FILE = "rebel_security.json"
SUDO_USERS = [6467728995] # ايديك المالك

client = TelegramClient(StringSession(config.SESSION), config.API_ID, config.API_HASH)

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: pass
    return {"status": True, "counts": {}, "allowed": []}

def save_data(data):
    with open(DB_FILE, "w") as f: json.dump(data, f)

# --- [3] محرك الأوامر (رفع/تنزيل + عرض الأوامر) ---
@client.on(events.NewMessage(outgoing=True))
async def rebel_engine(event):
    text = event.text
    data = load_data()
    
    if text == ".رفع مطور":
        reply = await event.get_reply_message()
        if reply:
            if reply.sender_id not in data["allowed"]:
                data["allowed"].append(reply.sender_id)
                save_data(data); await event.edit(f"**✅ تم رفع `{reply.sender_id}` مطوراً.**")
        else: await event.edit("**❌ ارسل الأمر بالرد على الشخص.**")

    elif text == ".الاوامر" or text == ".اوامر الجروب": # دعم الأوامر التي جربتها
        msg = f"**{REBEL_TITLE}**\n— — —\n**١ ⇐** `.رفع مطور`\n**٢ ⇐** `.تنزيل مطور`\n**٣ ⇐** `.ايدي`\n— — —"
        await client.send_file(event.chat_id, REBEL_IMG, caption=msg); await event.delete()

# --- [4] حماية القروبات (Anti-Hack) ---
@client.on(events.ChatAction)
async def group_guard(event):
    data = load_data()
    if event.user_id in SUDO_USERS or event.user_id in data.get("allowed", []): return
    
    if event.user_kicked or event.new_title or event.new_photo:
        try:
            await client(functions.channels.EditBannedRequest(
                event.chat_id, event.user_id, types.ChatBannedRights(until_date=None, view_messages=True)
            ))
            await event.reply("**🛡️ تم رصد محاولة تخريب وحظر المخرب.**")
        except: pass

# --- [5] حماية الخاص والترحيب ---
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
        await client.send_file(event.chat_id, REBEL_IMG, caption=f"**{REBEL_TITLE}**\n⚠️ تحذير (1/5): يمنع السبام.")
    elif count >= 5:
        await client(functions.contacts.BlockRequest(id=event.sender_id))

async def start_rebel():
    await client.start()
    print("🛡️ Rebel is Online") # ستظهر في سجلات ريندر
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(start_rebel())
