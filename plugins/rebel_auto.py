from telethon import events, functions, types
import asyncio  # ضروري جداً عشان ما يطلع خطأ
import os
import pytz # ضروري للوقت
from datetime import datetime
from __main__ import client

# --- إعدادات المملكة والتحكم ---
allowed_users = []
message_counts = {} 
LOG_GROUP_ID = -1002446700860 

@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    # نشتغل فقط في الخاص والرسائل اللي جاية لك
    if event.is_private and not event.out:
        user_id = event.sender_id
        
        # إذا كان الشخص مسموح له، لا ترد عليه تلقائياً
        if user_id in allowed_users: return
        
        user = await event.get_sender()
        if user and user.bot: return

        # [أ] نظام الحظر التلقائي (بعد 5 رسائل)
        message_counts[user_id] = message_counts.get(user_id, 0) + 1
        if message_counts[user_id] > 5:
            await event.reply("**⚠️ تم حظرك نهائياً لتجاهلك التحذيرات وتجاوز حد المراسلة.**")
            await client(functions.contacts.BlockRequest(id=user_id))
            return

        # [ب] صيد الوسائط المخفية
        if event.media:
            if hasattr(event.media, 'ttl_seconds') and event.media.ttl_seconds:
                try:
                    file = await event.download_media()
                    cap = f"**⚠️ تم صيد ميديا مخفية!**\n**👤 من:** {user.first_name}\n**🆔 الآيدي:** `{user_id}`"
                    await client.send_file(LOG_GROUP_ID, file, caption=cap)
                    if os.path.exists(file): os.remove(file)
                except: pass

        # [ج] الرد التلقائي (التحذير الفوري من أول رسالة)
        if message_counts[user_id] == 1:
            photos = await client.get_profile_photos("me", limit=1)
            msg = f"""
**- أهـلاً بـك فـي مـعقل الـمتمرد الـتقني 🛡️🦅**
— — — — — — — — — — —
◈ الـاسم ⇐ {user.first_name}
◈ الآيـدي ⇐ `{user_id}`
— — — — — — — — — — —
**⚠️ تـحذير أمـني فـوري :**
**- جـاري فـحص بـياناتك والـتأكد مـن هـويتك الآن..**
**- يـمنع إرسـال أكـثر مـن 5 رسـائل لـتجنب الـحظر الـتلقائي.**
— — — — — — — — — — —
**🛡️ في عالم المتمرد، الأمن ليس خياراً بل هوية.**
"""
            try:
                if photos:
                    await client.send_file(event.chat_id, photos[0], caption=msg, reply_to=event.id)
                else:
                    await event.reply(msg)
            except: pass

        # --- التخزين في المملكة ---
        try:
            user_info = f"[{user.first_name}](tg://user?id={user_id})"
            text_to_log = event.text if event.text else "أرسل وسائط/ملف"
            log_text = f"**📥 رسـالة جـديدة مـن:** {user_info}\n**🆔 الآيـدي:** `{user_id}`\n**💬 الـنص:**\n{text_to_log}"
            await client.send_message(LOG_GROUP_ID, log_text)
        except: pass

# أوامر التحكم
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.(سماح|رفض|فحص)"))
async def control(event):
    cmd = event.pattern_match.group(1)
    if cmd == "سماح":
        if event.chat_id not in allowed_users: allowed_users.append(event.chat_id)
        await event.edit("**✅ تـم الـسماح.**")
    elif cmd == "رفض":
        if event.chat_id in allowed_users: allowed_users.remove(event.chat_id)
        await event.edit("**❌ تـم إلغاء الـسماح.**")
    elif cmd == "فحص":
        await event.edit("**🚀 الـمتمرد شـغال مـية مـية!**")
