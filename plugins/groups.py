from main import client, CMD_HELP, SUDO_USERS, DB_FILE 
from telethon import events, functions, types
import json, os, re

# --- [ AL-MUTAMARRID SECURITY IDENTITY ] ---
# بصمة المتمرد الإنجليزية الفخمة (تثبت حقوقك عالمياً)
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"

# تسجيل القسم بالعربي في القائمة
CMD_HELP.update({
    "الحماية القصوى": [
        "تفعيل_الحماية", "منع_الروابط", "حماية_التفليش"
    ]
})

# محرك الحماية من الروابط والسبام
@client.on(events.NewMessage(incoming=True))
async def global_security_guard(event):
    if not event.is_group: return
    data = load_data()
    
    if event.sender_id in SUDO_USERS or event.sender_id in data.get("allowed", []):
        return

    # فحص الروابط والكلمات الممنوعة
    for pattern in SPAM_PATTERNS:
        if re.search(pattern, event.text, re.IGNORECASE):
            try:
                await event.delete() # حذف الرسالة الممنوعة فوراً
                return 
            except: pass

# نظام منع "التفليش" والتخريب
@client.on(events.ChatAction)
async def anti_destruction(event):
    data = load_data()
    me = await client.get_me()
    owner_name = me.first_name # اسم منصب السورس

    if event.user_id in SUDO_USERS or event.user_id in data.get("allowed", []):
        return

    # إذا حاول شخص تخريب القروب (حذف أعضاء، تغيير اسم، إلخ)
    if event.user_kicked or event.new_title or event.new_photo or event.new_pin:
        try:
            await client(functions.channels.EditBannedRequest(
                event.chat_id, event.user_id, 
                types.ChatBannedRights(until_date=None, view_messages=True)
            ))
            # الرسالة بالعربي عشان الكل يفهم أن الحماية شغالة
            alert_msg = (
                f"**🛡️ {owner_name} بالمرصاد..**\n"
                f"**⚠️ تم حظر المخرب `{event.user_id}` فوراً لمنع التخريب.**\n\n"
                f"{WAR_IDENTITY}"
            )
            await event.reply(alert_msg)
        except: pass
