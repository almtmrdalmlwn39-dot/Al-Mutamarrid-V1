import asyncio, random
from telethon import events
from __main__ import client 

# هوية المساعد التقني
TECH_IDENTITY = "**- مـساعد الـمتمرد الـتقني | قـسم الألـعاب والـهاتف 🎮📱**"

# 1. نصيحة تسريع الهاتف (مخصصة لـ S22 Ultra وأشباهه)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تسريع"))
async def phone_boost(event):
    await event.edit("**- جـاري تـحليل مـوارد الـنظام...**")
    await asyncio.sleep(1.5)
    boost_tips = [
        "**🚀 تـنصيحة المـتمرد:** قـم بـتفعيل 'خـيارات الـمطور' وتـعطيل حـركة الـإطارات لـسرعة صـاروخية.",
        "**🎮 للألـعاب:** اسـتخدم Game Booster وقم بـإيقاف الـتطبيقات فـي الـخلفية لـلحفاظ على FPS.",
        "**🔋 للـبطارية:** قـلل دقة الـشاشة إلى FHD+ بـدل WQHD+ لـتوفير الـطاقة أثـناء الـلعب الـمكثف."
    ]
    await event.edit(f"{random.choice(boost_tips)}\n\n{TECH_IDENTITY}")

# 2. أمر "تجهيز التشكيلة" (يعطيك تشكيلات مقترحة لـ eFootball/FC)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تشكيلة"))
async def formation_suggest(event):
    await event.edit("**- جـاري جـلب أقـوى الـخطط الـتكتيكية... ⚽**")
    formations = [
        "**🔥 خطة هجومية:** 4-2-4 (مـناسبة لـلضغط الـعالي والـسرعة).",
        "**🛡️ خطة متوازنة:** 4-3-3 (تـعطيك سـيطرة كـاملة عـلى وسـط الـملعب).",
        "**🔱 خطة الـمتمرد:** 4-1-2-3 (لـلعب الـمباشر والـمرتدات الـصاعقة)."
    ]
    await asyncio.sleep(1)
    await event.edit(f"{random.choice(formations)}\n\n{TECH_IDENTITY}")

# 3. أمر "تقييم اللاعب" (بشكل عشوائي للمزح مع أصدقائك في اللعبة)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تقييم (.*)"))
async def player_rate(event):
    player = event.pattern_match.group(1)
    rating = random.randint(85, 99)
    await event.edit(f"**📈 تـقييم الـلاعب `{player}` فـي سـيرفر الـمتمرد هو: `{rating}/100` 🌟**")

# --- [ قسم استعراض أوامر التقنية ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اوامر_التقنية"))
async def tech_help(event):
    help_text = (
        "**📱 أوامـر الـتقنية والـألعاب :**\n"
        "**— — — — — — — — — —**\n"
        "**🚀 | `.تسريع` :** نـصائح لـزيادة سـرعة هـاتفك وأدائـه.\n"
        "**⚽ | `.تشكيلة` :** اقـتراح خـطط لـ eFootball و FC Mobile.\n"
        "**📈 | `.تقييم [الاسم]` :** لـتقييم أي لاعـب بـشكل تـقني.\n"
        "**— — — — — — — — — —**\n"
        f"{TECH_IDENTITY}"
    )
    await event.edit(help_text)
