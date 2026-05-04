import asyncio
from telethon import events
from __main__ import client 

# هوية الذكاء الاصطناعي
AI_IDENTITY = "**- عـقل الـمتمرد الـاصطناعي | الـإصدار الـذكي 🧠🦅**"

# 1. أمر "البحث في جوجل" (يعطيك رابط البحث فوراً)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.بحث (.*)"))
async def google_search(event):
    query = event.pattern_match.group(1)
    await event.edit(f"**🔍 جـاري الـبحث عـن: `{query}` فـي جـوجل...**")
    link = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    await asyncio.sleep(1)
    await event.edit(f"**🌐 نـتائج الـبحث عـن: `{query}`\n\n🔗 الـرابط: [اضـغط هـنا لـلرؤية]({link})\n\n{AI_IDENTITY}**")

# 2. أمر "الرد الذكي" (ردود جاهزة لأسئلة تقنية)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.سوال (.*)"))
async def tech_ask(event):
    question = event.pattern_match.group(1)
    await event.edit("**🔄 جـاري تـحليل الـسؤال بـرمجياً...**")
    await asyncio.sleep(1.5)
    # هنا ردود ثابتة، يمكن تطويرها لاحقاً
    await event.edit(f"**💡 بـخصوص سـؤالك عن `{question}` :\n\n- الـمتمرد يـنصحك بـالبحث فـي GitHub أولاً.\n- أو تـأكد من تـنصيب مـكتبات الـبايثون الـلازمة.\n\n{AI_IDENTITY}**")

# 3. أمر "الترجمة" (ترجمة سريعة للإنجليزية - للمطورين)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.ترجم (.*)"))
async def fast_translate(event):
    text = event.pattern_match.group(1)
    await event.edit(f"**🌐 جـاري الـترجمة إلـى الـإنجليزية...**")
    # ملاحظة: هذه محاكاة بسيطة، الأفضل ربطها بـ API مستقبلاً
    await asyncio.sleep(1)
    await event.edit(f"**✅ الـنص بـالـلغة الـأخرى :\n\n`Processing: {text}`\n\n{AI_IDENTITY}**")

# --- [ قسم استعراض أوامر الذكاء ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اوامر_الذكاء"))
async def ai_help(event):
    help_text = (
        "**🧠 أوامـر الـبحث والـذكاء :**\n"
        "**— — — — — — — — — —**\n"
        "**🔍 | `.بحث [النص]` :** لـلبحث الـسريع فـي جـوجل.\n"
        "**💡 | `.سوال [النص]` :** لـلحصول عـلى نـصيحة بـرمجية.\n"
        "**🌐 | `.ترجم [النص]` :** لـترجمة الـكلام لـلغة الـبرمجة.\n"
        "**— — — — — — — — — —**\n"
        f"{AI_IDENTITY}"
    )
    await event.edit(help_text)
