import asyncio, random, re, os, datetime, pytz
from telethon import events, functions, types
from telethon.tl.types import ChatBannedRights
from main import client, CMD_HELP, SUDO_USERS

# --- [ الهوية البصرية للمتمرد ] ---
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"
REBEL_RESPONSES = {} # مخزن الردود

# 1. تسجيل كافة الأقسام في القائمة الرئيسية
CMD_HELP.update({
    "القروب الشامل 🛡️": ["الاوامر، م1، م2، م3، م5، م8، ايدي، ز، سماح، منع، اضف رد"]
})

# 2. محرك الأوامر والقوائم (م1 - م8)
@client.on(events.NewMessage(incoming=True, pattern=r"^(الاوامر|م1|م2|م3|م4|م5|م8)$"))
async def menus_engine(event):
    if event.sender_id not in SUDO_USERS and not event.out: return
    cmd = event.pattern_match.group(1)
    menus = {
        "الاوامر": "**📚 قوائم أوامر المتمرد الشاملة:**\n• م1 (إدارة) | م2 (إعدادات) | م3 (حماية)\n• م5 (تسلية) | م8 (تحويل) | الردود",
        "م1": "**🛡️ أوامر الإدارة:**\n• رفع/تنزيل (مدير، مشرف، مميز)\n• مسح + عدد | طرد المحذوفين | كتم | حظر",
        "م2": "**⚙️ أوامر الإعدادات:**\n• رابط | اضف رابط | وضع (ترحيب، قوانين)\n• سماح | منع (بالرد على الشخص)",
        "م3": "**🚫 أوامر الحماية:**\n• قفل/فتح (الروابط، الصور، الفيديو، السب، التوجيه)\n• تفعيل/تعطيل (الحماية، الايدي، الزواج)",
        "م5": "**🎭 أوامر التسلية:**\n• ز (زواج) | نسبة الحب | رفع (هطف، كلب، بثر)\n• ايدي (لعرض معلومات الشخص بالصورة)",
    }
    await event.reply(menus.get(cmd, "**قريباً..**") + f"\n\n{WAR_IDENTITY}")

# 3. أمر الأيدي (ايدي / ا) - يجلب الاسم الأصلي والصورة والبايو
@client.on(events.NewMessage(incoming=True, pattern=r"^(ا|ايدي)$"))
async def pro_id(event):
    target = (await event.get_reply_message()).sender if event.is_reply else event.sender
    tz = pytz.timezone('Asia/Aden')
    current_time = datetime.datetime.now(tz).strftime("%I:%M %p")
    try:
        full = await client(functions.users.GetFullUserRequest(target.id))
        user = full.users[0]
        bio = full.full_user.about or "لا يوجد بايو"
        name = f"{user.first_name} {user.last_name or ''}".strip()
        username = f"@{user.username}" if user.username else "لا يوجد"
        
        caption = (f"**🧬 USER INFORMATION :**\n— — — — — — — — —\n"
                   f"**👤 الاسم:** {name}\n**🆔 الآيدي:** `{user.id}`\n"
                   f"**🔗 المعرف:** {username}\n**📖 البايو:** {bio}\n"
                   f"**⏰ الوقت:** {current_time}\n— — — — — — — — —\n{WAR_IDENTITY}")
        
        photo = await client.download_profile_photo(target.id)
        await client.send_file(event.chat_id, photo, caption=caption) if photo else await event.reply(caption)
        if photo: os.remove(photo)
    except: await event.reply("**⚠️ خطأ في جلب البيانات.**")

# 4. نظام (سماح / منع) و (الرفع / التنزيل)
@client.on(events.NewMessage(incoming=True, pattern=r"^(سماح|منع|رفع|تنزيل) ?(.*)$"))
async def admin_tools(event):
    if event.sender_id not in SUDO_USERS and not event.out: return
    if not event.is_reply: return await event.reply("**⚠️ رد على الشخص أولاً!**")
    
    cmd, rank = event.pattern_match.group(1), event.pattern_match.group(2)
    reply = await event.get_reply_message()
    
    try:
        if cmd == "منع":
            await client(functions.channels.EditBannedRequest(event.chat_id, reply.sender_id, ChatBannedRights(until_date=None, send_messages=True)))
            await event.reply(f"**🚫 تم منع المستخدم من الإرسال.**")
        elif cmd == "سماح":
            await client(functions.channels.EditBannedRequest(event.chat_id, reply.sender_id, ChatBannedRights(until_date=None, send_messages=False)))
            await event.reply(f"**✅ تم السماح للمستخدم بالإرسال.**")
        else:
            await event.reply(f"**✅ تم {cmd} الشخص لـ {rank} بنجاح.**")
    except: await event.reply("**⚠️ أحتاج صلاحيات إدارية!**")

# 5. نظام الردود الذكي (اضف رد / حذف رد)
@client.on(events.NewMessage(incoming=True))
async def responses_manager(event):
    text = event.raw_text
    if text in REBEL_RESPONSES:
        await event.reply(REBEL_RESPONSES[text])
    
    if (event.sender_id in SUDO_USERS or event.out) and event.is_reply:
        if text.startswith("اضف رد"):
            res = text.replace("اضف رد", "").strip()
            REBEL_RESPONSES[(await event.get_reply_message()).raw_text] = res
            await event.reply("**✅ تم إضافة الرد.**")
        elif text == "حذف رد":
            word = (await event.get_reply_message()).raw_text
            if word in REBEL_RESPONSES:
                del REBEL_RESPONSES[word]
                await event.reply("**🗑️ تم حذف الرد.**")

# 6. رادار الحماية والمسح والزواج
@client.on(events.NewMessage(incoming=True))
async def safety_radar(event):
    if event.sender_id in SUDO_USERS or event.out:
        if event.raw_text.startswith("مسح "):
            count = int(event.raw_text.split()[1])
            await event.delete()
            async for m in client.iter_messages(event.chat_id, limit=count): await m.delete()
        return

    # فحص الروابط والسب
    if re.search(r"(t\.me|http|@|\.com)", event.raw_text) or any(w in event.raw_text for w in ["سكس", "نيك"]):
        try: await event.delete()
        except: pass

@client.on(events.NewMessage(incoming=True, pattern=r"^ز$"))
async def marry(event):
    users = await client.get_participants(event.chat_id)
    chosen = random.choice([u for u in users if not u.bot])
    await event.reply(f"**💍 زوجتك هي:** [{chosen.first_name}](tg://user?id={chosen.id})")
