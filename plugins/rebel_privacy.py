import asyncio
from telethon import events, functions, types
from __main__ import client 

# هوية الخصوصية
PRIVACY_IDENTITY = "**- نـظام الـحماية والـتشفير | الـمتمرد الـتقني 🛡️👤**"

# 1. أمر إخفاء معلومات الحساب (الكل) بلمحة بصر
@client.on(events.NewMessage(outgoing=True, pattern=r"\.قفل_الحساب"))
async def hide_everything(event):
    await event.edit("**- جـاري تـفعيل وضـع الـتخفي الـشامل...**")
    try:
        # إخفاء رقم الهاتف، آخر ظهور، والصور
        await client(functions.account.SetPrivacyRequest(key=types.InputPrivacyKeyPhoneNumber(), rules=[types.InputPrivacyValueDisallowAll()]))
        await client(functions.account.SetPrivacyRequest(key=types.InputPrivacyKeyStatusTimestamp(), rules=[types.InputPrivacyValueDisallowAll()]))
        await client(functions.account.SetPrivacyRequest(key=types.InputPrivacyKeyProfilePhoto(), rules=[types.InputPrivacyValueDisallowAll()]))
        await event.edit(f"**✅ تـم تـفعيل الـدرع الـبرمجي.. حـسابك الآن مـخفي عـن الـجميع.\n\n{PRIVACY_IDENTITY}**")
    except: await event.edit("**- حـصل خـطأ فـي تـغيير إعـدادات الـخصوصية.**")

# 2. أمر "تدمير الرسائل" (حذف الرسائل من الطرفين في الخاص)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تدمير"))
async def destroy_chat(event):
    if not event.is_private: return await event.edit("**- هـذا الأمـر يـعمل فـي الـدردشات الـخاصة فـقط!**")
    await event.edit("**- جـاري تـدمير الـمحادثة مـن الـطرفين... 🧨**")
    async for msg in client.iter_messages(event.chat_id):
        await msg.delete(revoke=True)

# 3. أمر "الرد السريع للمزعجين" (تبنيد شخص في الخاص بضغطة زر)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.انهاء"))
async def end_user(event):
    if not event.is_private: return
    await event.edit("**- تـم حـظر الـمستخدم وإنـهاء الـدردشة بـنجاح. ✅**")
    await client(functions.contacts.BlockRequest(event.chat_id))

# --- [ قسم استعراض أوامر الخصوصية ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اوامر_الخصوصية"))
async def privacy_help(event):
    help_text = (
        "**👤 أوامـر الـخصوصية والـتخفي :**\n"
        "**— — — — — — — — — —**\n"
        "**🛡️ | `.قفل_الحساب` :** لإخـفاء الـرقم والـصورة وآخـر ظـهور فوراً.\n"
        "**🧨 | `.تدمير` :** لـحذف كـافة الـرسائل مـن الـطرفين (فـي الـخاص).\n"
        "**🚫 | `.انهاء` :** لـحظر الـشخص وحـذف الـمحادثة بـلمحة بـصر.\n"
        "**— — — — — — — — — —**\n"
        f"{PRIVACY_IDENTITY}"
    )
    await event.edit(help_text)
