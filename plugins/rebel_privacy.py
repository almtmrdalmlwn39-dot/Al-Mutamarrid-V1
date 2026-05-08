import asyncio
from telethon import events, functions, types
from main import client, CMD_HELP, SUDO_USERS

# --- [ AL-MUTAMARRID TECH IDENTITY ] ---
# اسم المتمرد بالإنجليزية الفخمة كما طلبت
REBEL_NAME = "𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗧𝗘𝗖𝗛"
WAR_IDENTITY = f"**𓄂 {REBEL_NAME} 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"

# متغيرات الحالة والتخزين
PRIVATE_PROTECTION = True 
private_log = {} 

# تسجيل القسم في قائمة المساعدة
CMD_HELP.update({
    "الخصوصية والترحيب": [
        "تفعيل_الخاص", "تعطيل_الخاص", "قفل_الحساب", "تدمير", "انهاء"
    ]
})

# --- [ 1. أوامر التحكم بالدرع ] ---

@client.on(events.NewMessage(outgoing=True, pattern=r"\.تفعيل_الخاص"))
async def enable_p(event):
    global PRIVATE_PROTECTION
    PRIVATE_PROTECTION = True
    await event.edit(f"**✅ تم تفعيل درع {REBEL_NAME} للخاص.**")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.تعطيل_الخاص"))
async def disable_p(event):
    global PRIVATE_PROTECTION
    PRIVATE_PROTECTION = False
    await event.edit(f"**📴 تم تعطيل حماية {REBEL_NAME} بنجاح.**")

# --- [ 2. الترحيب ونظام الـ 5 تحذيرات ] ---

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def private_guard_system(event):
    if event.out or not PRIVATE_PROTECTION:
        return
    sender = await event.get_sender()
    user_id = event.sender_id
    
    if user_id in SUDO_USERS or (sender and sender.bot):
        return

    # أول رسالة: ترحيب عربي + الاسم بالإنجليزي + صورة بروفايلك
    if user_id not in private_log:
        private_log[user_id] = 5 
        photos = await client.get_profile_photos("me")
        welcome_text = (
            f"**🛡️ أهـلاً بـك فـي مـنـظومة {REBEL_NAME}**\n"
            f"**— — — — — — — — — — —**\n"
            f"**👤 أيـديـك:** `{user_id}`\n"
            f"**⚠️ لـديـك (5) مـحاولات قـبل الـحـظر الـتلقـائي.**\n"
            f"**— — — — — — — — — — —**\n"
            f"**𓄂 الـخـاص مـراقب تـقـنيـاً لـمنع الإزعاج 🛡️**\n\n"
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

    # نظام تناقص التحذيرات بالعربي
    private_log[user_id] -= 1
    remains = private_log[user_id]

    if remains > 0:
        await event.reply(f"**⚠️ تـنـبـيـه! تـبـقى لـك ({remains}) مـحـاولات فـقـط قـبـل الـحـظر.**")
    else:
        try:
            await client(functions.contacts.BlockRequest(id=user_id))
            await event.reply(f"**🚫 تـم حـظرك نـهـائـياً بـواسطة {REBEL_NAME}.**")
            del private_log[user_id]
        except: pass

# --- [ 3. أوامر الخصوصية الأصلية ] ---

@client.on(events.NewMessage(outgoing=True, pattern=r"\.قفل_الحساب"))
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
