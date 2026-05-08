import os
import sys
import asyncio
from telethon import events
from main import client, CMD_HELP

# --- [ AL-MUTAMARRID CONTROL BRAND ] ---
# الهوية الموحدة لمركز التحكم بالاسم الإنجليزي الفخم
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"
CONTROL_BRAND = "**⚙️ 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗖𝗢𝗡𝗧𝗥𝗢𝗟**"

# تسجيل القسم في قائمة المساعدة
CMD_HELP.update({
    "نظام الإدارة": [
        "اعادة_تشغيل", "تحديث", "تفعيل_التخزين"
    ]
})

# 1. أمر إعادة التشغيل (Restart)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اعادة_تشغيل"))
async def restart_bot(event):
    # استخدام اسم السورس بالإنجليزي كما طلبت
    await event.edit("**🔄 جـاري إعـادة تـشـغـيـل 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗧𝗘𝗖𝗛...**")
    await asyncio.sleep(2)
    # إنهاء العملية الحالية وبدء تشغيل الملف الأساسي مجدداً
    os.execl(sys.executable, sys.executable, *sys.argv)

# 2. أمر التحديث الجذري (Update from GitHub)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تحديث"))
async def update_bot(event):
    await event.edit("**📥 جـاري جـلـب تـحـديـثـات 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 مـن الـمـسـتـودع...**")
    try:
        # سحب التغييرات ومسح أي تضارب في الملفات
        os.system("git fetch --all && git reset --hard origin/main") 
        await event.edit("**✅ تـم تـحـديث 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 بـنجاح! جـاري إعـادة الـتشـغيل...**")
        await asyncio.sleep(2)
        os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception as e:
        await event.edit(f"**⚠️ حـدث خـطأ أثـنـاء تـحـديـث الـنـظـام:**\n`{str(e)}`")

# 3. أمر تفعيل التخزين (Log Storage)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تفعيل_التخزين"))
async def start_storage(event):
    await event.edit("**🔥 جـاري تـفـعـيـل مـنـظـومـة الـتـخـزيـن لـ 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗...**")
    # استدعاء أمر الإنشاء الموجود في ملف log.py تلقائياً
    await event.respond(".انشاء_تخزين")
    await event.delete()

# --- [ استعراض أوامر الإدارة ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اوامر_الادارة"))
async def control_help(event):
    help_text = (
        f"**{CONTROL_BRAND}**\n"
        "**— — — — — — — — — — —**\n"
        "**🔄 | `.اعادة_تشغيل` :** لإعادة إقلاع السورس.\n"
        "**📥 | `.تحديث` :** لجلب آخر الميزات من GitHub.\n"
        "**📦 | `.تفعيل_التخزين` :** لربط السورس بجروب التخزين.\n"
        "**— — — — — — — — — — —**\n"
        f"{WAR_IDENTITY}"
    )
    await event.edit(help_text)
