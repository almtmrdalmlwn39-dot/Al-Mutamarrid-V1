import asyncio, os, pytz, re, random, time
from datetime import datetime
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

# --- [ إعدادات المحرك - تأكد من تعبئة البيانات هنا لو فشل ريندر ] ---
# إذا ريندر ما سحب البيانات، السورس بيستخدم اللي بنكتبه هانا
API_ID = int(os.environ.get("APP_ID") or 0) 
API_HASH = os.environ.get("API_HASH") or ""
SESSION = os.environ.get("TERMUX_SESSION") or ""

# تحقق أمان إضافي عشان ما يطفي السورس
if not API_ID or not API_HASH:
    print("⚠️ تنبيه: لم يتم العثور على API_ID أو API_HASH في ريندر!")
    # هانا تقدر تحط قيمك يدوياً كحل أخير إذا استمر الخطأ
    # API_ID = 123456
    # API_HASH = "your_hash_here"

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# --- [ بقية الكود حقك اللي فيه التفليش والترحيب ] ---
YEMEN_TZ = pytz.timezone('Asia/Aden')
approved_users = set() 
warned_users = set() 
BANNED_RIGHTS = ChatBannedRights(until_date=None, view_messages=True, send_messages=True, send_media=True, send_stickers=True, send_gifs=True, send_games=True, send_inline=True, embed_links=True)
CYBER_IDENTITY = "**- نـحنُ حـماةُ الـخصوصيةِ فـي زمنِ الاختراق 🦅💻🛡️**"

def custom_nums(text):
    nums = {'0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵'}
    return "".join(nums.get(c, c) for c in text)

@client.on(events.NewMessage(outgoing=True))
async def mutamarrid_engine(event):
    cmd = event.text
    chat = event.chat_id
    if cmd == ".حالة_السورس":
        start = time.time()
        await client(functions.PingRequest(ping_id=0))
        ping_ms = round((time.time() - start) * 1000)
        time_now = datetime.now(YEMEN_TZ).strftime("%I:%M")
        await event.edit(f"**🚀 الـمتمرد نـشط:**\n**⚡ الـسرعة: `{custom_nums(str(ping_ms))}` ms**\n**⌚ الـوقت: `{custom_nums(time_now)}`**\n{CYBER_IDENTITY}")
    elif cmd in [".تدمير", ".تفليش"]:
        await event.edit("**- جـاري الـتطهير 🧨**")
        async for user in client.iter_participants(chat):
            if user.is_self or user.admin_rights: continue 
            try: await client(EditBannedRequest(chat, user.id, BANNED_RIGHTS))
            except: continue
        await event.respond(f"**- تـم سـحق الـجروب بـواسطة الـمتمرد ✅**")

print("🚀 جـاري الإقـلاع...")
with client:
    print("🦅 الـمتمرد نـشط الآن!")
    client.run_until_disconnected()
