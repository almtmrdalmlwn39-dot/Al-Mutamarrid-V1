from telethon import events
# استدعاء العميل من ملف main الأساسي وليس من __main__
import main 
client = main.client

# 1. أمر استخراج المعلومات (بالرد)
@client.on(events.NewMessage(pattern=r'\.معلومات', outgoing=True))
async def get_info(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        try:
            user = await client.get_entity(reply.sender_id)
            info_text = f"""
🛡️ **معلومات المستخدم:**
─── • ⚡️ • ───
🆔 **الايدي:** `{user.id}`
👤 **الاسم:** {user.first_name}
🏷️ **اليوزر:** @{user.username if user.username else 'لا يوجد'}
🛡️ **الحساب:** {"بوت" if user.bot else "شخصي"}
─── • ⚡️ • ───
"""
            await event.edit(info_text)
        except Exception as e:
            await event.edit(f"⚠️ خطأ: {e}")
    else:
        await event.edit("**⚠️ يرجى الرد على الشخص لجلب معلوماته!**")

# 2. أمر حذف الرسائل بسرعة
@client.on(events.NewMessage(pattern=r'\.حذف', outgoing=True))
async def delete_msg(event):
    if event.is_reply:
        msg = await event.get_reply_message()
        await msg.delete()
        await event.delete()
    else:
        await event.delete()

# 3. أمر الطرد (للمشرفين)
@client.on(events.NewMessage(pattern=r'\.طرد', outgoing=True))
async def kick_user(event):
    if not event.is_group:
        return await event.edit("**⚠️ هذا الأمر يستخدم في المجموعات فقط!**")
    
    if event.is_reply:
        reply = await event.get_reply_message()
        try:
            await client.kick_participant(event.chat_id, reply.sender_id)
            await event.edit("**✅ تم طرد العضو من المجموعه بنجاح!**")
        except:
            await event.edit("**⚠️ فشل الطرد، تأكد من صلاحيات المشرف!**")
    else:
        await event.edit("**⚠️ رد على الشخص الذي تود طرده!**")

# 4. أمر تثبيت الرسائل
@client.on(events.NewMessage(pattern=r'\.تثبيت', outgoing=True))
async def pin_msg(event):
    if event.is_reply:
        msg = await event.get_reply_message()
        try:
            await msg.pin()
            await event.edit("**📌 تم تثبيت الرسالة بنجاح!**")
        except:
            await event.edit("**⚠️ لا أملك صلاحيات التثبيت!**")
