import os
import asyncio
from telethon import events

# --- 1. أمر سحب الميديا المقيدة ---
@events.register(events.NewMessage(pattern=r"\.سحب", outgoing=True))
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
        await event.client.send_file("me", path, caption="**✅ تم سحب الميديا بنجاح بواسطة سورس المتمرد**")
        await event.edit("**✅ بنجاح! راجع رسائلك المحفوظة.**")
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        await event.edit(f"**❌ حدث خطأ أثناء السحب:** `{str(e)}`")

# --- 2. أمر الفحص السريع ---
@events.register(events.NewMessage(pattern=r"\.فحص", outgoing=True))
async def ping(event):
    await event.edit("**⚡ سورس المتمرد يعمل بنجاح!**")
