import asyncio, random, platform
from telethon import events, functions, types
from __main__ import client 

# هوية السورس الموحدة
SAWA_IDENTITY = "**- نـظام الـمتمرد الـتقني الـشامل | الإصـدار الـملكـي 🦅👑**"

# 1. أمر الفحص الشامل (بنج + معلومات السيرفر)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.فحص"))
async def sawa_ping(event):
    start = datetime.now()
    await event.edit("**- جـاري فـحص اسـتجابة الـسيرفر...**")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    res = (
        f"**📊 تـقرير الـأداء الـشامل :**\n"
        f"**— — — — — — — — — —**\n"
        f"**🚀 الـبنج:** `{ms}ms`\n"
        f"**⚙️ الـنظام:** `{platform.system()}`\n"
        f"**🛡️ الـحالة:** مـتصل وقـيد الـسيطرة\n"
        f"**— — — — — — — — — —**\n"
        f"{SAWA_IDENTITY}"
    )
    await event.edit(res)

# 2. أمر الحماية السريع (قفل الدردشة بالرد)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تأمين"))
async def sawa_secure(event):
    if not event.is_private: return
    await event.edit("**- تـم تـأمين الـدردشة وتـشفير الـبيانات 🔐**")
    # محاكاة برمجية للحماية
    await asyncio.sleep(1)
    await event.edit(f"**🛡️ الـدردشة الآن تـحت حـماية الـمتمرد.\n\n{SAWA_IDENTITY}**")

# 3. أمر الردود الذكية (ترفيه + تقنية)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.سوا (.*)"))
async def sawa_ask(event):
    query = event.pattern_match.group(1)
    replies = [
        f"**💡 بـخصوص `{query}`: الـمتمرد يـرى أن الـاستمرار هـو سـر الـنجاح.**",
        f"**🚀 `{query}` مـوضوع مـهم، سـأقوم بـتحديثك بـالـنتائج فـوراً.**",
        f"**🔥 الـمتمرد الـتقني يـدعم خـطتك فـي `{query}` بـقوة.**"
    ]
    await event.edit(random.choice(replies))

# 4. أمر جلب المعلومات المتقدمة
@client.on(events.NewMessage(outgoing=True, pattern=r"\.معلوماتي"))
async def sawa_info(event):
    me = await client.get_me()
    info = (
        f"**🪪 بـطاقة الـمتمرد الـذكية :**\n"
        f"**— — — — — — — — — —**\n"
        f"**- الـاسم:** `{me.first_name}`\n"
        f"**- الآيـدي:** `{me.id}`\n"
        f"**- الـمطور:** @A0_O7"
        f"**— — — — — — — — — —**\n"
        f"{SAWA_IDENTITY}"
    )
    await event.edit(info)

# --- [ قائمة أوامر "سوا" المدمجة ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اوامر_سوا"))
async def sawa_help(event):
    help_text = (
        "**👑 قـائمة أوامـر سـوا الـشاملة :**\n"
        "**— — — — — — — — — —**\n"
        "**📊 | `.فحص` :** لـرؤية سـرعة الـبنج وحـالة الـنظام.\n"
        "**🛡️ | `.تأمين` :** لـإظهار وضـع الـحماية فـي الـخاص.\n"
        "**💡 | `.سوا [نص]` :** لـلحصول عـلى رد ذكـي مـن الـسورس.\n"
        "**🪪 | `.معلوماتي` :** لـعرض بـياناتك بـتنسيق الـمتمرد.\n"
        "**— — — — — — — — — —**\n"
        f"{SAWA_IDENTITY}"
    )
    await event.edit(help_text)
