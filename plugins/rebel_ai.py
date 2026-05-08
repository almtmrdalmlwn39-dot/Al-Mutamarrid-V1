import asyncio
from telethon import events
from main import client, CMD_HELP

# --- [ AL-MUTAMARRID AI IDENTITY ] ---
# البصمة الملكية الموحدة بالخط الإنجليزي العريض
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"
AI_BRAND = "**🧠 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗔𝗜 𝗦𝗬𝗦𝗧𝗘𝗠**"

# تسجيل القسم في قائمة المساعدة
CMD_HELP.update({
    "عقل المتمرد": [
        "بحث", "سوال", "ترجم", "اوامر_الذكاء"
    ]
})

# 1. أمر "البحث في جوجل"
@client.on(events.NewMessage(outgoing=True, pattern=r"\.بحث (.*)"))
async def google_search(event):
    query = event.pattern_match.group(1)
    await event.edit(f"**🔍 جـاري الـتـنـقيب عـن: `{query}` فـي جـوجل...**")
    link = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    await asyncio.sleep(1)
    await event.edit(
        f"**🌐 نـتائج الـبحث الـذكـي عـن: `{query}`**\n\n"
        f"**🔗 الـرابط:** [إضغط هنا للمشاهدة]({link})\n\n"
        f"{WAR_IDENTITY}"
    )

# 2. أمر "الرد الذكي" (نصائح تقنية)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.سوال (.*)"))
async def tech_ask(event):
    question = event.pattern_match.group(1)
    await event.edit("**🔄 جـاري تـحليل الـبيانات بـرمجياً...**")
    await asyncio.sleep(1.5)
    
    response = (
        f"**💡 نـتـيجة الـتـحلـيـل لــ `{question}` :**\n\n"
        f"**- يـنصحك الـمتمرد بـمراجعة مـستودعات GitHub أولاً.**\n"
        f"**- تأكد من تـحديث مـكتبات Python لآخر إصدار.**\n\n"
        f"{AI_BRAND}"
    )
    await event.edit(response)

# 3. أمر "الترجمة" السريعة
@client.on(events.NewMessage(outgoing=True, pattern=r"\.ترجم (.*)"))
async def fast_translate(event):
    text = event.pattern_match.group(1)
    await event.edit(f"**🌐 جـاري الـمـعالـجة والـتـرجـمة...**")
    await asyncio.sleep(1)
    await event.edit(
        f"**✅ الـنـص بـعد الـمـعـالـجـة :**\n\n"
        f"`Processing: {text}`\n\n"
        f"{WAR_IDENTITY}"
    )

# 4. قائمة أوامر الذكاء
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اوامر_الذكاء"))
async def ai_help(event):
    help_text = (
        f"**{AI_BRAND}**\n"
        "**— — — — — — — — — —**\n"
        "**🔍 | `.بحث [النص]` :** لـلبحث الـسريع فـي جـوجل.\n"
        "**💡 | `.سوال [النص]` :** لـلحصول عـلى نـصيحة بـرمجية.\n"
        "**🌐 | `.ترجم [النص]` :** لـترجمة الـكلام لـلغة الـبرمجة.\n"
        "**— — — — — — — — — —**\n"
        f"{WAR_IDENTITY}"
    )
    await event.edit(help_text)
