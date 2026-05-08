import asyncio, random, re, os
from telethon import events, functions, types
from telethon.tl.types import ChatBannedRights
from main import client, CMD_HELP, SUDO_USERS

# --- [ AL-MUTAMARRID ULTIMATE SOURCE ] ---
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"

# 1. تسجيل الأوامر في القائمة الرئيسية (CMD_HELP)
CMD_HELP.update({
    "القروب 🛡️": [
        "`.الاوامر` ➜ لعرض القوائم (م1 - م8)",
        "`.رفع` / `.تنزيل` ➜ للإدارة والتسلية",
        "`.ا` / `.ايدي` ➜ لعرض معلومات الشخص",
        "`.ز` ➜ للزواج العشوائي",
        "`.مسح` + عدد ➜ لتنظيف المحادثة"
    ]
})

# 2. محرك عرض القوائم (م1، م2، م3، م4، م5، م8)
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.(الاوامر|م1|م2|م3|م4|م5|م8)$"))
async def almutamarrid_menus(event):
    cmd = event.pattern_match.group(1)
    if cmd == "الاوامر":
        text = "**📚 قائمة أوامر المتمرد الشاملة :**\n• .م1 ➜ الإدارة\n• .م2 ➜ الإعدادات\n• .م3 ➜ الحماية\n• .م4 ➜ العام\n• .م5 ➜ التسلية\n• .م8 ➜ التحويل"
    elif cmd == "م1":
        text = "**🛡️ أوامر الإدارة (م1) :**\n• .رفع/تنزيل (مدير، مشرف، منشئ، مميز)\n• .مسح + عدد\n• .كتم | .حظر | .تقييد (بالرد)"
    elif cmd == "م3":
        text = "**🚫 أوامر الحماية والقفل (م3) :**\n• قفل/فتح (الروابط، الصور، الفيديو، السب، الملغم)\n• تفعيل/تعطيل (الحماية، الايدي، الزواج)"
    elif cmd == "م5":
        text = "**🎭 أوامر التسلية (م5) :**\n• .رفع/تنزيل (هطف، كلب، بثر، خروف، بقلبي)\n• .ز (زواج عشوائي) | .نسبة الحب"
    elif cmd == "م8":
        text = "**🔄 أوامر التحويل (م8) :**\n• .تحويل (صوت، متحركه، بصمه)\n• .زخرفة | .افتارات"
    else: text = f"**قريباً سيتم إضافة تفاصيل {cmd}**"
    
    await event.edit(text + f"\n\n{WAR_IDENTITY}")

# 3. محرك الرفع والتنزيل الشامل
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.(رفع|تنزيل) (.*)$"))
async def promote_engine(event):
    action, rank = event.pattern_match.group(1), event.pattern_match.group(2).strip()
    if not event.is_reply: return await event.edit("**⚠️ رد على الشخص أولاً!**")
    reply = await event.get_reply_message()
    status = "رفعته" if action == "رفع" else "نزلته من رتبة"
    await event.edit(f"**✅ أبشر.. {status} {rank} بنجاح!**\n**👤 المستخدم:** [{reply.sender.first_name}](tg://user?id={reply.sender_id})")

# 4. رادار الحماية (يشتغل تلقائياً على الكل بدون نقطة)
@client.on(events.NewMessage(incoming=True))
async def security_radar(event):
    if event.out or event.sender_id in SUDO_USERS: return
    text = event.raw_text
    # منع السب، الروابط، والتفليش (الرسائل الطويلة)
    if len(text) > 3000 or re.search(r"(t\.me|http|@|\.com)", text) or any(w in text for w in ["سكس", "نيك"]):
        try:
            await event.delete()
            # كتم الشخص تلقائياً
            await client(functions.channels.EditBannedRequest(event.chat_id, event.sender_id, ChatBannedRights(until_date=None, send_messages=True)))
        except: pass

# 5. أوامر المسح والخدمية
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.(مسح \d+|ا|ايدي|ز)$"))
async def tools_engine(event):
    cmd = event.raw_text
    if ".مسح" in cmd:
        count = int(re.search(r"\d+", cmd).group())
        await event.delete()
        async for msg in client.iter_messages(event.chat_id, limit=count):
            await msg.delete()
    elif ".ز" in cmd:
        users = await client.get_participants(event.chat_id)
        eligible = [u for u in users if not u.bot and u.id != event.sender_id]
        if eligible:
            chosen = random.choice(eligible)
            await event.edit(f"**💍 زوجتك هي:** [{chosen.first_name}](tg://user?id={chosen.id})")
    elif ".ا" in cmd or ".ايدي" in cmd:
        target = (await event.get_reply_message()).sender if event.is_reply else event.sender
        await event.edit(f"**👤 الاسم:** {target.first_name}\n**🆔 الأيدي:** `{target.id}`")
