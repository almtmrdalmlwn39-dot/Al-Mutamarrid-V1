import asyncio
from telethon import events, functions, types

# استدعاء الكلاينت بطريقة تضمن الاتصال بالسيرفر
try:
    from main import client
except ImportError:
    from __main__ import client

# هوية الرد التلقائي
AUTO_IDENTITY = "**- نـظام الـرد الـآلي | الـمتمرد الـتقني 🤖🦅**"

# عبارة الأمن السيبراني
CYBER_SECURITY_NOTE = """
**🛡️ في عالم المتمرد، الأمن ليس خياراً بل هوية. 
أعتز بخصوصية عالمي، وأقدر تواصلك الراقي. 
جاري معالجة طلبك بأعلى مستويات الحماية.. كن صبوراً.**
"""

# قائمة المسموح لهم ومخزن السبام
allowed_users = []
spam_control = {}

# 1. نظام حماية الخاص الشامل
@client.on(events.NewMessage(incoming=True))
async def private_protection_handler(event):
    # التأكد أن الرسالة في الخاص وليست منك وليست من بوت
    if event.is_private and not event.out:
        sender = await event.get_sender()
        if sender and sender.bot:
            return
            
        user_id = event.sender_id
        
        # إذا كان مسموحاً له، توقف عن الرد الآلي
        if user_id in allowed_users:
            return

        # حساب الرسائل للحظر التلقائي (السبام)
        spam_control[user_id] = spam_control.get(user_id, 0) + 1
        if spam_control[user_id] > 5: # زدنا العدد قليلاً للتجربة
            await event.reply("**⚠️ تـم حـظرك تـلقائياً بـسبب الـإزعاج. 🛡️**")
            await client(functions.contacts.BlockRequest(id=user_id))
            return

        # نص الترحيب
        protection_msg = f"""
**- أهـلاً بـك فـي مـعقل الـمتمرد الـتقني 🛡️**
— — — — — — — — — — —
◈ اسمك ⇐ {sender.first_name if sender else 'مستخدم'}
◈ ايديك ⇐ `{user_id}`
— — — — — — — — — — —
**⚠️ تـحذير الـسيطرة :**
**يـمنع الـإزعاج. سـيد الـمتمرد مـشغول الآن.. اتـرك رسـالتك بـوضوح. 🦅**

{CYBER_SECURITY_NOTE}
— — — — — — — — — — —
{AUTO_IDENTITY}
"""
        try:
            # محاولة جلب الصورة وإرسالها
            photos = await client.get_profile_photos(user_id)
            if photos:
                await client.send_file(event.chat_id, photos[0], caption=protection_msg)
            else:
                await event.reply(protection_msg)
        except:
            await event.reply(protection_msg)

# 2. أمر السماح (.سماح)
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.سماح"))
async def allow_user(event):
    user_id = event.chat_id
    if user_id not in allowed_users:
        allowed_users.append(user_id)
    await event.edit("**✅ تـم الـسماح لـهذا الـمستخدم.**")

# 3. أمر الرفض (.رفض)
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.رفض"))
async def deny_user(event):
    user_id = event.chat_id
    if user_id in allowed_users:
        allowed_users.remove(user_id)
    await event.edit("**❌ تـم إلـغاء الـسماح.**")
