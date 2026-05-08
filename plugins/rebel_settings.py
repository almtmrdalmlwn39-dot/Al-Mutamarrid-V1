import asyncio, os, platform, psutil
from telethon import events, functions, types
from main import client, CMD_HELP

# --- [ AL-MUTAMARRID SETTINGS BRAND ] ---
# استخدام الإنجليزية العريضة للعناوين فقط لضمان الفخامة
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"
SET_BRAND = "**⚙️ 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗖𝗢𝗡𝗧𝗥𝗢𝗟**"

# تسجيل القسم في قائمة المساعدة
CMD_HELP.update({
    "الإعدادات والتحكم": [
        "حالة_السورس", "بايو", "عن_المتمرد", "اوامر_الاعدادات"
    ]
})

# 1. أمر فحص حالة السيرفر (Render Status)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.حالة_السورس"))
async def server_status(event):
    await event.edit("**🔄 جـاري فـحص مـوارد الـسيرفر والـتأكد من الـثبات...**")
    
    # جلب معلومات النظام
    ram = f"{psutil.virtual_memory().percent}%"
    cpu = f"{psutil.cpu_percent()}%"
    uptime = "نـشـط وقـيد الـسيطرة ✅"
    
    status_msg = (
        f"**📊 تـقـريـر أداء الـمـنـظـومـة :**\n"
        f"**— — — — — — — — — — —**\n"
        f"**🛡️ الـحـالـة:** {uptime}\n"
        f"**📉 اسـتهلاك الـرام:** `{ram}`\n"
        f"**🧠 مـعـالـج الـنـظام:** `{cpu}`\n"
        f"**💻 بـيـئة الـعـمـل:** `{platform.system()}`\n"
        f"**— — — — — — — — — — —**\n"
        f"{WAR_IDENTITY}"
    )
    await event.edit(status_msg)

# 2. أمر تغيير البايو (النبذة) فوراً
@client.on(events.NewMessage(outgoing=True, pattern=r"\.بايو (.*)"))
async def change_bio(event):
    new_bio = event.pattern_match.group(1)
    await event.edit("**⚙️ جـاري تـحـديث الـهـوية الـتعـريـفية لـلـحساب...**")
    try:
        # تحديث النبذة التعريفية في التليجرام
        await client(functions.account.UpdateProfileRequest(about=new_bio))
        await event.edit(
            f"**✅ تـم تـحـديث الـبـايـو بـنـجاح :**\n"
            f"`{new_bio}`\n\n"
            f"{WAR_IDENTITY}"
        )
    except Exception as e:
        await event.edit(f"**⚠️ فـشل الـتحديث:** `{e}`")

# 3. أمر "عن المتمرد" (التعريف الفخم)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.عن_المتمرد"))
async def about_me(event):
    about_text = (
        "**🦅 الـمتمرد الـتقني | 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗**\n"
        "**— — — — — — — — — — —**\n"
        "**مـطور سـورسات، خـبير فـي تـقـنيات الـتـشفـير، ومـهـندس أتمتة الـحسابات.**\n"
        "**صـاحـب هـوية يـمـنيـة أصـيلـة فـي عـالـم الأمـن الـسيـبرانـي 🇾🇪**\n"
        "**— — — — — — — — — — —**\n"
        f"{WAR_IDENTITY}"
    )
    await event.edit(about_text)

# 4. قائمة أوامر الإعدادات
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اوامر_الاعدادات"))
async def settings_help(event):
    help_text = (
        f"**{SET_BRAND}**\n"
        "**— — — — — — — — — — —**\n"
        "**📊 | `.حالة_السورس` :** لـمراقـبـة أداء الـمعـالـج والـرام.\n"
        "**📝 | `.بايو [النص]` :** لـتـغـيير نـبـذة حـسابك فـوراً.\n"
        "**👤 | `.عن_المتمرد` :** لـعرض بـطـاقة الـتـعريف الـخـاصة بـك.\n"
        "**— — — — — — — — — — —**\n"
        f"{WAR_IDENTITY}"
    )
    await event.edit(help_text)
