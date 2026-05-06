from telethon import events, functions
import asyncio
from datetime import datetime
import main

client = main.client
allowed_users = []

# 1. نظام الرد التلقائي (الترحيب)
@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    if event.is_private and not event.out:
        if event.sender_id in allowed_users: return
        user = await event.get_sender()
        if user and user.bot: return
        
        msg = f"""
**- أهـلاً بـك فـي مـعقل الـمتمرد الـتقني 🛡️**
— — — — — — — — — — —
◈ اسمك ⇐ {user.first_name}
◈ ايديك ⇐ `{event.sender_id}`
— — — — — — — — — — —
**🛡️ في عالم المتمرد، الأمن ليس خياراً بل هوية.**
**جاري معالجة طلبك.. كن صبوراً. 🦅**
— — — — — — — — — — —
**- نـظام الـرد الـآلي | الـمتمرد الـتقني 🤖🦅**
"""
        await event.reply(msg)

# 2. أوامر التحكم (سماح، رفض، فحص)
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.(سماح|رفض|فحص)"))
async def control(event):
    cmd = event.pattern_match.group(1)
    if cmd == "سماح":
        allowed_users.append(event.chat_id)
        await event.edit("**✅ تـم الـسماح.**")
    elif cmd == "رفض":
        if event.chat_id in allowed_users: allowed_users.remove(event.chat_id)
        await event.edit("**❌ تـم الـرفض.**")
    elif cmd == "فحص":
        await event.edit("**🚀 الـمتمرد شـغال مـية مـية!**")

# 3. نظام الاسم الوقتي (مدمج بطريقة آمنة لتجنب Flood)
async def time_name_task():
    while True:
        try:
            current_time = datetime.now().strftime("%I:%M")
            await client(functions.account.UpdateProfileRequest(
                first_name=f"فرانكو | {current_time}"
            ))
            await asyncio.sleep(300) # تحديث كل 5 دقائق فقط لتجنب الحظر
        except:
            await asyncio.sleep(600)

# تشغيل الاسم الوقتي في الخلفية
client.loop.create_task(time_name_task())
