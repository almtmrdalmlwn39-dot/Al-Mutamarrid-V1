import asyncio, random
from telethon import events
from main import client, CMD_HELP

# --- [ AL-MUTAMARRID TECH BRAND ] ---
# استخدام الهوية الموحدة لضمان الفخامة
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"
TECH_BRAND = "**🎮 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗧𝗘𝗖𝗛**"

# تسجيل القسم في قائمة المساعدة
CMD_HELP.update({
    "التقنية والألعاب": [
        "تسريع", "تشكيلة", "تقييم", "اوامر_التقنية"
    ]
})

# 1. نصيحة تسريع الهاتف (تحسين أداء S22 Ultra)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تسريع"))
async def phone_boost(event):
    await event.edit("**🔄 جـاري تـحـليل مـوارد الـنظام وتـقـييم الأداء...**")
    await asyncio.sleep(1.5)
    
    # نصائح مبنية على طلباتك السابقة لتحسين الـ FPS والحرارة
    boost_tips = [
        "**🚀 تـوصـية الـمتمرد:** فـعّل 'خـيارات الـمطور' وعـطّل حـركة الـإطارات لـسرعة اسـتجابة خـارقة.",
        "**🎮 أداء الألـعاب:** اسـتخدم Game Booster ووجّه كـل الـطاقة لـلمعالج لـضمان ثـبات الـ FPS.",
        "**🔋 تـوفـير الـطاقة:** قـلل دقـة الـشاشة لـ FHD+ أثـناء الـلعب لـلحفاظ عـلى بـرودة الـجهاز.",
        "**❄️ الـحرارة:** اغـلق تـطبيقات الـخلفية لـتجنب الـتـحمية الـمفاجئة لـلـمـعـالج."
    ]
    await event.edit(f"{random.choice(boost_tips)}\n\n{WAR_IDENTITY}")

# 2. أمر "تجهيز التشكيلة" (eFootball / FC Mobile)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تشكيلة"))
async def formation_suggest(event):
    await event.edit("**⚽ جـاري اسـتـدعـاء أقـوى الـخطط الـتكتيكية...**")
    formations = [
        "**🔥 هـجـوم كـاسـح:** 4-2-4 (مـثالية لـلضغط الـعالي والـمرتدات).",
        "**🛡️ تـوازن مـلكـي:** 4-3-3 (تـعطيك سـيطرة مـطلقة عـلى وسـط الـميدان).",
        "**🔱 تـكتيك الـمتمرد:** 4-1-2-3 (لـصناعة اللـعب الـسريع والـعمق الـهجومي)."
    ]
    await asyncio.sleep(1)
    await event.edit(f"{random.choice(formations)}\n\n{WAR_IDENTITY}")

# 3. أمر "تقييم اللاعب" (تقييم تقني عشوائي)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تقييم (.*)"))
async def player_rate(event):
    player = event.pattern_match.group(1)
    rating = random.randint(88, 99) # رفعنا الحد الأدنى للتقييم ليكون أكثر حماساً
    await event.edit(
        f"**📈 الـتـقـييم الـتـقـنـي لـلـلاعب `{player}` :**\n"
        f"**📊 الـدرجـة :** `{rating}/100` 🌟\n\n"
        f"{WAR_IDENTITY}"
    )

# 4. قائمة أوامر التقنية
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اوامر_التقنية"))
async def tech_help(event):
    help_text = (
        f"**{TECH_BRAND}**\n"
        "**— — — — — — — — — — —**\n"
        "**🚀 | `.تسريع` :** نـصائح لـرفع كـفاءة الـهاتف والـألعاب.\n"
        "**⚽ | `.تشكيلة` :** اقـتراح خـطط هـجومية ودفاعـية لـلألعاب.\n"
        "**📈 | `.تقييم [الاسم]` :** لـإعطاء تـقييم تـقني لأي لاعـب.\n"
        "**— — — — — — — — — — —**\n"
        f"{WAR_IDENTITY}"
    )
    await event.edit(help_text)
