from telethon import events, functions, types
import asyncio
from datetime import datetime
from __main__ import client

# --- إعدادات المملكة والتحكم ---
allowed_users = []
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

# 1. نظام الرد التلقائي المطور (صورة + تحذير + تخزين)
@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    # الرد في الخاص فقط وللرسائل الواردة
    if event.is_private and not event.out:
        if event.sender_id in allowed_users: return
        user = await event.get_sender()
        if user and user.bot: return
        
        # جلب صورتك الشخصية الحالية
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
            # الرد بالصورة
            if photos:
                await client.send_file(event.chat_id, photos[0], caption=msg, reply_to=event.id)
            else:
                await event.reply(msg)
            
            # إرسال نسخة من الرسالة إلى "المملكة" (التخزين)
            log_id = await get_log_group()
            if log_id:
                user_info = f"[{user.first_name}](tg://user?id={event.sender_id})"
                log_text = f"**📥 رسـالة جـديدة مـن:** {user_info}\n**🆔 الآيـدي:** `{event.sender_id}`\n**💬 الـنص:**\n{event.text}"
                await client.send_message(log_id, log_text)
        except: 
            pass

# 2. أمر إنشاء التخزين (المملكة الجديدة)
@client.on(events.NewMessage(pattern=r"\.انشاء تخزين", outgoing=True))
async def create_storage(event):
    await event.edit("**- جـاري تـأسيس مـملكة الـتخزين الـجديدة... 🏗️**")
    try:
        # إنشاء الجروب وتعيينه كمملكة
        result = await client(functions.channels.CreateChannelRequest(
            title=GROUP_NAME, 
            about="تخزين المتمرد التقني للمراسلات المهمة", 
            megagroup=True
        ))
        STORAGE_CACHE["id"] = result.chats[0].id
        await event.edit(f"**✅ تـم تـجديد الـمملكة بـنجاح!**\n**🆔 الآيـدي:** `{STORAGE_CACHE['id']}`")
    except Exception as e:
        await event.edit(f"**❌ حـدث خـطأ: {e}**")

# 3. أوامر التحكم السريعة
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.(سماح|رفض|فحص)"))
async def control(event):
    cmd = event.pattern_match.group(1)
    if cmd == "سماح":
        if event.chat_id not in allowed_users: allowed_users.append(event.chat_id)
        await event.edit("**✅ تـم الـسماح.**")
    elif cmd == "فحص":
        await event.edit("**🚀 الـمتمرد شـغال مـية مـية!**")
