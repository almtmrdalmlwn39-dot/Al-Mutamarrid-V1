import asyncio, os, pytz, time
from datetime import datetime
from telethon import TelegramClient, events, functions
from telethon.sessions import StringSession
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

# --- [ البيانات الأساسية ] ---
API_ID = 20585941
API_HASH = "4c8b6debbee47ab644c82305487f34b2"
SESSION = "1BJWap1wBu5vQiQcBMGMZKLP2M4bB9N35sx4d6ImRcOhwqsosy6VZ7IKnFblvoBi-wwK4e2Rw5mWP_MhdFk7DnlVk0wbAEZMXxeONswAvGteNtW4tnjMhEkMEbjrZs0boh5nrE8yzOxucTVnzj58v4I6ynr1pY01ROVPbBY0EX7LEITSMqOz5ZQjj9KFFrKaUTTVYxFqiMFZSrDkdVJIn3kzj_US7If39FwfsL0qc9SQUqEY5rnvXGSussGODWnUMesYnrTsj0JRBQNlvYW2HwC2SCPJydl1peBmLwxeevARUg70-wi2rrOUDCQMZnRfgsBIHX2j-3ZooY6WueuxU-SPrtk0M418="

# --- [ إعدادات الهوية ] ---
YEMEN_TZ = pytz.timezone('Asia/Aden')
CYBER_IDENTITY = "**- سـورس الـمتمرد ✅ | الـقوةُ والـسيطرة. 🦅🛡️**"

def custom_nums(text):
    nums = {'0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵'}
    return "".join(nums.get(c, c) for c in text)

# إنشاء العميل
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# --- [ الأوامر ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.حالة$"))
async def status_check(event):
    start = time.time()
    await client(functions.PingRequest(ping_id=0))
    ping_ms = round((time.time() - start) * 1000)
    time_now = datetime.now(YEMEN_TZ).strftime("%I:%M")
    await event.edit(f"**🚀 الـمتمرد نـشط:**\n**⚡ الـسرعة: `{custom_nums(str(ping_ms))}` ms**\n**⌚ الـوقت: `{custom_nums(time_now)}`**\n{CYBER_IDENTITY}")

@client.on(events.NewMessage(outgoing=True, pattern=r"^\.(تدمير|تفليش)$"))
async def nuker(event):
    await event.edit("**- جـاري الـسحق 🧨**")
    rights = ChatBannedRights(until_date=None, view_messages=True)
    async for user in client.iter_participants(event.chat_id):
        if user.is_self or user.admin_rights: continue
        try: await client(EditBannedRequest(event.chat_id, user.id, rights))
        except: continue
    await event.respond(f"**- تـم الـسحق بـواسطة الـمتمرد ✅**")

# --- [ الحل الجذري لخطأ الـ RuntimeError ] ---
async def main():
    await client.start()
    print("🦅 الـمتمرد نـشط الآن! جـرب .حالة")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # هذه الأسطر هي اللي "عـتسبّر" السورس في ريندر
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
