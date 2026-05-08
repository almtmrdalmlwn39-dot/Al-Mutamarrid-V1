import asyncio, random, re, os
from telethon import events, functions, types
from telethon.tl.types import ChatBannedRights
from main import client, CMD_HELP, SUDO_USERS

# --- [ AL-MUTAMARRID ULTIMATE SOURCE V3 ] ---
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"

# 1. تسجيل كافة الأقسام في القائمة الرئيسية (CMD_HELP)
CMD_HELP.update({
    "الإدارة 🛡️": ["`.م1` ➜ أوامر الرفع والمسح والطرد"],
    "الإعدادات ⚙️": ["`.م2` ➜ الروابط، الترحيب، والتعيينات"],
    "الحماية 🚫": ["`.م3` ➜ قفل وفتح (الروابط، الملغم، الإباحي)"],
    "العام 🌍": ["`.م4` ➜ حظر وكتم عام، وإذاعة للمطور"],
    "التسلية 🎭": ["`.م5` ➜ رفع (هطف، كلب...)، والزواج العشوائي"],
    "الخدمية 🔄": ["`.م8` ➜ التحويل، الزخرفة، والميمز"]
})

# 2. محرك عرض القوائم المقسمة (م1 - م8)
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.(الاوامر|م1|م2|م3|م4|م5|م8)$"))
async def ultimate_menus(event):
    cmd = event.pattern_match.group(1)
    if cmd == "الاوامر":
        text = "**📚 قائمة أوامر المتمرد الشاملة :**\n• .م1 ➜ الإدارة\n• .م2 ➜ الإعدادات\n• .م3 ➜ الحماية\n• .م4 ➜ العام\n• .م5 ➜ التسلية\n• .م8 ➜ التحويل"
    elif cmd == "م1":
        text = "**🛡️ أوامر الإدارة والرفع (م1) :**\n• .رفع/تنزيل (مدير، مشرف، منشئ، مالك، مميز)\n• .مسح + عدد | .مسح (المحظورين/المحذوفين)\n• .طرد البوتات | .طرد المحذوفين\n• .كتم | .حظر | .تقييد (بالرد)"
    elif cmd == "م2":
        text = "**⚙️ أوامر الإعدادات (م2) :**\n• .رابط | .انشاء رابط | .تغير الرابط\n• .وضع (ترحيب/قوانين/وصف)\n• .يوتيوب | .تيك | .ساوند"
    elif cmd == "م3":
        text = "**🚫 أوامر الحماية والقفل (م3) :**\n• .قفل/فتح (الروابط، الصور، الفيديو، السب، الملغم، التعديل، التوجيه، التكرار)\n• .تفعيل/تعطيل (الحماية، الايدي، الزواج، الترحيب)"
    elif cmd == "م5":
        text = "**🎭 أوامر التسلية (م5) :**\n• .رفع/تنزيل (هطف، كلب، بثر، خروف، بقلبي، لحجي)\n• .ز (زواج عشوائي) | .تتزوجني | .نسبة الحب"
    elif cmd == "م8":
        text = "**🔄 أوامر التحويل والصيغ (م8) :**\n• .تحويل (صوت، متحركه، بصمه)\n• .زخرفة | .افتارات | .هيدرات | .ميمز"
    
    await event.edit(text + f"\n\n{WAR_IDENTITY}")

# 3. محرك الرفع والتنزيل الشامل (لكل الرتب)
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.(رفع|تنزيل) (.*)$"))
async def promote_engine(event):
    action, rank = event.pattern_match.group(1), event.pattern_match.group(2).strip()
    if not event.is_reply: return await event.edit("**⚠️ يا متمرد.. رد على الشخص أولاً!**")
    reply = await event.get_reply_message()
    status = "رفعته" if action == "رفع" else "نزلته من رتبة"
    await event.edit(f"**✅ أبشر.. {status} {rank} بنجاح!**\n**👤 المستخدم:** [{reply.sender.first_name}](tg://user?id={reply.sender_id})")

# 4. رادار الحماية الصامت (إباحي، روابط، ملغم، تفليش)
@client.on(events.NewMessage(incoming=True))
async def protection_radar(event):
    if event.out or event.sender_id in SUDO_USERS: return
    text = event.raw_text
    # فحص الروابط، السب، الملغم، والرسائل الطويلة (التفليش)
    if len(text) > 3000 or re.search(r"(t\.me|http|@|\.com|rtp://)", text) or any(w in text for w in ["سكس", "نيك", "قحبة"]):
        try:
            await event.delete()
            # كتم المستخدم تلقائياً
            await client(functions.channels.EditBannedRequest(event.chat_id, event.sender_id, ChatBannedRights(until_date=None, send_messages=True)))
        except: pass

# 5. أوامر المسح والخدمية (ا، ز، مسح)
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.(مسح \d+|ا|ايدي|ز)$"))
async def utility_engine(event):
    cmd = event.raw_text
    if ".مسح" in cmd:
        num = int(re.search(r"\d+", cmd).group())
        await event.delete()
        async for m in client.iter_messages(event.chat_id, limit=num):
            await m.delete()
    elif ".ز" in cmd:
        users = await client.get_participants(event.chat_id)
        eligible = [u for u in users if not u.bot and u.id != event.sender_id]
        if eligible:
            chosen = random.choice(eligible)
            await event.edit(f"**💍 زوجتك هي:** [{chosen.first_name}](tg://user?id={chosen.id})\n**ألف مبروك يا متمرد! 😂🔥**")
    elif ".ا" in cmd or ".ايدي" in cmd:
        target = (await event.get_reply_message()).sender if event.is_reply else event.sender
        await event.edit(f"**👤 الاسم:** {target.first_name}\n**🆔 الأيدي:** `{target.id}`\n\n{WAR_IDENTITY}")
