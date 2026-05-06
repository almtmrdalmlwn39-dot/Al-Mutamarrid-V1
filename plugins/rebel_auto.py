from telethon import events, functions
import asyncio
from datetime import datetime
# التعديل الذهبي: الاستدعاء من الملف الرئيسي مباشرة لضمان العمل
from __main__ import client

allowed_users = []

# 1. نظام الرد التلقائي (الترحيب)
@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    # الرد فقط في الخاص وعلى الرسائل الواردة (ليست منك)
    if event.is_private and not event.out:
        # إذا كان المستخدم مسموح له، لا ترد عليه
        if event.sender_id in allowed_users: 
            return
        
        user = await event.get_sender()
        # تجاهل البوتات تماماً
        if user and user.bot: 
            return
        
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
        try:
            await event.reply(msg)
        except Exception as e:
            print(f"خطأ في الرد: {e}")

# 2. أوامر التحكم (سماح، رفض، فحص)
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.(سماح|رفض|فحص)"))
async def control(event):
    cmd = event.pattern_match.group(1)
    if cmd == "سماح":
        if event.chat_id not in allowed_users:
            allowed_users.append(event.chat_id)
        await event.edit("**✅ تـم الـسماح لـهذا الـمستخدم.**")
    elif cmd == "رفض":
        if event.chat_id in allowed_users: 
            allowed_users.remove(event.chat_id)
        await event.edit("**❌ تـم إلـغاء الـسماح.**")
    elif cmd == "فحص":
        await event.edit("**🚀 الـمتمرد شـغال مـية مـية!**")

# 3. نظام الاسم الوقتي (تحديث كل 5 دقائق)
async def time_name_task():
    while True:
        try:
            # تحديث الاسم ليناسب توقيت صنعاء
            from datetime import datetime
            import pytz
            yemen_tz = pytz.timezone('Asia/Aden')
            current_time = datetime.now(yemen_tz).strftime("%I:%M")
            await client(functions.account.UpdateProfileRequest(
                first_name=f"فرانكو | {current_time}"
            ))
            await asyncio.sleep(300) 
        except:
            await asyncio.sleep(600)

# تشغيل مهمة الوقت فور إقلاع البوت
client.loop.create_task(time_name_task())
