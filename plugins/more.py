from telethon import events, functions, types
from __main__ import client

# قائمة لتخزين المعرفات المكتومة في الخاص
muted_users = []

# 1. ميزة الكتم (Mute) - تعمل في المجموعات والخاص
@client.on(events.NewMessage(pattern=r'\.كتم', outgoing=True))
async def mute(event):
    if not event.is_reply:
        return await event.edit("**⚠️ يرجى الرد على الشخص لكتمه!**")
    
    reply = await event.get_reply_message()
    user_id = reply.sender_id

    if event.is_private:
        # كتم في الخاص (إضافة للقائمة لحذف رسائله)
        if user_id not in muted_users:
            muted_users.append(user_id)
            await event.edit("**🔇 تم كتم الشخص في الخاص (سيتم حذف رسائله تلقائياً)!**")
        else:
            await event.edit("**⚠️ الشخص مكتوم بالفعل في الخاص.**")
    else:
        # كتم في المجموعات (صلاحيات مشرف)
        try:
            from telethon.tl.functions.channels import EditBannedRequest
            from telethon.tl.types import ChatBannedRights
            await client(EditBannedRequest(event.chat_id, user_id, ChatBannedRights(until_date=None, send_messages=True)))
            await event.edit("**🔇 تم كتم الشخص في المجموعة بنجاح!**")
        except:
            await event.edit("**⚠️ لست مشرفاً أو لا أملك صلاحيات الكتم هنا!**")

# 2. ميزة إلغاء الكتم (Unmute)
@client.on(events.NewMessage(pattern=r'\.الغاء كتم', outgoing=True))
async def unmute(event):
    if not event.is_reply:
        return await event.edit("**⚠️ يرجى الرد على الشخص لإلغاء كتمه!**")
    
    reply = await event.get_reply_message()
    user_id = reply.sender_id

    if event.is_private:
        if user_id in muted_users:
            muted_users.remove(user_id)
            await event.edit("**🔊 تم إلغاء كتم الشخص في الخاص.**")
        else:
            await event.edit("**⚠️ الشخص ليس مكتوماً في الخاص.**")
    else:
        try:
            await client.edit_permissions(event.chat_id, user_id, send_messages=True)
            await event.edit("**🔊 تم إلغاء الكتم في المجموعة، خلوه يتكلم!**")
        except:
            await event.edit("**⚠️ فشلت العملية، تأكد من صلاحياتك!**")

# 3. محرك الحذف التلقائي للمكتومين في الخاص
@client.on(events.NewMessage(incoming=True))
async def watcher(event):
    if event.is_private and event.sender_id in muted_users:
        await event.delete()

# 4. ميزة "رد المتمرد" (الرد التلقائي)
@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    if 'يا متمرد' in event.raw_text:
        await event.reply("**لبييييه! المتمرد @Vi_ti0 يسمعك، إيش تشتي؟ 😎**")
    elif event.raw_text == 'السلام عليكم':
        await event.reply("**وعليكم السلام ورحمة الله وبركاته، نورت يا غالي! ✨**")
