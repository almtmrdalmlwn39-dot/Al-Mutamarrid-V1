import asyncio
from telethon import events, functions, types
from main import client, CMD_HELP, SUDO_USERS

REBEL_NAME = "𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗧𝗘𝗖𝗛"
WAR_IDENTITY = f"**𓄂 {REBEL_NAME} 𝗦𝗢𝗨Ｒ𝗖𝗘 🛡️**"

PRIVATE_PROTECTION = True 
private_log = {}

CMD_HELP.update({
    "الخصوصية والترحيب": [
        "تفعيل الحماية", "تعطيل الحماية", "قفل الحساب", "تدمير", "انهاء"
    ]
})

@client.on(events.NewMessage(outgoing=True, pattern=r"\.تفعيل الحماية"))
async def enable_p(event):
    global PRIVATE_PROTECTION
    PRIVATE_PROTECTION = True
    await event.edit(f"**✅ تم تفعيل درع حماية الخاص لـ {REBEL_NAME}.**")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.تعطيل الحماية"))
async def disable_p(event):
    global PRIVATE_PROTECTION
    PRIVATE_PROTECTION = False
    await event.edit(f"**𓄴 تم تعطيل حماية الخاص بنجاح.**")

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def private_guard_system(event):
    if event.out or not PRIVATE_PROTECTION:
        return
    sender = await event.get_sender()
    user_id = event.sender_id
    
    if user_id in SUDO_USERS or (sender and sender.bot):
        return

    # 1. إرسال الترحيب الفخم عند أول رسالة
    if user_id not in private_log:
        private_log[user_id] = 4  # عدد التحذيرات المتاحة له بعد الترحيب
        
        me = await client.get_me()
        my_name = me.first_name if me.first_name else "صاحب الحساب"
        photos = await client.get_profile_photos("me")
        
        welcome_text = (
            f"**مرحباً بك.. ✨**\n\n"
            f"**أهلاً بك في خاص حـسـاب ({my_name})**\n"
            f"**فضلاً، اترك رسالتك أو سبب تواصلك هنا بوضوح،**\n"
            f"**وسيتم الرد عليك في أقرب وقت ممكن فور التواجد.**\n\n"
            f"**🆔 آيديك:** `{user_id}`\n"
            f"**— — — — — — — — — — — —**\n"
            f"{WAR_IDENTITY}"
        )
        try:
            if photos:
                await client.send_file(event.chat_id, photos[0], caption=welcome_text)
            else:
                await event.reply(welcome_text)
        except:
            await event.reply(welcome_text)
        return

    # 2. إرسال تحذير في كل رسالة أخرى يقوم بإرسالها
    private_log[user_id] -= 1
    remains = private_log[user_id]

    if remains > 0:
        await event.reply(f"**⚠️ تنبيه: يرجى الانتظار دون تكرار الرسائل. متبقي لك ({remains}) محاولات قبل الحظر التلقائي.**")
    else:
        # 3. الحظر النهائي عند انتهاء المحاولات
        try:
            await client(functions.contacts.BlockRequest(id=user_id))
            await event.reply(f"**🚫 تم حظرك تلقائياً لتجاوزك حد المحاولات وتكرار الإزعاج.**")
            if user_id in private_log:
                del private_log[user_id]
        except:
            pass

# تصفير العداد وإلغاء الرصد إذا قمت أنت بمراسلته أو الرد عليه
@client.on(events.NewMessage(outgoing=True, func=lambda e: e.is_private))
async def clear_user_log(event):
    user_id = event.chat_id
    if user_id in private_log:
        del private_log[user_id]

@client.on(events.NewMessage(outgoing=True, pattern=r"\.قفل الحساب"))
async def hide_everything(event):
    await event.edit(f"**🛡️ جـاري تـفعيل وضـع الـشبح لـ {REBEL_NAME}...**")
    try:
        await client(functions.account.SetPrivacyRequest(key=types.InputPrivacyKeyPhoneNumber(), rules=[types.InputPrivacyValueDisallowAll()]))
        await client(functions.account.SetPrivacyRequest(key=types.InputPrivacyKeyStatusTimestamp(), rules=[types.InputPrivacyValueDisallowAll()]))
        await client(functions.account.SetPrivacyRequest(key=types.InputPrivacyKeyProfilePhoto(), rules=[types.InputPrivacyValueDisallowAll()]))
        await event.edit(f"**✅ تم تفعيل درع الخصوصية بنجاح.**\n{WAR_IDENTITY}")
    except Exception as e:
        await event.edit(f"**⚠️ فـشل في الإعدادات:** `{e}`")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.تدمير"))
async def destroy_chat(event):
    if not event.is_private: return
    await event.edit("**🧨 جـاري تـطـهـير الـسجلات مـن الـطرفـين...**")
    async for msg in client.iter_messages(event.chat_id):
        await msg.delete(revoke=True)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.انهاء"))
async def end_user(event):
    if not event.is_private: return
    await client(functions.contacts.BlockRequest(event.chat_id))
    await event.edit(f"**🚫 تـم إنـهـاء الـمستخدم بـواسطة {REBEL_NAME}.**")
