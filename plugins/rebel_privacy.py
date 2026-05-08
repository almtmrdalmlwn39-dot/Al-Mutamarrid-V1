import asyncio
from telethon import events, functions, types
from main import client, CMD_HELP

# --- [ AL-MUTAMARRID PRIVACY IDENTITY ] ---
# البصمة الملكية الموحدة بالخط الإنجليزي العريض
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"
PRIVACY_BRAND = "**👤 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗣𝗥𝗜𝗩𝗔𝗖𝗬**"

# تسجيل القسم في قائمة المساعدة
CMD_HELP.update({
    "الخصوصية والتخفي": [
        "قفل_الحساب", "تدمير", "انهاء", "اوامر_الخصوصية"
    ]
})

# 1. أمر إخفاء معلومات الحساب الشامل
@client.on(events.NewMessage(outgoing=True, pattern=r"\.قفل_الحساب"))
async def hide_everything(event):
    await event.edit("**🛡️ جـاري تـفـعـيل وضـع الـتـخـفي الـمـطـلـق...**")
    try:
        # إخفاء رقم الهاتف، آخر ظهور، والصور عن الجميع
        await client(functions.account.SetPrivacyRequest(key=types.InputPrivacyKeyPhoneNumber(), rules=[types.InputPrivacyValueDisallowAll()]))
        await client(functions.account.SetPrivacyRequest(key=types.InputPrivacyKeyStatusTimestamp(), rules=[types.InputPrivacyValueDisallowAll()]))
        await client(functions.account.SetPrivacyRequest(key=types.InputPrivacyKeyProfilePhoto(), rules=[types.InputPrivacyValueDisallowAll()]))
        await event.edit(
            f"**✅ تـم تـنـشيط الـدرع الـبرمجي بنجاح.**\n"
            f"**👤 حـسابك الآن خـارج نـطاق الـرؤية.**\n\n"
            f"{WAR_IDENTITY}"
        )
    except Exception as e:
        await event.edit(f"**⚠️ فـشل تـغيير الإعـدادات:** `{e}`")

# 2. أمر "تدمير الرسائل" (حذف من الطرفين)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تدمير"))
async def destroy_chat(event):
    if not event.is_private: 
        return await event.edit("**⚠️ هـذا الأمـر مـخصص لـلـتطهير فـي الـدردشات الـخاصة!**")
    
    await event.edit("**🧨 جـاري تـفـجير الـسجلات مـن الـطرفـين...**")
    async for msg in client.iter_messages(event.chat_id):
        await msg.delete(revoke=True) # الحذف من الطرفين

# 3. أمر "إنهاء المستخدم" (حظر فوري)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.انهاء"))
async def end_user(event):
    if not event.is_private: return
    await event.edit("**🚫 تـم عـزل الـمستخدم وتـصـفـيـة الـمحادثة.**")
    await client(functions.contacts.BlockRequest(event.chat_id)) # حظر الشخص

# 4. قائمة أوامر الخصوصية
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اوامر_الخصوصية"))
async def privacy_help(event):
    help_text = (
        f"**{PRIVACY_BRAND}**\n"
        "**— — — — — — — — — —**\n"
        "**🛡️ | `.قفل_الحساب` :** لـتـفـعـيل وضـع الـشبح فـوراً.\n"
        "**🧨 | `.تدمير` :** لـمـسح الأثـر مـن الـطرفـين (خـاص).\n"
        "**🚫 | `.انهاء` :** لـحـظر الـمـزعج بـضـغطة واحـدة.\n"
        "**— — — — — — — — — —**\n"
        f"{WAR_IDENTITY}"
    )
    await event.edit(help_text)
