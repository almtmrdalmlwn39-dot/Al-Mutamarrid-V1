import asyncio, random, re, os, datetime, pytz, json
from telethon import events, functions, types
from telethon.tl.types import ChatBannedRights, ChatAdminRights
from main import client, CMD_HELP, SUDO_USERS

# --- [ إعدادات الهوية والتخزين ] ---
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"
DB_FILE = "rebel_master_db.json"
ADD_MODE = {} 

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return {"responses": {}, "locks": {}}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=4)

DB = load_db()

# 1. أوامر الإدارة الشاملة (كتم، حظر، طرد، تقييد)
@client.on(events.NewMessage(incoming=True))
async def admin_commands(event):
    if event.sender_id not in SUDO_USERS and not event.out: return
    text = event.raw_text
    chat_id = event.chat_id

    # مسح الرسائل بالعدد (حذف 10)
    if text.startswith(("حذف ", "مسح ")):
        count = int(text.split()[1])
        await event.delete()
        async for m in client.iter_messages(chat_id, limit=count): await m.delete()

    # أوامر الإدارة بالرد
    if event.is_reply:
        reply = await event.get_reply_message()
        user_id = reply.sender_id
        if text == "حظر": await client.edit_permissions(chat_id, user_id, view_messages=False)
        elif text == "كتم" or text == "تقييد": await client.edit_permissions(chat_id, user_id, send_messages=False)
        elif text == "طرد": await client.kick_participant(chat_id, user_id)
        elif text == "الغاء الكتم" or text == "فك التقييد": await client.edit_permissions(chat_id, user_id, send_messages=True)
        elif text == "رفع مشرف": await client(functions.channels.EditAdminRequest(chat_id, user_id, ChatAdminRights(add_admins=True, ban_users=True, delete_messages=True, pin_messages=True, invite_users=True), "Admin"))
        elif text == "تنزيل مشرف": await client(functions.channels.EditAdminRequest(chat_id, user_id, ChatAdminRights(add_admins=False, ban_users=False, delete_messages=False), "Member"))

# 2. نظام الردود التفاعلي (اضف رد بالخطوات)
@client.on(events.NewMessage(incoming=True))
async def add_res_steps(event):
    user_id, text = event.sender_id, event.raw_text
    if text == "اضف رد" and (user_id in SUDO_USERS or event.out):
        ADD_MODE[user_id] = {"step": 1}
        return await event.reply("**🛡️ معالج الردود:**\nارسـل الآن **(الكلمة)** التي تريد الرد عليها..")
    if user_id in ADD_MODE:
        step = ADD_MODE[user_id]["step"]
        if step == 1:
            ADD_MODE[user_id].update({"word": text, "step": 2})
            return await event.reply(f"**✅ تم حفظ: ({text})**\nارسـل الرد الآن (استخدم {{اسم}} أو {{يوزر}})")
        if step == 2:
            if text == "تم":
                word, res = ADD_MODE[user_id].get("word"), ADD_MODE[user_id].get("response")
                DB["responses"][word] = res
                save_db(DB)
                del ADD_MODE[user_id]
                return await event.reply(f"**🛡️ تم الحفظ! جرب كتابة ({word})**")
            ADD_MODE[user_id]["response"] = text
            await event.reply(f"**📝 الرد الحالي:** {text}\nأرسل **(تم)** للحفظ.")

# 3. الأيدي الاحترافي (الاسم الحقيقي، البايو، الصورة)
@client.on(events.NewMessage(incoming=True, pattern=r"^(ا|ايدي)$"))
async def pro_id(event):
    target = (await event.get_reply_message()).sender if event.is_reply else event.sender
    tz = pytz.timezone('Asia/Aden')
    time_now = datetime.datetime.now(tz).strftime("%I:%M %p")
    try:
        full = await client(functions.users.GetFullUserRequest(target.id))
        user = full.users[0]
        name = f"{user.first_name} {user.last_name or ''}".strip()
        bio = full.full_user.about or "لا يوجد بايو"
        caption = (f"**👤 الاسم:** {name}\n**🆔 الآيدي:** `{user.id}`\n"
                   f"**🔗 المعرف:** @{user.username or 'لا يوجد'}\n"
                   f"**📖 البايو:** {bio}\n**⏰ الوقت:** {time_now}\n\n{WAR_IDENTITY}")
        photo = await client.download_profile_photo(target.id)
        if photo: await client.send_file(event.chat_id, photo, caption=caption); os.remove(photo)
        else: await event.reply(caption)
    except: await event.reply("**⚠️ خطأ في جلب البيانات.**")

# 4. قسم التسلية (زواج، نسبة الحب، خيرات)
@client.on(events.NewMessage(incoming=True, pattern=r"^ز$"))
async def casual_marry(event):
    users = await client.get_participants(event.chat_id)
    chosen = random.choice([u for u in users if not u.bot])
    await event.reply(f"**💍 زوجتك اليوم هي:** [{chosen.first_name}](tg://user?id={chosen.id})")

@client.on(events.NewMessage(incoming=True, pattern=r"^نسبة الحب$"))
async def love_percent(event):
    if not event.is_reply: return await event.reply("**⚠️ رد على الشخص اللي تبي تقيس حبك له!**")
    percent = random.randint(0, 100)
    await event.reply(f"**❤️ نسبة الحب بينكم هي: {percent}%**")

# 5. الأقفال والرادار (روابط، دخول، سب)
@client.on(events.NewMessage(incoming=True, pattern=r"^(قفل|فتح) (الروابط|الدخول|السب)$"))
async def locks_ctrl(event):
    if event.sender_id not in SUDO_USERS and not event.out: return
    action, item = event.pattern_match.group(1), event.pattern_match.group(2)
    chat_id = str(event.chat_id)
    if chat_id not in DB["locks"]: DB["locks"][chat_id] = {}
    DB["locks"][chat_id][item] = (action == "قفل")
    save_db(DB)
    await event.reply(f"**✅ تم {action} {item} بنجاح.**")

@client.on(events.NewMessage(incoming=True))
async def guard_and_res(event):
    text, chat_id = event.raw_text, str(event.chat_id)
    # تنفيذ الردود
    if text in DB["responses"]:
        res = DB["responses"][text]
        user = await event.get_sender()
        await event.reply(res.replace("{يوزر}", f"@{user.username or user.first_name}").replace("{اسم}", user.first_name))
    
    # حماية الروابط والسب للأعضاء
    if not (event.sender_id in SUDO_USERS or event.out):
        locks = DB["locks"].get(chat_id, {})
        if locks.get("الروابط") and re.search(r"(t\.me|http|@|\.com)", text): await event.delete()
        elif locks.get("السب") and any(w in text for w in ["سكس", "نيك"]): await event.delete()

@client.on(events.ChatAction)
async def auto_kick(event):
    if event.user_joined and DB["locks"].get(str(event.chat_id), {}).get("الدخول"):
        try: await client.kick_participant(event.chat_id, event.user_id)
        except: pass
