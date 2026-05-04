import asyncio, os, pytz, re, random, time
from datetime import datetime
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

# --- [ إعدادات المحرك الأساسية ] ---
# جلب البيانات من ريندر (تأكد أن الأسماء مطابقة لما في Environment Variables)
API_ID = int(os.environ.get("APP_ID", 0))
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("TERMUX_SESSION")

# تعريف الـ client (هذا هو السطر اللي كان ناقص الكود حقك)
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# --- [ إعدادات الهوية والوقت ] ---
YEMEN_TZ = pytz.timezone('Asia/Aden')
approved_users = set() 
warned_users = set() 
BANNED_RIGHTS = ChatBannedRights(until_date=None, view_messages=True, send_messages=True, send_media=True, send_stickers=True, send_gifs=True, send_games=True, send_inline=True, embed_links=True)
CYBER_IDENTITY = "**- نـحنُ حـماةُ الـخصوصيةِ فـي زمنِ الاختراق 🦅💻🛡️**"

# دالة زخرفة الأرقام
def custom_nums(text):
    nums = {'0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵'}
    return "".join(nums.get(c, c) for c in text)

# --- [ 1. محرك الترحيب والرد الآلي (كودك القديم) ] ---
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def pm_welcome(event):
    if event.is_bot: return
    sender = await event.get_sender()
    if not sender or event.sender_id in approved_users or event.sender_id in warned_users: return
    me = await client.get_me()
    if event.sender_id == me.id: return 
    
    time_now = datetime.now(YEMEN_TZ).strftime("%I:%M %p")
    welcome_msg = (f"**- مـرحباً بـك يـا {sender.first_name} فـي سـيرفر الـمتمرد 🦅\n"
                   f"**- تـوقيت الـيمن الآن: {custom_nums(time_now)}**\n"
                   "**— — — — — — — — — —**\n"
                   "**🛡️ | جـدار الـحماية مـفعل تـلقائياً.**\n"
                   f"{CYBER_IDENTITY}")
    try:
        await event.reply(welcome_msg)
        warned_users.add(event.sender_id)
    except: pass

# --- [ 2. المحرك الرئيسي للأوامر (كودك القديم + الإضافات) ] ---
@client.on(events.NewMessage(outgoing=True))
async def mutamarrid_engine(event):
    cmd = event.text
    chat = event.chat_id

    if cmd == ".سماح":
        approved_users.add(event.chat_id)
        await event.edit("**✅ تـم الـسماح.**")
    
    elif cmd == ".حالة_السورس":
        start = time.time()
        await client(functions.PingRequest(ping_id=0))
        ping_ms = round((time.time() - start) * 1000)
        time_now = datetime.now(YEMEN_TZ).strftime("%I:%M")
        await event.edit(f"**🚀 نـظام الـمتمرد نـشط:**\n**⚡ الـسرعة: `{custom_nums(str(ping_ms))}` ms**\n**⌚ الـوقت: `{custom_nums(time_now)}`**\n{CYBER_IDENTITY}")

    elif cmd in [".تدمير", ".تفليش"]:
        await event.edit("**- جـاري الـتطهير 🧨**")
        async for user in client.iter_participants(chat):
            if user.is_self or user.admin_rights: continue 
            try: await client(EditBannedRequest(chat, user.id, BANNED_RIGHTS))
            except: continue
        await event.respond(f"**- تـم سـحق الـجروب بـواسطة الـمتمرد ✅**\n{CYBER_IDENTITY}")

    elif cmd == ".اوامر":
        await event.edit(f"**- أوامـر الـمتمرد 🦅:**\n"
                         "**🛡️ .سماح | .حالة_السورس**\n"
                         "**🧨 .تفليش | .تدمير**\n"
                         f"{CYBER_IDENTITY}")

# --- [ تشغيل السورس ] ---
print("🚀 جـاري الإقـلاع...")
client.start()
print("🦅 الـمتمرد نـشط الآن!")
client.run_until_disconnected()
