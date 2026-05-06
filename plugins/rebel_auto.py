from telethon import events, functions, types
import asyncio
import os
from datetime import datetime
from __main__ import client

# --- إعدادات المملكة والتحكم ---
allowed_users = []
message_counts = {} 
LOG_GROUP_ID = -1002446700860 

@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    if event.is_private and not event.out:
        if event.sender_id in allowed_users: return
        user = await event.get_sender()
        if user and user.bot: return
        
        user_id = event.sender_id

        # [أ] نظام الحظر التلقائي (البلوك النهائي بعد 5 رسائل)
        message_counts[user_id] = message_counts.get(user_id, 0) + 1
        if message_counts[user_id] > 5:
            await event.reply("**⚠️ تم حظرك نهائياً لتجاهلك التحذيرات وتجاوز حد المراسلة.**")
            await client(functions.contacts.BlockRequest(id=user_id))
            return

        # [ب] صيد الوسائط المخفية (ذاتية التدمير)
        if event.media:
            if hasattr(event.media, 'ttl_seconds') and event.media.ttl_seconds:
                try:
                    file = await event.download_media()
                    cap = f"**⚠️ تم صيد ميديا مخفية!**\n**👤 من:** {user.first_name}\n**🆔 الآيدي:** `{user_id}`"
                    await client.send_file(LOG_GROUP_ID, file, caption=cap)
                    if os.path.exists(file): os.remove(file)
                except: pass

        # [ج] الرد التلقائي مع التحذير الفوري (يظهر في أول رسالة فقط)
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

        # --- إرسال نسخة للتخزين في المملكة ---
        try:
            user_info = f"[{user.first_name}](tg://user?id={user_id})"
            text_to_log = event.text if event.text else "أرسل وسائط/ملف"
            log_text = f"**📥 رسـالة جـديدة مـن:** {user_info}\n**🆔 الآيـدي:** `{user_id}`\n**💬 الـنص:**\n{text_to_log}"
            await client.send_message(LOG_GROUP_ID, log_text)
        except Exception as e:
            print(f"Error: {e}")

# (بقية الأوامر .انشاء تخزين و .سماح تبقى كما هي)
