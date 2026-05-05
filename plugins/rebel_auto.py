import asyncio
from telethon import events, functions

# محاولة جلب الكلاينت بأكثر من طريقة لضمان العمل
try:
    import main
    client = main.client
except:
    from __main__ import client

AUTO_IDENTITY = "**- نـظام الـرد الـآلي | الـمتمرد الـتقني 🤖🦅**"
allowed_users = []

@client.on(events.NewMessage(incoming=True))
async def private_handler(event):
    # الرد فقط في الخاص وعلى الرسائل الواردة من الآخرين
    if event.is_private and not event.out:
        user_id = event.sender_id
        if user_id in allowed_users:
            return

        user = await event.get_sender()
        # نص الترحيب والتحذير مع عبارة الأمن السيبراني
        msg = f"""
**- أهـلاً بـك فـي مـعقل الـمتمرد الـتقني 🛡️**
— — — — — — — — — — —
◈ اسمك ⇐ {user.first_name}
◈ ايديك ⇐ `{user_id}`
— — — — — — — — — — —
**🛡️ في عالم المتمرد، الأمن ليس خياراً بل هوية. 
أعتز بخصوصية عالمي، وأقدر تواصلك الراقي. 
جاري معالجة طلبك.. كن صبوراً. 🦅**
— — — — — — — — — — —
{AUTO_IDENTITY}
"""
        try:
            # إرسال صورة بروفايله لإبهاره
            photos = await client.get_profile_photos(user_id)
            if photos:
                await client.send_file(event.chat_id, photos[0], caption=msg)
            else:
                await event.reply(msg)
        except:
            await event.reply(msg)

# أوامر التحكم (سماح ورفض وقلك)
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.(سماح|رفض|قلك)"))
async def commands(event):
    cmd = event.pattern_match.group(1)
    if cmd == "سماح":
        allowed_users.append(event.chat_id)
        await event.edit("**✅ تـم الـسماح.**")
    elif cmd == "رفض":
        if event.chat_id in allowed_users: allowed_users.remove(event.chat_id)
        await event.edit("**❌ تـم الـرفض.**")
    elif cmd == "قلك":
        await event.edit("**- قـال لـك الـمتمرد الـتقني :**\n**الـعقول الـعظيمة تـبني الـأكواد.. 🦅**")
