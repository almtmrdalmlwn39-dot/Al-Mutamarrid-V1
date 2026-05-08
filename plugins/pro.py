import pytz
from datetime import datetime
from telethon import events
from main import client, CMD_HELP

# --- [ AL-MUTAMARRID PRO IDENTITY ] ---
# البصمة الملكية الموحدة بالخط الإنجليزي العريض
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"

# تسجيل القسم في قائمة المساعدة
CMD_HELP.update({
    "الأدوات الاحترافية": [
        "الوقت", "طرد"
    ]
})

# ملاحظة: تم حذف الرد التلقائي من هنا لأنه موجود في ملف more.py بشكل أذكى

# 1. أمر الوقت المطور (بتوقيت اليمن السعيد 🇾🇪)
@client.on(events.NewMessage(pattern=r'\.الوقت', outgoing=True))
async def get_time(event):
    # ضبط التوقيت على آسيا/عدن لضمان الدقة في اليمن
    now = datetime.now(pytz.timezone('Asia/Aden'))
    time_str = now.strftime("%I:%M %p")
    date_str = now.strftime("%Y/%m/%d")
    
    time_msg = (
        f"**⌚ الـوقـت الآن :** `{time_str}`\n"
        f"**📅 الـتـاريـخ :** `{date_str}`\n"
        f"**📍 الـموقـع :** `𝗬𝗘𝗠𝗘𝗡 🇾🇪`\n"
        f"**— — — — — — — — — —**\n"
        f"{WAR_IDENTITY}"
    )
    await event.edit(time_msg)

# 2. أمر الطرد السريع للمشرفين
@client.on(events.NewMessage(pattern=r'\.طرد', outgoing=True))
async def kick_user(event):
    if not event.is_reply:
        return await event.edit("**⚠️ يـرجى الـرد عـلى الـشخص لـطرده!**")
    
    reply = await event.get_reply_message()
    try:
        await client.kick_participant(event.chat_id, reply.sender_id)
        await event.edit(f"**✅ تـم طـرد الـمخرب مـن الـساحة بـنجاح!**\n\n{WAR_IDENTITY}")
    except Exception as e:
        await event.edit("**⚠️ لا أمـلك صـلاحـيات الـطرد فـي هـذه الـمجموعة!**")
