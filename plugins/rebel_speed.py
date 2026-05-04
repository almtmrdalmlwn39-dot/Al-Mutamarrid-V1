import asyncio
from telethon import events
from __main__ import client 

# هوية السرعة
SPEED_IDENTITY = "**- قـسم الـسرعة والـتنسيق | الـمتمرد الـتقني ⚡🦅**"

# 1. اختصار "السلام عليكم" بتنسيق فخم
@client.on(events.NewMessage(outgoing=True, pattern=r"\.سلام"))
async def sleek_shalam(event):
    await event.edit("**- الـسلام عـليكم ورحـمة الله وبـركاته 🌹✨**")

# 2. اختصار "تحميل" (وهمي لشغل الوقت)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.انتظر"))
async def wait_process(event):
    for i in range(0, 101, 20):
        await event.edit(f"**⏳ جـاري الـتحميل: `% {i}`**")
        await asyncio.sleep(0.5)
    await event.edit("**✅ تـمت الـعملية بـنجاح!**")

# 3. أمر "القلب النابض" (تأثير بصري)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.نبض"))
async def heart_beat(event):
    hearts = ["❤️", "🖤", "❤️", "🖤", "❤️"]
    for h in hearts:
        await event.edit(f"**{h} الـمتمرد الـتقني {h}**")
        await asyncio.sleep(0.5)

# 4. أمر "كتابة سريعة" (يظهر كأنك تكتب حرف بحرف)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اكتب (.*)"))
async def type_writer(event):
    text = event.pattern_match.group(1)
    t_text = ""
    for char in text:
        t_text += char
        await event.edit(f"**{t_text}**")
        await asyncio.sleep(0.1)

# --- [ قسم استعراض أوامر السرعة ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اوامر_السرعة"))
async def speed_help(event):
    help_text = (
        "**⚡ أوامـر الـسرعة والـتنسيق :**\n"
        "**— — — — — — — — — —**\n"
        "**👋 | `.سلام` :** لإرسـال تـحية فـخمة.\n"
        "**⏳ | `.انتظر` :** لـإظهار شـريط تـحميل وهـمي.\n"
        "**💓 | `.نبض` :** تـأثير الـقلب الـنابض بـاسمك.\n"
        "**⌨️ | `.اكتب [النص]` :** لـلكتابة بـتأثير الآلـة الـكاتبة.\n"
        "**— — — — — — — — — —**\n"
        f"{SPEED_IDENTITY}"
    )
    await event.edit(help_text)
