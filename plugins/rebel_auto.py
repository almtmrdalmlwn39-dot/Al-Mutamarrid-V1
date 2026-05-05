import asyncio
from telethon import events, functions, types
import main 

client = main.client
# هوية الرد التلقائي
AUTO_IDENTITY = "**- نـظام الـرد الـآلي | الـمتمرد الـتقني 🤖🦅**"

# عبارة الأمن السيبراني
CYBER_SECURITY_NOTE = """
**🛡️ في عالم المتمرد، الأمن ليس خياراً بل هوية. 
أعتز بخصوصية عالمي، وأقدر تواصلك الراقي. 
جاري معالجة طلبك بأعلى مستويات الحماية.. كن صبوراً.**
"""

# قائمة الأشخاص المسموح لهم (تخزن في الذاكرة)
allowed_users = []
# مخزن مؤقت لحساب الرسائل
spam_control = {}

# 1. نظام حماية الخاص مع السماح والرفض
@client.on(events.NewMessage(incoming=True))
async def private_protection_handler(event):
    if event.is_private and not event.out and not (await event.get_sender()).bot:
        user_id = event.sender_id
        
        # إذا كان الشخص مسموحاً له، لا تفعل شيئاً
        if user_id in allowed_users:
            return

        user = await event.get_sender()
        
        # نظام الحظر التلقائي (بعد 3 رسائل)
        spam_control[user_id] = spam_control.get(user_id, 0) + 1
        if spam_control[user_id] > 3:
            await event.reply("**⚠️ تـم حـظرك تـلقائياً بـسبب الـإزعاج وتـجاوز نـظام الـحماية. 🛡️**")
            await client(functions.contacts.BlockRequest(id=user_id))
            return

        # رسالة الترحيب والتحذير
        protection_msg = f"""
**- أهـلاً بـك فـي مـعقل الـمتمرد الـتقني 🛡️**
— — — — — — — — — — —
◈ اسمك ⇐ {user.first_name}
◈ ايديك ⇐ `{user_id}`
— — — — — — — — — — —
**⚠️ تـحذير الـسيطرة :**
**يـمنع الـإزعاج أو الـتكرار. سـيد الـمتمرد مـشغول بـتطوير الـعالم الآن.. اتـرك رسـالتك بـوضوح. 🦅**

{CYBER_SECURITY_NOTE}
— — — — — — — — — — —
{AUTO_IDENTITY}
"""
        try:
            photos = await client.get_profile_photos(user)
            if photos:
                await client.send_file(event.chat_id, photos[0], caption=protection_msg)
            else:
                await event.reply(protection_msg)
        except Exception:
            await event.reply(protection_msg)

# 2. أمر السماح (.سماح) بالرد على الشخص
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.سماح"))
async def allow_user(event):
    if event.is_private:
        user_id = event.chat_id
        if user_id not in allowed_users:
            allowed_users.append(user_id)
            await event.edit("**✅ تـم الـسماح لـهذا الـمستخدم بـتخطي الـحماية.**")
        else:
            await event.edit("**⚠️ الـمستخدم مـسموح لـه بـالفعل.**")

# 3. أمر الرفض (.رفض) لإعادة تفعيل الحماية عليه
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.رفض"))
async def deny_user(event):
    if event.is_private:
        user_id = event.chat_id
        if user_id in allowed_users:
            allowed_users.remove(user_id)
            await event.edit("**❌ تـم إلـغاء الـسماح، نـظام الـحماية يـراقب الآن.**")
        else:
            await event.edit("**⚠️ الـمستخدم غـير مـسموح لـه أصلاً.**")

# 4. ميزة "قلك"
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.قلك"))
async def quick_statement(event):
    await event.edit("**- قـال لـك الـمتمرد الـتقني :**\n**الـعقول الـعظيمة تـبني الـأكواد.. 🦅**")
