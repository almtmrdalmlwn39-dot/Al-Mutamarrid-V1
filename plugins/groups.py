from main import client, CMD_HELP, SUDO_USERS
from telethon import events, functions, types
import json, os, re, asyncio

# --- [ AL-MUTAMARRID IRON DEFENSE ] ---
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"

# قوائم الكشف (إباحي، سب، روابط، تلغيم، تفليش)
PORN_PATTERNS = [r"sex", r"porn", r"إباحي", r"سكس", r"نيك", r"قحبة", r"شرموطة", r"مص"]
SPAM_PATTERNS = [r"t\.me\/", r"http", r"www\.", r"bit\.ly", r"ارسلها", r"انشر"]
ATTACK_PATTERNS = [r"تفليش", r"تصفية", r"تلغيم", r"هكر", r"اختراق", r"ثغرة"]

CMD_HELP.update({
    "الحماية القاطعة": [
        "حظر_تلقائي: حماية آلية ضد الروابط والسب",
        ".تنظيف_الدردشة: لمسح رسائل المجموعة (للمالك)",
        ".حظر: لحظر شخص بالرد عليه (للمالك)"
    ]
})

# 1. محرك الحماية التلقائي (شغال طول الوقت)
@client.on(events.NewMessage(incoming=True))
async def instant_ban_guard(event):
    if not event.is_group or event.out or event.sender_id in SUDO_USERS:
        return

    text = event.raw_text or ""
    user_id = event.sender_id
    chat_id = event.chat_id
    
    if any(re.search(p, text, re.IGNORECASE) for p in (PORN_PATTERNS + SPAM_PATTERNS + ATTACK_PATTERNS)):
        try:
            await event.delete() 
            await client(functions.channels.EditBannedRequest(
                chat_id, user_id, 
                types.ChatBannedRights(until_date=None, view_messages=True)
            ))
            await event.respond(
                f"**🛡️ تـم رصـد مـخـالـفـة قـواعـد الـمـتـمـرد!**\n"
                f"**👤 الـمـسـتـخدم:** `{user_id}`\n"
                f"**⚖️ الـإجـراء:** حـظر نـهـائـي.\n\n"
                f"{WAR_IDENTITY}"
            )
        except: pass

# 2. أمر تنظيف الدردشة (يدوي للمالك فقط)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تنظيف_الدردشة"))
async def manual_clean(event):
    await event.edit("**🛡️ جـاري تـنظيف الـدردشـة مـن الـمخـلفـات...**")
    try:
        # يمسح آخر 100 رسالة
        count = 0
        async for msg in client.iter_messages(event.chat_id, limit=100):
            await msg.delete()
            count += 1
        await event.respond(f"**✅ تـم تـنظيف ({count}) رسـالـة بـنجاح!**")
    except Exception as e:
        await event.edit(f"**⚠️ فشل: تأكد أنني مشرف بصلاحية الحذف.**")

# 3. أمر الحظر بالرد (يدوي للمالك فقط)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.حظر"))
async def manual_ban(event):
    if not event.is_reply:
        return await event.edit("**⚠️ رد عـلى رسـالة الـشخص لـحظره!**")
    
    reply = await event.get_reply_message()
    try:
        await client(functions.channels.EditBannedRequest(
            event.chat_id, reply.sender_id, 
            types.ChatBannedRights(until_date=None, view_messages=True)
        ))
        await event.edit(f"**🛡️ تـم طـرد الـمخرب `{reply.sender_id}` بـأمر الـمتمرد.**")
    except:
        await event.edit("**⚠️ خـطأ في الـصلاحـيات.**")

# 4. منع دخول البوتات وحظر من أضافهم
@client.on(events.ChatAction)
async def instant_anti_bot(event):
    if event.user_added:
        added_by = event.action_message.from_id
        if added_by in SUDO_USERS: return
        for user in event.users:
            if user.bot:
                try:
                    await client(functions.channels.EditBannedRequest(event.chat_id, user.id, types.ChatBannedRights(until_date=None, view_messages=True)))
                    await client(functions.channels.EditBannedRequest(event.chat_id, added_by, types.ChatBannedRights(until_date=None, view_messages=True)))
                except: pass
