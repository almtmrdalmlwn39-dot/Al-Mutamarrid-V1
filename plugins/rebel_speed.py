import asyncio
from telethon import events
from main import client, CMD_HELP

# --- [ AL-MUTAMARRID SPEED BRAND ] ---
# الهوية الموحدة التي تضمن فخامة المظهر
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"
SPEED_BRAND = "**⚡ 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗣𝗘𝗘𝗗**"

# تسجيل القسم في قائمة المساعدة الشاملة
CMD_HELP.update({
    "السرعة والتنسيق": [
        "سلام", "انتظر", "نبض", "اكتب", "اوامر_السرعة"
    ]
})

# 1. اختصار "السلام عليكم" بتنسيق المتمرد الفخم
@client.on(events.NewMessage(outgoing=True, pattern=r"\.سلام"))
async def sleek_shalam(event):
    await event.edit(
        "**— الـسلام عـليكم ورحـمة الله وبـركاته 🌹✨**\n"
        f"{WAR_IDENTITY}"
    )

# 2. أمر شريط التحميل الوهمي (تنسيق مطور)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.انتظر"))
async def wait_process(event):
    bar = ["⬜", "⬛", "⬛", "⬛", "⬛"]
    for i in range(5):
        bar[i] = "🟩"
        progress = "".join(bar)
        await event.edit(f"**⏳ جـاري الـتـنـفـيـذ...**\n`{progress}`")
        await asyncio.sleep(0.4)
    await event.edit(f"**✅ تـم اخـتراق الـوقت بـنجاح!**\n\n{WAR_IDENTITY}")

# 3. أمر "القلب النابض" المطور
@client.on(events.NewMessage(outgoing=True, pattern=r"\.نبض"))
async def heart_beat(event):
    # نبضات متناغمة تعكس هيبة الاسم
    hearts = ["❤️", "🖤", "❤️", "🖤", "❤️"]
    for h in hearts:
        await event.edit(f"**{h} 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 {h}**")
        await asyncio.sleep(0.6)

# 4. أمر "الآلة الكاتبة" السريع
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اكتب (.*)"))
async def type_writer(event):
    text = event.pattern_match.group(1)
    t_text = ""
    for char in text:
        t_text += char
        # إضافة مؤشر الكتابة لإعطاء واقعية
        await event.edit(f"**{t_text}▒**")
        await asyncio.sleep(0.1)
    await event.edit(f"**{t_text}**")

# 5. استعراض أوامر السرعة
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اوامر_السرعة"))
async def speed_help(event):
    help_text = (
        f"**{SPEED_BRAND}**\n"
        "**— — — — — — — — — — —**\n"
        "**👋 | `.سلام` :** لإلـقاء تـحية تـليق بـالـمتمردين.\n"
        "**⏳ | `.انتظر` :** لـإظهار تـأثير مـعالجة بـرمجية.\n"
        "**💓 | `.نبض` :** تـأثير بـصري يـنبض بـقوة اسـمك.\n"
        "**⌨️ | `.اكتب [نص]` :** لـمحاكاة الآلـة الـكاتبة الـسريعة.\n"
        "**— — — — — — — — — — —**\n"
        f"{WAR_IDENTITY}"
    )
    await event.edit(help_text)
