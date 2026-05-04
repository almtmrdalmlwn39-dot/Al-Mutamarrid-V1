import os
import asyncio
from telethon import events
from __main__ import client  # استدعاء العميل من الملف الرئيسي

# --- أمر سحب الميديا المقيدة ---
@client.on(events.NewMessage(pattern=r"\.سحب", outgoing=True))
async def steal(event):
    if not event.is_reply:
        return await event.edit("**⚠️ يجب الرد على الرسالة أولاً!**")
    
    reply = await event.get_reply_message()
    if not reply.media:
        return await event.edit("**⚠️ يجب الرد على صورة أو فيديو!**")
    
    await event.edit("**🚀 جاري سحب المحتوى...**")
    
    try:
        path = await reply.download_media()
        # إرسال المحتوى لنفسك (الرسائل المحفوظة)
        await client.send_file("me", path, caption="**✅ تم سحب المحتوى بنجاح بواسطة المتمرد 🦅**")
        await event.edit("**✅ بنجاح! راجع رسائلك المحفوظة.**")
        
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        await event.edit(f"**❌ حدث خطأ أثناء السحب: `{str(e)}`**")

# --- أمر الفحص السريع ---
@client.on(events.NewMessage(pattern=r"\.فحص", outgoing=True))
async def ping(event):
    await event.edit("**⚡ سورس المتمرد يعمل بنجاح!**")
