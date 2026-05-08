from telethon import events, functions, types
from main import client, CMD_HELP

# --- [ AL-MUTAMARRID GLOBAL IDENTITY ] ---
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"

# قائمة لتخزين المعرفات المكتومة في الخاص
muted_users = []

# تسجيل الأوامر في قائمة المساعدة
CMD_HELP.update({
    "أدوات السيطرة": [
        "كتم", "الغاء كتم", "الرد التفاعلي"
    ]
})

# --- [ 1. ميزة الكتم - MUTE ] ---
@client.on(events.NewMessage(pattern=r'\.كتم', outgoing=True))
async def mute(event):
    if not event.is_reply:
        return await event.edit("**⚠️ يرجى الرد على الشخص لكتمه!**")
    
    reply = await event.get_reply_message()
    user_id = reply.sender_id

    if event.is_private:
        if user_id not in muted_users:
            muted_users.append(user_id)
            await event.edit(f"**🔇 تم كتم الشخص في الخاص بنجاح!**\n\n{WAR_IDENTITY}")
        else:
            await event.edit("**⚠️ الشخص مكتوم بالفعل في الخاص.**")
    else:
        try:
            from telethon.tl.functions.channels import EditBannedRequest
            from telethon.tl.types import ChatBannedRights
            await client(EditBannedRequest(event.chat_id, user_id, ChatBannedRights(until_date=None, send_messages=True)))
            await event.edit(f"**🔇 تم كتم الشخص في المجموعة بنجاح!**\n\n{WAR_IDENTITY}")
        except:
            await event.edit("**⚠️ لست مشرفاً أو لا أملك صلاحيات الكتم هنا!**")

# --- [ 2. ميزة إلغاء الكتم - UNMUTE ] ---
@client.on(events.NewMessage(pattern=r'\.الغاء كتم', outgoing=True))
async def unmute(event):
    if not event.is_reply:
        return await event.edit("**⚠️ يرجى الرد على الشخص لإلغاء كتمه!**")
    
    reply = await event.get_reply_message()
    user_id = reply.sender_id

    if event.is_private:
        if user_id in muted_users:
            muted_users.remove(user_id)
            await event.edit(f"**🔊 تم إلغاء كتم الشخص في الخاص.**\n\n{WAR_IDENTITY}")
        else:
            await event.edit("**⚠️ الشخص ليس مكتوماً في الخاص.**")
    else:
        try:
            await client.edit_permissions(event.chat_id, user_id, send_messages=True)
            await event.edit(f"**🔊 تم إلغاء الكتم في المجموعة، خلوه يتكلم!**\n\n{WAR_IDENTITY}")
        except:
            await event.edit("**⚠️ فشلت العملية، تأكد من صلاحياتك!**")

# --- [ 3. محرك الحذف التلقائي للمكتومين ] ---
@client.on(events.NewMessage(incoming=True))
async def watcher(event):
    if event.is_private and event.sender_id in muted_users:
        await event.delete()

# --- [ 4. ميزة الرد الذكي والترحيب الملكي ] ---
@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    me = await client.get_me()
    owner_name = me.first_name 
    
    sender = await event.get_sender()
    sender_name = sender.first_name if sender.first_name else "يا طيب"
    
    msg = event.raw_text
    
    # الرد باسم صاحب الحساب
    if owner_name in msg:
        await event.reply(
            f"**لبييييه يا {sender_name}! {owner_name} يسمعك عبر 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘.. تفضل! 😎**"
        )
    
    # الرد بلقب المتمرد
    elif 'يا متمرد' in msg:
        await event.reply(
            f"**لبييييه يا {sender_name}! المتمرد معك عبر 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘.. ✨**"
        )
        
    # الترحيب الفخم
    elif msg == 'السلام عليكم':
        await event.reply(
            f"**وعليكم السلام ورحمة الله وبركاته.. حياك الله يا {sender_name} في رحاب {owner_name}! 𓄂**\n"
            f"**نورت الساحة بمرورك الملكي.. ✨**"
        )
