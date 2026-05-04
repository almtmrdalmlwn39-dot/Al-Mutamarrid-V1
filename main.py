import asyncio, os, pytz, re, random, time
from datetime import datetime
from collections import defaultdict
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.types import ChatBannedRights

# --- [ إعدادات الربط ] ---
API_ID = 20585941
API_HASH = "4c8b6debbee47ab644c82305487f34b2"
SESSION = os.environ.get("TERMUX_SESSION") or ""

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# --- [ الهوية الشخصية الفخمة ] ---
YEMEN_TZ = pytz.timezone('Asia/Aden')
FIXED_NAME = "فــرانــكَـَۄ|| 𝗟َِ𝗢َِ𝗿َِ𝗶َِ𝗙َِ𝒆َِل↜͟͞💸⁩"
MY_BIO = "نبذة تعريفية: شخص مغرم بنفسه ولايتنازل لـ خلق الله ابدا"
CYBER_IDENTITY = "**- نـحنُ حـماةُ الـخصوصيةِ فـي زمنِ الاختراق، نـبرمجُ الـصمتَ ونـصنعُ الـفرق.. عـقولنا خـلفَ الـشاشاتِ تـبني، وأيـدينا فـي الأنـظمةِ تـحمي. 🦅💻🛡️**"

welcomed_users = set()

def custom_nums(text):
    nums = {'0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵'}
    return "".join(nums.get(c, c) for c in text)

# --- [ 1. محرك تحديث الاسم والنبذة والساعة ] ---
async def update_profile_loop():
    while True:
        try:
            current_time = datetime.now(YEMEN_TZ).strftime("%I:%M")
            z_time = custom_nums(current_time)
            await client(UpdateProfileRequest(
                first_name=f"{FIXED_NAME} | {z_time}",
                about=f"{MY_BIO} | {z_time}"
            ))
        except Exception as e:
            print(f"Update Error: {e}")
        await asyncio.sleep(60)

# --- [ 2. محرك الرد التلقائي بالخاص ] ---
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def cyber_welcome(event):
    if event.is_bot: return
    me = await client.get_me()
    if event.sender_id == me.id: return
    
    if event.sender_id not in welcomed_users:
        sender = await event.get_sender()
        time_now = datetime.now(YEMEN_TZ).strftime("%I:%M %p")
        z_time = custom_nums(time_now)
        welcome_msg = (
            f"**- مـرحباً بـك يـا {sender.first_name} فـي سـيرفر الـمتمرد 🦅\n"
            f"**- تـوقيت الـيمن الـمحدد: {z_time}**\n"
            "**— — — — — — — — — —**\n"
            f"{CYBER_IDENTITY}"
        )
        try:
            photo = await client.download_profile_photo(me.id)
            if photo:
                await client.send_file(event.chat_id, photo, caption=welcome_msg)
                if os.path.exists(photo): os.remove(photo)
            else:
                await event.reply(welcome_msg)
            welcomed_users.add(event.sender_id)
        except: pass

# --- [ 3. محرك الأوامر والتفليش ] ---
@client.on(events.NewMessage(outgoing=True))
async def commands_engine(event):
    text = event.raw_text
    if text == ".حالة":
        start = time.time()
        await client(functions.PingRequest(ping_id=0))
        ping_ms = round((time.time() - start) * 1000)
        await event.edit(f"**🚀 الـمتمرد نـشط وبـكامل قـوته:**\n**⚡ الـسرعة: `{custom_nums(str(ping_ms))}` ms**\n\n{CYBER_IDENTITY}")

# --- [ الإقلاع الشامل - تم تعديله لحل مشكلة Loop ] ---
async def start_mared():
    await client.start()
    print(f"🦅 الـمتمرد {FIXED_NAME} نـشط الآن..")
    asyncio.create_task(update_profile_loop())
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_mared())
    except RuntimeError:
        # حل لمشكلة No current event loop
        asyncio.run(start_mared())
