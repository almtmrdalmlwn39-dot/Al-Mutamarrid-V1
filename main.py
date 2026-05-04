import os, pytz, asyncio, sys
from datetime import datetime
from collections import defaultdict
from telethon import TelegramClient, events, functions, types
from telethon.tl.types import ChatBannedRights

# --- [ إعدادات الحماية والربط ] ---
# تأكد أن هذه القيم موجودة في ملف .env أو إعدادات Render
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION")

client = TelegramClient(SESSION, API_ID, API_HASH)

YEMEN_TZ = pytz.timezone('Asia/Aden')
CYBER_IDENTITY = "**- نـحنُ حـماةُ الـخصوصيةِ فـي زمنِ الاختراق 🦅💻🛡️**"

welcomed_users = set() 
user_messages = defaultdict(list) 

# --- [ محرك الحماية ] ---
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def fast_security_engine(event):
    if event.is_bot: return
    me = await client.get_me()
    if event.sender_id == me.id: return

    if event.sender_id not in welcomed_users:
        sender = await event.get_sender()
        time_now = datetime.now(YEMEN_TZ).strftime("%I:%M %p")
        welcome_msg = (
            f"**- مـرحباً بـك يـا {sender.first_name} فـي سـيرفر الـمتمرد 🦅\n"
            f"**- تـوقيت الـيمن: {time_now}**\n"
            "**🛡️ | جـدار الـحماية مـفعل تـلقائياً.**\n\n"
            f"{CYBER_IDENTITY}"
        )
        try:
            await event.reply(welcome_msg)
            welcomed_users.add(event.sender_id)
        except: pass

# --- [ الأوامر ] ---
@client.on(events.NewMessage(pattern=r'^\.بينج$', outgoing=True))
async def ping_cmd(event):
    start = datetime.now()
    await event.edit("**🚀 جـاري فحص النبض...**")
    ms = (datetime.now() - start).microseconds / 1000
    await event.edit(f"**⚡ سـرعة الـمتمرد: `{ms}`ms**")

# --- [ تشغيل البوت وضمان استمرار الرابط ] ---
async def main():
    print("🚀 جاري تشغيل سورس المتمرد...")
    await client.start()
    print("✅ السورس شغال الآن بنجاح!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
