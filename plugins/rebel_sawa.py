import asyncio, random, platform
from datetime import datetime
from telethon import events, functions, types
from main import client, CMD_HELP

# --- [ AL-MUTAMARRID SAWA IDENTITY ] ---
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"
SAWA_BRAND = "**👑 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗥𝗢𝗬𝗔𝗟 𝗘𝗗𝗜𝗧𝗜𝗢𝗡**"

CMD_HELP.update({
    "نظام سوا الشامل": [
        "فحص", "تأمين", "سوا", "معلوماتي", "اوامر_سوا"
    ]
})

# 1. أمر الفحص الشامل
@client.on(events.NewMessage(outgoing=True, pattern=r"\.فحص"))
async def sawa_ping(event):
    start = datetime.now()
    await event.edit("**🔄 جـاري تـحليل اسـتجابة الـنظام...**")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    
    res = (
        f"**📊 تـقـريـر الأداء الـمـلكـي :**\n"
        f"**— — — — — — — — — — —**\n"
        f"**🚀 الـبـنـج :** `{ms}ms`\n"
        f"**⚙️ الـنـظـام :** `{platform.system()}`\n"
        f"**🛡️ الـحـالـة :** `𝗢𝗡𝗟𝗜𝗡𝗘 & 𝗦𝗘𝗖𝗨𝗥𝗘 🛡️`\n"
        f"**— — — — — — — — — — —**\n"
        f"{WAR_IDENTITY}"
    )
    await event.edit(res)

# 2. أمر الحماية (تم تحويل الرسالة للإنجليزية العريضة)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تأمين"))
async def sawa_secure(event):
    if not event.is_private: 
        return await event.edit("**⚠️ هـذا الأمـر يـعمل فـي الـخاص فـقط!**")
    
    await event.edit("**🛡️ 𝗦𝗘𝗖𝗨𝗥𝗜𝗡𝗚 𝗖𝗛𝗔𝗧 𝗔𝗡𝗗 𝗘𝗡𝗖𝗥𝗬𝗣𝗧𝗜𝗡𝗚 𝗗𝗔𝗧𝗔...**")
    await asyncio.sleep(1.5)
    await event.edit(
        f"**🔐 𝗧𝗛𝗜𝗦 𝗖𝗛𝗔𝗧 𝗜𝗦 𝗡𝗢𝗪 𝗨𝗡𝗗𝗘𝗥 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗣𝗥𝗢𝗧𝗘𝗖𝗧𝗜𝗢𝗡.**\n"
        f"**🛡️ 𝗦𝗧𝗔𝗧𝗨𝗦: 𝗘𝗡𝗖𝗥𝗬𝗣𝗧𝗘𝗗.**\n\n"
        f"{WAR_IDENTITY}"
    )

# 3. أمر معلوماتي الذكي (يسحب معلومات الشخص الذي ترد عليه)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.معلوماتي"))
async def sawa_info(event):
    # التحقق إذا كان هناك رد على شخص آخر
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        user = await client.get_entity(reply_msg.sender_id)
        title = "🔍 تـحليل بـيانات الـهدف :"
    else:
        user = await client.get_me()
        title = "🪪 بـطاقة الـمتمرد الـتـقـنـية :"

    # تجهيز المعرف بشكل صحيح
    username = f"@{user.username}" if user.username else "لا يوجد معرف"
    
    info = (
        f"**{title}**\n"
        f"**— — — — — — — — — — —**\n"
        f"**👤 الـاسـم :** `{user.first_name}`\n"
        f"**🆔 الآيـدي :** `{user.id}`\n"
        f"**🌐 الـمـعرف :** {username}\n"
        f"**— — — — — — — — — — —**\n"
        f"{WAR_IDENTITY}"
    )
    await event.edit(info)

# 4. أوامر سوا الأخرى (كما هي)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.سوا (.*)"))
async def sawa_ask(event):
    query = event.pattern_match.group(1)
    replies = [
        f"**💡 بـخصوص `{query}`: الـمتمرد يـرى أن الـاستمرار هـو سـر الـنجاح.**",
        f"**🚀 `{query}` مـوضوع مـهم، الـنظام يـقوم بـالمعالجة الآن.**",
        f"**🔥 الـمتمرد الـتقني يـدعم خـطتك فـي `{query}` بـكل قـوة.**"
    ]
    await event.edit(random.choice(replies))

@client.on(events.NewMessage(outgoing=True, pattern=r"\.اوامر_سوا"))
async def sawa_help(event):
    help_text = (
        f"**{SAWA_BRAND}**\n"
        "**— — — — — — — — — — —**\n"
        "**📊 | `.فحص` :** لـرؤية سـرعة الـبنج وحـالة الـنظام.\n"
        "**🛡️ | `.تأمين` :** لـتفعيل وضـع الـتشفير فـي الـخاص.\n"
        "**💡 | `.سوا [نص]` :** لـلحصول عـلى رد ذكـي مـن الـسورس.\n"
        "**🪪 | `.معلوماتي` :** لـعرض بـياناتك أو بـيانات الـهدف بالرد.\n"
        "**— — — — — — — — — — —**\n"
        f"{WAR_IDENTITY}"
    )
    await event.edit(help_text)
