import asyncio, random, re, os, datetime, pytz, json
from telethon import events, functions, types
from telethon.tl.types import ChatBannedRights
from main import client, CMD_HELP, SUDO_USERS

# --- [ إعدادات الهوية والداتابيز ] ---
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"
DB_FILE = "rebel_data.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return {"responses": {}, "locks": {}}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=4)

DB = load_db()

# 1. أوامر القوائم (م1 - م8)
@client.on(events.NewMessage(incoming=True, pattern=r"^(الاوامر|م1|م2|م3|م4|م5|م8)$"))
async def menus_engine(event):
    if event.sender_id not in SUDO_USERS and not event.out: return
    cmd = event.pattern_match.group(1)
    menus = {
        "الاوامر": "**📚 أوامر المتمرد:**\n• م1 (إدارة) | م2 (إعدادات) | م3 (حماية)\n• م5 (تسلية) | م8 (تحويل) | الردود",
        "م1": "**🛡️ إدارة:**\n• رفع/تنزيل (مدير، مشرف)\n• مسح + عدد | كتم | حظر",
        "م3": "**🚫 حماية:**\n• قفل/فتح (الروابط، الدخول، الصور، السب)\n• تفعيل/تعطيل (الحماية، الايدي)",
    }
    await event.reply(menus.get(cmd, "**قريباً..**") + f"\n\n{WAR_IDENTITY}")

# 2. الأيدي المطوّر (الاسم الحقيقي + البايو + الوقت)
@client.on(events.NewMessage(incoming=True, pattern=r"^(ا|ايدي)$"))
async def pro_id(event):
    target = (await event.get_reply_message()).sender if event.is_reply else event.sender
    tz = pytz.timezone('Asia/Aden')
    time_now = datetime.datetime.now(tz).strftime("%I:%M %p")
    try:
        full = await client(functions.users.GetFullUserRequest(target.id))
        user = full.users[0]
        bio = full.full_user.about or "لا يوجد بايو"
        # جلب الاسم الحقيقي من التليجرام مباشرة
        name = f"{user.first_name} {user.last_name or ''}".strip()
        
        caption = (f"**🧬 USER INFORMATION :**\n— — — — — — — — —\n"
                   f"**👤 الاسم:** {name}\n**🆔 الآيدي:** `{user.id}`\n"
                   f"**🔗 المعرف:** @{user.username or 'لا يوجد'}\n"
                   f"**📖 البايو:** {bio}\n**⏰ الوقت:** {time_now}\n— — — — — — — — —\n{WAR_IDENTITY}")
        
        photo = await client.download_profile_photo(target.id)
        if photo:
            await client.send_file(event.chat_id, photo, caption=caption)
            os.remove(photo)
        else: await event.reply(caption)
    except: await event.reply("**⚠️ خطأ في جلب البيانات.**")

# 3. نظام الردود (أضف رد لـ / حذف رد)
@client.on(events.NewMessage(incoming=True))
async def responses_manager(event):
    text = event.raw_text
    # تنفيذ الرد
    if text in DB["responses"]:
        await event.reply(DB["responses"][text])
        return
    # إضافة رد
    if (event.sender_id in SUDO_USERS or event.out) and event.is_reply:
        if text.startswith("اضف رد لـ") or text.startswith("أضف رد لـ"):
            res = text.split("لـ", 1)[1].strip()
            word = (await event.get_reply_message()).raw_text
            DB["responses"][word] = res
            save_db(DB)
            await event.reply(f"**✅ تم حفظ رد لـ ({word})**")
        elif text == "حذف رد":
            word = (await event.get_reply_message()).raw_text
            if word in DB["responses"]:
                del DB["responses"][word]
                save_db(DB)
                await event.reply(f"**🗑️ تم حذف الرد.**")

# 4. التحكم والقفل (روابط، دخول، مسح رسائل)
@client.on(events.NewMessage(incoming=True, pattern=r"^(قفل|فتح) (الروابط|الدخول|السب)$"))
async def locks_manager(event):
    if event.sender_id not in SUDO_USERS and not event.out: return
    action, item = event.pattern_match.group(1), event.pattern_match.group(2)
    chat_id = str(event.chat_id)
    if chat_id not in DB["locks"]: DB["locks"][chat_id] = {}
    DB["locks"][chat_id][item] = (action == "قفل")
    save_db(DB)
    await event.reply(f"**✅ تم {action} {item} بنجاح.**")

@client.on(events.NewMessage(incoming=True, pattern=r"^(حذف|مسح) (\d+)$"))
async def delete_msgs(event):
    if event.sender_id not in SUDO_USERS and not event.out: return
    count = int(event.pattern_match.group(2))
    await event.delete()
    async for m in client.iter_messages(event.chat_id, limit=count):
        try: await m.delete()
        except: pass

# 5. حماية الرادار (روابط، سب، منع دخول)
@client.on(events.ChatAction)
async def protector_action(event):
    if event.user_joined and DB["locks"].get(str(event.chat_id), {}).get("الدخول"):
        try: await client.kick_participant(event.chat_id, event.user_id)
        except: pass

@client.on(events.NewMessage(incoming=True))
async def protector_text(event):
    if event.sender_id in SUDO_USERS or event.out: return
    locks = DB["locks"].get(str(event.chat_id), {})
    if locks.get("الروابط") and re.search(r"(t\.me|http|@|\.com)", event.raw_text):
        await event.delete()
    elif locks.get("السب") and any(w in event.raw_text for w in ["سكس", "نيك"]):
        await event.delete()

# 6. التسلية (ز)
@client.on(events.NewMessage(incoming=True, pattern=r"^ز$"))
async def marry(event):
    users = await client.get_participants(event.chat_id)
    chosen = random.choice([u for u in users if not u.bot])
    await event.reply(f"**💍 زوجتك المختارة هي:** [{chosen.first_name}](tg://user?id={chosen.id})")
