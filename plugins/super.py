import asyncio, os, pytz, re, random, time
from datetime import datetime
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

# --- [ إعدادات الهوية والربط المباشر ] ---
API_ID = 20585941
API_HASH = "4c8b6debbee47ab644c82305487f34b2"
SESSION = os.environ.get("TERMUX_SESSION") or ""

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# --- [ إعدادات المتمرد ] ---
YEMEN_TZ = pytz.timezone('Asia/Aden')
BANNED_RIGHTS = ChatBannedRights(until_date=None, view_messages=True, send_messages=True, send_media=True, send_stickers=True, send_gifs=True, send_games=True, send_inline=True, embed_links=True)
CYBER_IDENTITY = "**- سـورس الـمتمرد ✅ | الـقوةُ والـسيطرة. 🦅🛡️**"

def custom_nums(text):
    nums = {'0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵'}
    return "".join(nums.get(c, c) for c in text)

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

# --- [ إقلاع السورس ] ---
print("🚀 جـاري الإقـلاع ببياناتك الخاصة...")
with client:
    print("🦅 الـمتمرد نـشط الآن.. جرب أمر .حالة")
    client.run_until_disconnected()
