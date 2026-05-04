from telethon import events, functions, types
import os
import asyncio
# السطر الذهبي عشان يشتغل الملف الفرعي
from __main__ import client 

# اسم الجروب الثابت لكي لا يتكرر الإنشاء
GROUP_NAME = "سجل رسائل المتمرد التقني 📥"

async def get_log_group(bot_client):
    """دالة ذكية للبحث عن الجروب أو إنشائه"""
    async for dialog in bot_client.iter_dialogs():
        if dialog.is_group and dialog.name == GROUP_NAME:
            return dialog.id
    return None

@client.on(events.NewMessage(pattern=r"\.انشاء تخزين", outgoing=True))
async def create_fakhama_log(event):
    await event.edit("**جـاري تـأسـيـس مـمـلـكـة الـتـخـزيـن الـفـخـمـة... 🔥**")
    
    try:
        # التأكد إذا كان الجروب موجود مسبقاً
        existing_group = await get_log_group(client)
        if existing_group:
            return await event.edit(f"**المملكة موجودة بالفعل يا متمرد! ✅**\n**الأيدي:** `{existing_group}`")

        me = await client.get_me()
        
        # 1. إنشاء الجروب
        result = await client(functions.channels.CreateChannelRequest(
            title=GROUP_NAME,
            about="تخزين خاص ومشفر لرسائل المطور [المتمرد].",
            megagroup=True
        ))
        
        created_chat_id = result.chats[0].id
        log_id = int(f"-100{created_chat_id}")
        
        # 2. وضع صورة الحساب للجروب
        await event.edit("**جـاري وضـع لـمـسـة الـفـخـامة عـلـى الـجـروب... ✨**")
        photos = await client.get_profile_photos(me.id)
        if photos:
            photo_path = await client.download_media(photos[0])
            await client(functions.channels.EditPhotoRequest(
                channel=log_id,
                photo=await client.upload_file(photo_path)
            ))
            if os.path.exists(photo_path): os.remove(photo_path)

        # 3. رسالة الترحيب
        await client.send_message(log_id, f"**‹ تـم تـأسـيـس مـمـلـكـة الـتـخـزيـن بـنـجـاح ✅ ›**\n**الـمـطـور:** [{me.first_name}](tg://user?id={me.id})")
        
        await event.edit(f"**تـم الإنـشـاء بـفـخـامـة! ✅**\n**الأيدي:** `{log_id}`")
        
    except Exception as e:
        await event.edit(f"**حدث خطأ أثناء الإنشاء:** {e}")

# --- دالة تحويل الرسائل التلقائية ---
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def auto_log_messages(event):
    if event.is_bot: return
    sender = await event.get_sender()
    if not sender: return

    # البحث عن الجروب لإرسال الرسالة إليه
    log_id = await get_log_group(client)
    if not log_id: return

    try:
        log_caption = f"**📥 رسالة من: [{sender.first_name}](tg://user?id={sender.id})\n🆔 الأيدي: `{sender.id}`**"
        await client.send_message(log_id, log_caption)
        await client.forward_messages(log_id, event.message)
    except:
        pass
