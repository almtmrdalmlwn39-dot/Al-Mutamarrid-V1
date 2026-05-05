from telethon import events
import main

client = main.client

# قائمة البيضاء (الأشخاص المسموح لهم)
allowed_users = []

# 1. نظام الرد التلقائي الذكي
@client.on(events.NewMessage(incoming=True))
async def rebel_protection(event):
    # الرد فقط في الخاص، ومن الآخرين، وإذا لم يكن مسموحاً له
    if event.is_private and not event.out:
        user_id = event.sender_id
        
        # إذا الشخص في قائمة السماح، البوت يسكت وما يرد
        if user_id in allowed_users:
            return
            
        user = await event.get_sender()
        if user and user.bot: return

        protection_msg = f"""
**- أهـلاً بـك فـي مـعقل الـمتمرد الـتقني 🛡️**
— — — — — — — — — — —
◈ اسمك ⇐ {user.first_name}
◈ ايديك ⇐ `{user_id}`
— — — — — — — — — — —
**🛡️ في عالم المتمرد، الأمن ليس خياراً بل هوية.**
**أعتز بخصوصية عالمي، وأقدر تواصلك الراقي.**
**جاري معالجة طلبك بأعلى مستويات الحماية.. كن صبوراً. 🦅**
— — — — — — — — — — —
**- نـظام الـرد الـآلي | الـمتمرد الـتقني 🤖🦅**
"""
        await event.reply(protection_msg)

# 2. أمر السماح (.سماح)
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.سماح"))
async def allow(event):
    user_id = event.chat_id
    if user_id not in allowed_users:
        allowed_users.append(user_id)
        await event.edit("**✅ تـم الـسماح لـهذا الـمستخدم بـتخطي الـحماية.**")
    else:
        await event.edit("**⚠️ الـمستخدم مـسموح لـه بـالفعل.**")

# 3. أمر الرفض (.رفض)
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.رفض"))
async def deny(event):
    user_id = event.chat_id
    if user_id in allowed_users:
        allowed_users.remove(user_id)
        await event.edit("**❌ تـم إلـغاء الـسماح، نـظام الـحماية يـراقب الآن.**")
    else:
        await event.edit("**⚠️ الـمستخدم غـير مـسموح لـه أصلاً.**")

# 4. أمر الفحص (.فحص)
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.فحص"))
async def check(event):
    await event.edit("**🚀 الـمتمرد يـعمل بـنجاح، والأوامر جـاهزة!**")
