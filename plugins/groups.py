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
        "حظر_تلقائي", "تنظيف_الدردشة", "منع_التخريب"
    ]
})

# 1. محرك الحظر والحذف الفوري
@client.on(events.NewMessage(incoming=True))
async def instant_ban_guard(event):
    if not event.is_group or event.out or event.sender_id in SUDO_USERS:
        return

    text = event.raw_text or ""
    user_id = event.sender_id
    chat_id = event.chat_id
    
    # فحص شامل لجميع الأنماط
    if any(re.search(p, text, re.IGNORECASE) for p in (PORN_PATTERNS + SPAM_PATTERNS + ATTACK_PATTERNS)):
        try:
            # 1. حذف الرسالة فوراً
            await event.delete() 
            # 2. حظر المستخدم نهائياً من المجموعة
            await client(functions.channels.EditBannedRequest(
                chat_id, user_id, 
                types.ChatBannedRights(until_date=None, view_messages=True)
            ))
            # 3. إرسال إشعار بالتنفيذ
            await event.respond(
                f"**🛡️ تـم رصـد مـخـالـفـة قـواعـد الـمـتـمـرد!**\n"
                f"**👤 الـمـسـتـخدم:** `{user_id}`\n"
                f"**⚖️ الـإجـراء:** حـظر نـهـائـي وحـذف الـمـحـتوى.\n\n"
                f"{WAR_IDENTITY}"
            )
        except: pass

# 2. منع دخول البوتات الوهمية مع حظر المضيف
@client.on(events.ChatAction)
async def instant_anti_bot(event):
    if event.user_added:
        added_by = event.action_message.from_id
        if added_by in SUDO_USERS: return
        
        for user in event.users:
            if user.bot: # كشف البوت
                try:
                    await event.delete()
                    # حظر البوت ومن أضافه فوراً
                    await client(functions.channels.EditBannedRequest(
                        event.chat_id, user.id, 
                        types.ChatBannedRights(until_date=None, view_messages=True)
                    ))
                    await client(functions.channels.EditBannedRequest(
                        event.chat_id, added_by, 
                        types.ChatBannedRights(until_date=None, view_messages=True)
                    ))
                    await event.respond(f"**🛡️ تـم إحباط مـحـاولة تـلغـيم! حـظر الـمـخـرب والـبوت تـلقـائـياً.**")
                except: pass

# 3. حماية إعدادات المجموعة (حظر فوري للمخرب)
@client.on(events.ChatAction)
async def instant_lock_info(event):
    if event.user_id in SUDO_USERS: return
    
    if event.new_title or event.new_photo or event.user_kicked:
        try:
            # حظر من يحاول تغيير الاسم أو الصورة أو حذف الأعضاء
            await client(functions.channels.EditBannedRequest(
                event.chat_id, event.user_id, 
                types.ChatBannedRights(until_date=None, view_messages=True)
            ))
            await event.reply(f"**🛡️ مـحـاولة تـخـريب مـكـشـوفـة! تـم حـظر الـجـانـي فوراً.**")
        except: pass
