import asyncio
import os
from telethon import events, functions, types
from __main__ import client 

# إعدادات المملكة
GROUP_NAME = "سجل رسائل المتمرد التقني 📥"
STORAGE_CACHE = {"id": None} # ذاكرة مؤقتة لتسريع الأداء

async def get_log_group():
    """دالة ذكية تبحث عن الجروب وتخزن الأيدي لتوفير الجهد"""
    if STORAGE_CACHE["id"]:
        return STORAGE_CACHE["id"]
        
    async for dialog in client.iter_dialogs():
        if dialog.is_group and dialog.name == GROUP_NAME:
            STORAGE_CACHE["id"] = dialog.id
            return dialog.id
    return None

@client.on(events.NewMessage(pattern=r"\.انشاء تخزين", outgoing=True))
async def create_fakhama_log(event):
    await event.edit("**جـاري تـأسـيـس مـمـلـكـة الـتـخـزيـن الـفـخـمـة... 🔥**")
    try:
        existing_group = await get_log_group()
        if existing_group:
            return await event.edit(f"**المملكة موجودة بالفعل! ✅\nالأيدي:** `{existing_group}`")

        me = await client.get_me()
        result = await client(functions.channels.CreateChannelRequest(
            title=GROUP_NAME,
            about="تخزين مشفر وفخم لرسائل المتمرد التقني. 📡",
            megagroup=True
        ))
        
        log_id = int(f"-100{result.chats[0].id}")
        STORAGE_CACHE["id"] = log_id

        # وضع لمسة الفخامة (الصورة)
        photos = await client.get_profile_photos(me.id)
        if photos:
            path = await client.download_media(photos[0])
            await client(functions.channels.EditPhotoRequest(
                channel=log_id, photo=await client.upload_file(path)
            ))
            if os.path.exists(path): os.remove(path)

        await client.send_message(log_id, "**✅ تـم تـفعيل بـروتوكول الـتخزين الـشامل.**")
        await event.edit(f"**تـم الإنـشاء بـنجاح! 📥\nالأيدي:** `{log_id}`")
    except Exception as e:
        await event.edit(f"**⚠️ عـذراً مـتمرد، حـدث خـطأ:** {e}")

# --- نظام التخزين السيبراني اللحظي ---
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def auto_log_messages(event):
    # لا نخزن رسائل البوتات أو القنوات، فقط الأشخاص
    if event.is_private and not event.is_bot:
        try:
            log_id = await get_log_group()
            if not log_id:
                return # الجروب مش موجود

            sender = await event.get_sender()
            name = sender.first_name or "مستخدم مخفي"
            
            # إرسال معلومات المرسل قبل التوجيه (اختياري للفخامة)
            info_text = f"👤 **مـرسل جديد:** [{name}](tg://user?id={event.sender_id})\n🆔 **الأيدي:** `{event.sender_id}`"
            
            # توجيه الرسالة فوراً للمملكة
            await client.send_message(log_id, info_text)
            await event.forward_to(log_id)
            
        except Exception as e:
            print(f"❌ خطأ في نظام التخزين: {e}")
