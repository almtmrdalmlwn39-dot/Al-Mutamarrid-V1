import asyncio, random, re, os, datetime, pytz
from telethon import events, functions, types
from telethon.tl.types import ChatBannedRights
from main import client, CMD_HELP, SUDO_USERS

# --- [ الهوية البصرية لسورس المتمرد ] ---
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"
REBEL_RESPONSES = {} # لتخزين "اضف رد"
LOCKS = {} # لتخزين حالات القفل (روابط، دخول)

# تسجيل القسم في القائمة الرئيسية
CMD_HELP.update({
    "القروب الشامل 🛡️": ["ايدي، ز، قفل/فتح الدخول، قفل/فتح الروابط، حذف + عدد، اضف رد لـ"]
})

# 1. نظام الأيدي (ا / ايدي) - جلب الاسم الأصلي والبايو والصورة
@client.on(events.NewMessage(incoming=True, pattern=r"^(ا|ايدي)$"))
async def pro_id_engine(event):
    target = (await event.get_reply_message()).sender if event.is_reply else event.sender
    tz = pytz.timezone('Asia/Aden')
    current_time = datetime.datetime.now(tz).strftime("%I:%M %p")
    try:
        full = await client(functions.users.GetFullUserRequest(target.id))
        user = full.users[0]
        bio = full.full_user.about or "لا يوجد بايو"
        # جلب الاسم الحقيقي من الحساب (وليس جهات الاتصال)
        name = f"{user.first_name} {user.last_name or ''}".strip()
        
        caption = (f"**🧬 USER INFORMATION :**\n— — — — — — — — —\n"
                   f"**👤 الاسم:** {name}\n**🆔 الآيدي:** `{user.id}`\n"
                   f"**🔗 المعرف:** @{user.username if user.username else 'لا يوجد'}\n"
                   f"**📖 البايو:** {bio}\n**⏰ الوقت:** {current_time}\n— — — — — — — — —\n{WAR_IDENTITY}")
        
        photo = await client.download_profile_photo(target.id)
        if photo:
            await client.send_file(event.chat_id, photo, caption=caption)
            os.remove(photo)
        else: await event.reply(caption)
    except: await event.reply("**⚠️ خطأ في جلب البيانات!**")

# 2. أوامر التحكم (قفل الروابط، قفل الدخول)
@client.on(events.NewMessage(incoming=True, pattern=r"^(قفل|فتح) (الروابط|الدخول|الصور|السب)$"))
async def locks_manager(event):
    if event.sender_id not in SUDO_USERS and not event.out: return
    action, item = event.pattern_match.group(1), event.pattern_match.group(2)
    chat_id = event.chat_id
    
    if chat_id not in LOCKS: LOCKS[chat_id] = {}
    LOCKS[chat_id][item] = (action == "قفل")
    await event.reply(f"**✅ تم {action} {item} بنجاح.**")

# 3. حماية الدخول التلقائية
@client.on(events.ChatAction)
async def auto_kick_on_join(event):
    if event.user_joined and LOCKS.get(event.chat_id, {}).get("الدخول"):
        try: await client.kick_participant(event.chat_id, event.user_id)
        except: pass

# 4. حذف الرسائل بالعدد (حذف 10، مسح 100)
@client.on(events.NewMessage(incoming=True, pattern=r"^(حذف|مسح) (\d+)$"))
async def delete_by_number(event):
    if event.sender_id not in SUDO_USERS and not event.out: return
    count = int(event.pattern_match.group(2))
    await event.delete()
    async for msg in client.iter_messages(event.chat_id, limit=count):
        try: await msg.delete()
        except: pass
    await event.respond(f"**🗑️ تم مسح {count} رسالة.**", delete_after=5)

# 5. نظام الردود الذكي (أضف رد لـ)
@client.on(events.NewMessage(incoming=True))
async def dynamic_responses(event):
    # تنفيذ الرد التلقائي
    if event.raw_text in REBEL_RESPONSES:
        await event.reply(REBEL_RESPONSES[event.raw_text])
        return

    # إدارة الردود (للمطور فقط)
    if (event.sender_id in SUDO_USERS or event.out) and event.is_reply:
        if event.raw_text.startswith("اضف رد لـ"):
            res = event.raw_text.split("لـ", 1)[1].strip()
            word = (await event.get_reply_message()).raw_text
            REBEL_RESPONSES[word] = res
            await event.reply(f"**✅ تم إضافة رد لـ ({word})**")
        elif event.raw_text == "حذف رد":
            word = (await event.get_reply_message()).raw_text
            if word in REBEL_RESPONSES:
                del REBEL_RESPONSES[word]
                await event.reply(f"**🗑️ تم حذف رد ({word})**")

# 6. رادار حماية الروابط والسب
@client.on(events.NewMessage(incoming=True))
async def guard_radar(event):
    if event.sender_id in SUDO_USERS or event.out: return
    if LOCKS.get(event.chat_id, {}).get("الروابط") and re.search(r"(t\.me|http|@|\.com)", event.raw_text):
        await event.delete()
    elif LOCKS.get(event.chat_id, {}).get("السب") and any(w in event.raw_text for w in ["سكس", "نيك"]):
        await event.delete()

# 7. التسلية (زواج عشوائي)
@client.on(events.NewMessage(incoming=True, pattern=r"^ز$"))
async def casual_fun(event):
    users = await client.get_participants(event.chat_id)
    chosen = random.choice([u for u in users if not u.bot])
    await event.reply(f"**💍 زوجتك المختارة هي:** [{chosen.first_name}](tg://user?id={chosen.id})")
