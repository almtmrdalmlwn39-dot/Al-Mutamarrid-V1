import asyncio, os, pytz, re, random, time, threading
from datetime import datetime
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from flask import Flask

# --- [ إعداد منفذ ريندر الوهمي ] ---
app = Flask(__name__)
@app.route('/')
def home(): return "Rebel Source is Online ✅"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- [ إعدادات الهوية والربط ] ---
API_ID = 20585941
API_HASH = "4c8b6debbee47ab644c82305487f34b2"
SESSION = "1BJWap1wBu5vQiQcBMGMZKLP2M4bB9N35sx4d6ImRcOhwqsosy6VZ7IKnFblvoBi-wwK4e2Rw5mWP_MhdFk7DnlVk0wbAEZMXxeONswAvGteNtW4tnjMhEkMEbjrZs0boh5nrE8yzOxucTVnzj58v4I6ynr1pY01ROVPbBY0EX7LEITSMqOz5ZQjj9KFFrKaUTTVYxFqiMFZSrDkdVJIn3kzj_US7If39FwfsL0qc9SQUqEY5rnvXGSussGODWnUMesYnrTsj0JRBQNlvYW2HwC2SCPJydl1peBmLwxeevARUg70-wi2rrOUDCQMZnRfgsBIHX2j-3ZooY6WueuxU-SPrtk0M418="

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# --- [ إعدادات المتمرد ] ---
YEMEN_TZ = pytz.timezone('Asia/Aden')
BANNED_RIGHTS = ChatBannedRights(until_date=None, view_messages=True, send_messages=True, send_media=True, send_stickers=True, send_gifs=True, send_games=True, send_inline=True, embed_links=True)
CYBER_IDENTITY = "**- سـورس الـمتمرد ✅ | الـقوةُ والـسيطرة. 🦅🛡️**"

def custom_nums(text):
    nums = {'0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵'}
    return "".join(nums.get(c, c) for c in text)

# --- [ محرك الأوامر ] ---
@client.on(events.NewMessage(outgoing=True))
async def mutamarrid_engine(event):
    cmd = event.text
    if cmd == ".حالة":
        start = time.time()
        await client(functions.PingRequest(ping_id=0))
        ping_ms = round((time.time() - start) * 1000)
        time_now = datetime.now(YEMEN_TZ).strftime("%I:%M")
        await event.edit(f"**🚀 الـمتمرد نـشط الآن:**\n**⚡ الـسرعة: `{custom_nums(str(ping_ms))}` ms**\n**⌚ الـوقت: `{custom_nums(time_now)}`**\n{CYBER_IDENTITY}")
    elif cmd in [".تدمير", ".تفليش"]:
        await event.edit("**- جـاري الـسحق والـتطهير 🧨**")
        async for user in client.iter_participants(event.chat_id):
            if user.is_self or user.admin_rights: continue 
            try: await client(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
            except: continue
        await event.respond(f"**- تـم سـحق الـجروب بـواسطة الـمتمرد ✅**")

# --- [ تشغيل السورس ] ---
async def main():
    # تشغيل Flask في خيط منفصل تماماً
    threading.Thread(target=run_flask, daemon=True).start()
    
    # تشغيل التليجرام
    await client.start()
    print("🦅 سـورس الـمتمرد نـشط الآن.. جرب أمر .حالة")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # حل مشكلة الـ Event Loop لضمان الإقلاع
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
