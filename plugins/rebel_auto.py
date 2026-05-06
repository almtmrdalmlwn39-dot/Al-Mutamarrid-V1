from telethon import events, functions, types
import asyncio
from datetime import datetime
from __main__ import client

allowed_users = []

# 1. نظام الرد التلقائي المطور (مع الصورة والتحذير)
@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    if event.is_private and not event.out:
        if event.sender_id in allowed_users: return
        user = await event.get_sender()
        if user and user.bot: return
        
        # جلب صورة بروفايلك الحالية لإرسالها في الرد
        photos = await client.get_profile_photos("me", limit=1)
        
        msg = f"""
**- أهـلاً بـك فـي مـعقل الـمتمرد الـتقني 🛡️🦅**
— — — — — — — — — — —
◈ الـاسم ⇐ {user.first_name}
◈ الآيـدي ⇐ `{event.sender_id}`
— — — — — — — — — — —
**⚠️ تـحذير أمـني :**
**- جـاري فـحص بـياناتك والـتأكد مـن هـويتك..**
**- الـرجاء عـدم الـتكرار لـتجنب الـحظر الـتلقائي.**
— — — — — — — — — — —
**🛡️ في عالم المتمرد، الأمن ليس خياراً بل هوية.**
**- نـظام الـرد الـآلي | الـمتمرد الـتقني 🤖**
"""
        try:
            if photos:
                # إرسال الصورة مع النص
                await client.send_file(event.chat_id, photos[0], caption=msg, reply_to=event.id)
            else:
                # إذا لم توجد صورة، يرسل نص فقط
                await event.reply(msg)
        except Exception as e:
            print(f"Error: {e}")

# 2. أوامر التحكم
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.(سماح|رفض|فحص)"))
async def control(event):
    cmd = event.pattern_match.group(1)
    if cmd == "سماح":
        if event.chat_id not in allowed_users: allowed_users.append(event.chat_id)
        await event.edit("**✅ تـم الـسماح لـهذا الـمستخدم.**")
    elif cmd == "رفض":
        if event.chat_id in allowed_users: allowed_users.remove(event.chat_id)
        await event.edit("**❌ تـم إلـغاء الـسماح.**")
    elif cmd == "فحص":
        await event.edit("**🚀 الـمتمرد شـغال مـية مـية!**")
