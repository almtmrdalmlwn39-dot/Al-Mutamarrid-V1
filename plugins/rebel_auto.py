from telethon import events, functions, types
import asyncio
import os
from datetime import datetime
from __main__ import client

# --- إعدادات المملكة والتحكم ---
allowed_users = []
message_counts = {} # إضافة عداد الرسائل للحظر
GROUP_NAME = "سجل رسائل المتمرد التقني 🦅🛡️"
STORAGE_CACHE = {"id": None}

async def get_log_group():
    """البحث عن الجروب آلياً بدون الحاجة لأيدي ثابت"""
    if STORAGE_CACHE["id"]: return STORAGE_CACHE["id"]
    async for dialog in client.iter_dialogs():
        if dialog.is_group and dialog.name == GROUP_NAME:
            STORAGE_CACHE["id"] = dialog.id
            return dialog.id
    return None

# 1. نظام الرد التلقائي المطور (صورة + تحذير + تخزين + صيد مخفي + حظر)
@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    # الرد في الخاص فقط وللرسائل الواردة
    if event.is_private and not event.out:
        if event.sender_id in allowed_users: return
        user = await event.get_sender()
        if user and user.bot: return
        
        user_id = event.sender_id
        log_id = await get_log_group()

        # [أ] نظام الحظر التلقائي إذا تجاوز 5 رسائل
        message_counts[user_id] = message_counts.get(user_id, 0) + 1
        if message_counts[user_id] > 5:
            await event.reply("**⚠️ تـم حـظرك تـلقائياً لـتجاوزك حـد الـمراسلة المسموح (5 رسائل).**")
            await client(functions.contacts.BlockRequest(id=user_id))
            return

        # [ب] صيد الوسائط المخفية (الصور والفيديوهات ذاتية التدمير)
        if event.media and log_id:
            if hasattr(event.media, 'ttl_seconds') and event.media.ttl_seconds:
                try:
                    file = await event.download_media()
                    cap = f"**⚠️ تـم صـيد مـيديا مـخفية!**\n**👤 مـن:** {user.first_name}\n**🆔 الآيـدي:** `{user_id}`"
                    await client.send_file(log_id, file, caption=cap)
                    if os.path.exists(file): os.remove(file)
                except: pass

        # [ج] جلب صورتك الشخصية والرد (يتم الرد في أول رسالة فقط لتجنب السبام)
        if message_counts[user_id] == 1:
            photos = await client.get_profile_photos("me", limit=1)
            msg = f"""
**- أهـلاً بـك فـي مـعقل الـمتمرد الـتقني 🛡️🦅**
— — — — — — — — — — —
◈ الـاسم ⇐ {user.first_name}
◈ الآيـدي ⇐ `{user_id}`
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
                    await client.send_file(event.chat_id, photos[0], caption=msg, reply_to=event.id)
                else:
                    await event.reply(msg)
            except: pass

        # إرسال نسخة من الرسالة إلى "المملكة"
        if log_id:
            user_info = f"[{user.first_name}](tg://user?id={user_id})"
            log_text = f"**📥 رسـالة جـديدة مـن:** {user_info}\n**🆔 الآيـدي:** `{user_id}`\n**💬 الـنص:**\n{event.text}"
            await client.send_message(log_id, log_text)

# 2. أمر إنشاء التخزين (المملكة الجديدة مع وضع الصورة)
@client.on(events.NewMessage(pattern=r"\.انشاء تخزين", outgoing=True))
async def create_storage(event):
    await event.edit("**- جـاري تـأسيس مـملكة الـتخزين الـجديدة وضبط الصورة... 🏗️**")
    try:
        result = await client(functions.channels.CreateChannelRequest(
            title=GROUP_NAME, 
            about="تخزين المتمرد التقني للمراسلات المهمة", 
            megagroup=True
        ))
        new_id = result.chats[0].id
        STORAGE_CACHE["id"] = new_id
        
        # إضافة ميزة وضع صورتك الشخصية للجروب المنشأ
        photos = await client.get_profile_photos("me", limit=1)
        if photos:
            await client(functions.channels.EditPhotoRequest(channel=new_id, photo=photos[0]))
            
        await event.edit(f"**✅ تـم تـجديد الـمملكة وضبط الصورة بـنجاح!**\n**🆔 الآيـدي:** `{new_id}`")
    except Exception as e:
        await event.edit(f"**❌ حـدث خـطأ: {e}**")

# 3. أوامر التحكم السريعة
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
