from telethon import events
from __main__ import client

# 1. ميزة الكتم (Mute)
@client.on(events.NewMessage(pattern=r'\.كتم', outgoing=True))
async def mute(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        try:
            from telethon.tl.functions.channels import EditBannedRequest
            from telethon.tl.types import ChatBannedRights
            await client(EditBannedRequest(event.chat_id, reply.sender_id, ChatBannedRights(until_date=None, send_messages=True)))
            await event.edit("**🔇 تم كتم الشخص بنجاح!**")
        except: await event.edit("**⚠️ لست مشرفاً!**")

# 2. ميزة إلغاء الكتم (Unmute)
@client.on(events.NewMessage(pattern=r'\.الغاء كتم', outgoing=True))
async def unmute(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        try:
            await client.edit_permissions(event.chat_id, reply.sender_id, send_messages=True)
            await event.edit("**🔊 تم إلغاء الكتم، خلوه يتكلم!**")
        except: await event.edit("**⚠️ فشلت العملية!**")

# 3. ميزة "رد المتمرد" (الرد التلقائي)
@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    if 'يا متمرد' in event.raw_text:
        await event.reply("**لبييييه! المتمرد @Vi_ti0 يسمعك، إيش تشتي؟ 😎**")
    if event.raw_text == 'السلام عليكم':
        await event.reply("**وعليكم السلام ورحمة الله وبركاته، نورت يا غالي! ✨**")
