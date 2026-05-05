from telethon import events
import main

client = main.client

# قائمة السماح (الأشخاص الذين لن يرد عليهم البوت)
allowed_users = []

# نظام الرد التلقائي (محدث ليرد على الجميع بما فيهم حسابك الثاني)
@client.on(events.NewMessage(incoming=True))
async def rebel_protection(event):
    # الرد فقط في الخاص (Private) وبشرط ألا تكون الرسالة صادرة منك (not event.out)
    if event.is_private and not event.out:
        user_id = event.sender_id
        
        # إذا قمت بعمل .سماح لهذا الحساب، لن يرد البوت
        if user_id in allowed_users:
            return
            
        user = await event.get_sender()
        
        # نص الترحيب المنسق الذي طلبته
        protection_msg = f"""
**- أهـلاً بـك فـي مـعقل الـمتمرد الـتقني 🛡️**
— — — — — — — — — — —
◈ اسمك ⇐ {user.first_name if user else 'يا متمرد'}
◈ ايديك ⇐ `{user_id}`
— — — — — — — — — — —
**🛡️ في عالم المتمرد، الأمن ليس خياراً بل هوية.**
**أعتز بخصوصية عالمي، وأقدر تواصلك الراقي.**
— — — — — — — — — — —
**- نـظام الـرد الـآلي | الـمتمرد الـتقني 🤖🦅**
"""
        # الرد المباشر
        await event.reply(protection_msg)

# أوامر التحكم (تعمل من حسابك الأساسي فقط)
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.(سماح|رفض|فحص|قلك)"))
async def rebel_commands(event):
    cmd = event.pattern_match.group(1)
    user_id = event.chat_id
    
    if cmd == "سماح":
        if user_id not in allowed_users: allowed_users.append(user_id)
        await event.edit("**✅ تـم الـسماح لـهذا الـمستخدم.**")
    elif cmd == "رفض":
        if user_id in allowed_users: allowed_users.remove(user_id)
        await event.edit("**❌ تـم إلـغاء الـسماح، الـحماية تـعمل!**")
    elif cmd == "فحص":
        await event.edit("**🚀 الـمتمرد يـحلق بـنجاح!**")
    elif cmd == "قلك":
        await event.edit("**- قـال الـمتمرد: الـعقول الـعظيمة تـبني الـأكواد.. 🦅**")
