from telethon import events
from __main__ import client

# كاشف الحذف المطور
@client.on(events.MessageDeleted)
async def deleted_logger(event):
    # ملاحظة: في المجموعات تليجرام يرسل الايدي فقط
    for msg_id in event.deleted_ids:
        await client.send_message("me", f"**- تم حذف رسالة بالايدي: `{msg_id}`**\n**- في الدردشة: `{event.chat_id}`**")

# كاشف التعديل (يعطيك الشخص والاسم)
@client.on(events.MessageEdited)
async def edited_logger(event):
    if event.sender:
        name = event.sender.first_name
        user_id = event.sender_id
        old_text = event.text
        chat_name = event.chat.title if event.is_group else "الخاص"
        
        log_msg = (
            f"**- تم تعديل رسالة 🛡️**\n"
            f"**- الشخص : [{name}](tg://user?id={user_id})**\n"
            f"**- الايدي : `{user_id}`**\n"
            f"**- المكان : {chat_name}**\n"
            f"**- النص الجديد : {old_text}**"
        )
        await client.send_message("me", log_msg)
