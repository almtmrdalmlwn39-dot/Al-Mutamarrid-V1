import os
import asyncio
from telethon import events

# 1. أمر السحب (سحب ميديا مقيدة)
@events.register(events.NewMessage(pattern=r'\.سحب', outgoing=True))
async def steal(event):
    if not event.is_reply:
        return await event.edit("**⚠️ يجب الرد على الرسالة!**")
    
    reply = await event.get_reply_message()
    if not reply.media:
        return await event.edit("**⚠️ رد على صورة أو فيديو!**")

    await event.edit("**🚀 جاري سحب المحتوى...**")
    path = await reply.download_media()
    await event.client.send_file("me", path, caption="**🛡️ تم السحب بواسطة المتمرد التقني!**")
    await event.edit("**✅ تمت العملية بنجاح! راجع رسائلك المحفوظة.**")
    if os.path.exists(path): os.remove(path)

# 2. أمر التحويل (ملصق لصورة والعكس)
@events.register(events.NewMessage(pattern=r'\.تحويل', outgoing=True))
async def convert(event):
    if not event.is_reply:
        return await event.edit("**⚠️ يجب الرد على الرسالة!**")
    
    reply = await event.get_reply_message()
    await event.edit("**🔄 جاري التحويل...**")
    path = await reply.download_media()
    
    if reply.sticker:
        await event.client.send_file(event.chat_id, path, caption="**✅ تم التحويل من ملصق لصورة!**")
    else:
        await event.client.send_file(event.chat_id, path, sticker=True)
        
    await event.delete()
    if os.path.exists(path): os.remove(path)

# 3. أمر كشف سجل الأسماء (الميزة الجديدة)
@events.register(events.NewMessage(pattern=r'\.سجل', outgoing=True))
async def name_history(event):
    reply = await event.get_reply_message()
    if not reply:
        return await event.edit("⚠️ **يجب الرد على الشخص لكشف سجل أسمائه!**")
    
    user_id = reply.sender_id
    await event.edit("⏳ **جاري اختراق أرشيف الأسماء...**")

    try:
        async with event.client.conversation("@SangMata_BOT") as conv:
            await conv.send_message(f"{user_id}")
            response = await conv.get_response()
            await event.client.send_read_acknowledge("@SangMata_BOT")
            
            history_text = response.text
            await event.edit(f"🕵️‍♂️ **سجل تغييرات الأسماء للايدي** `{user_id}`:\n\n{history_text}")
    except Exception:
        await event.edit("❌ **فشل الوصول للبوت المساعد!** تأكد من تفعيل @SangMata_BOT أولاً.")

# 4. أمر كشف معلومات الحساب (ID + BIO)
@events.register(events.NewMessage(pattern=r'\.كشف', outgoing=True))
async def deep_info(event):
    reply = await event.get_reply_message()
    user = await event.client.get_entity(reply.sender_id if reply else event.chat_id)
    
    await event.edit("🔍 **جاري سحب المعلومات العميقة...**")
    
    info = f"""
👤 **الاسم:** {user.first_name}
🆔 **الايدي:** `{user.id}`
🔗 **المعرف:** @{user.username if user.username else 'لا يوجد'}
🤖 **حساب بوت:** {'نعم' if user.bot else 'لا'}
🛠️ **سورس المتمرد التقني**
"""
    await event.edit(info)
