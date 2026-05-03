from telethon import events
from __main__ import client

# 1. كشف الرسائل المحذوفة
@client.on(events.MessageDeleted)
async def deleted_logger(event):
    for msg_id in event.deleted_ids:
        # يمكنك جعل البوت يرسل الرسائل المحذوفة لـ "الرسائل المحفوظة" عندك
        await client.send_message("me", f"**- تم حذف رسالة بالايدي: `{msg_id}`**\n**- في الدردشة: `{event.chat_id}`**")

# 2. كشف الرسائل المعدلة
@client.on(events.MessageEdited)
async def edited_logger(event):
    if event.is_private:
        old_text = event.message.text
        await client.send_message("me", f"**- تم تعديل رسالة في الخاص 🛡️**\n**- النص الجديد: {old_text}**")

# 3. امر فحص السرعة (بينغ)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.بينج"))
async def ping(event):
    start = datetime.now()
    await event.edit("**- جاري فحص سرعة الاستجابة...**")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(f"**- سرعة استجابة المتمرد: `{ms}` ملي ثانية ⚡**")
