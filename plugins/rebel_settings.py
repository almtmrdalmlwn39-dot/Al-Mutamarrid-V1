import asyncio, os, platform, psutil
from telethon import events, functions, types
from __main__ import client 

# هوية الإعدادات
SET_IDENTITY = "**- مـركز تـحكم الـمتمرد الـتقني | الـإعدادات ⚙️🦅**"

# 1. أمر فحص حالة السيرفر (Render Status)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.حالة_السورس"))
async def server_status(event):
    await event.edit("**- جـاري فـحص مـوارد الـسيرفر...**")
    uptime = "مـتصل ✅"
    ram = f"{psutil.virtual_memory().percent}%"
    cpu = f"{psutil.cpu_percent()}%"
    status_msg = (
        f"**📊 تـقرير أداء الـسورس :**\n"
        f"**- الـحالة:** {uptime}\n"
        f"**- اسـتهلاك الـرام:** `{ram}`\n"
        f"**- مـعالج الـسيرفر:** `{cpu}`\n"
        f"**- الـنظام:** `{platform.system()}`\n"
        f"**— — — — — — — — — —**\n"
        f"{SET_IDENTITY}"
    )
    await event.edit(status_msg)

# 2. أمر تغيير البايو (النبذة) فوراً
@client.on(events.NewMessage(outgoing=True, pattern=r"\.بايو (.*)"))
async def change_bio(event):
    new_bio = event.pattern_match.group(1)
    await event.edit("**- جـاري تـحديث الـنبذة الـتعريفية...**")
    try:
        await client(functions.account.UpdateProfileRequest(about=new_bio))
        await event.edit(f"**✅ تـم تـغيير الـبايو إلـى:**\n`{new_bio}`")
    except: await event.edit("**- فـشل فـي تـحديث الـبايو.**")

# 3. أمر "الرد السريع" (أمر يحفظ لك نص طويل ويطلعه بكلمة)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.عن_المتمرد"))
async def about_me(event):
    about_text = (
        "**🦅 الـمتمرد الـتقني (Al-Mutamarrid):**\n"
        "**مـطور سـورسات، خـبير فـي تـقنيات الـتيليجرام، ومـحب لـلتطوير الـمستمر.**\n"
        "**يـمني الـهوية، عـالمي الـطموح. 🇾🇪**"
    )
    await event.edit(about_text)

# --- [ قسم استعراض أوامر الإعدادات ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اوامر_الاعدادات"))
async def settings_help(event):
    help_text = (
        "**⚙️ أوامـر تـحكم الـحساب والـسورس :**\n"
        "**— — — — — — — — — —**\n"
        "**📊 | `.حالة_السورس` :** لـرؤية اسـتهلاك الـرام والـسيرفر.\n"
        "**📝 | `.بايو [النص]` :** لـتغيير نـبذة حـسابك فـوراً.\n"
        "**👤 | `.عن_المتمرد` :** لـتعريف نـفسك بـتنسيق فـخم.\n"
        "**— — — — — — — — — —**\n"
        f"{SET_IDENTITY}"
    )
    await event.edit(help_text)
