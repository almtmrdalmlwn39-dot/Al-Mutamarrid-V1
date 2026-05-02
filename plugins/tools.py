import os
import asyncio
from telethon import events
from __main__ import client

# 1. أمر السحب (سحب ميديا مقيدة)
@client.on(events.NewMessage(pattern=r'\.سحب', outgoing=True))
async def steal(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        if reply.media:
            await event.edit("**🚀 جاري سحب المحتوى...**")
            path = await reply.download_media()
            await client.send_file("me", path, caption="**🛡️ تم السحب بواسطة المتمرد التقني!**")
            await event.edit("**✅ تمت العملية بنجاح! راجع رسائلك المحفوظة.**")
            if os.path.exists(path): os.remove(path)
        else: await event.edit("**⚠️ رد على صورة أو فيديو!**")
    else: await event.edit("**⚠️ يجب الرد على الرسالة!**")

# 2. أمر التحويل (ملصق لصورة والعكس)
@client.on(events.NewMessage(pattern=r'\.تحويل', outgoing=True))
async def convert(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        await event.edit("**🔄 جاري التحويل...**")
        path = await reply.download_media()
        if reply.sticker:
            await client.send_file(event.chat_id, path, caption="**✅ تم التحويل بنجاح!**")
        else:
            await client.send_file(event.chat_id, path, sticker=True)
        await event.delete()
        if os.path.exists(path): os.remove(path)

