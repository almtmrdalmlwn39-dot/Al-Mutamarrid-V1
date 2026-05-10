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
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: return {"responses": {}, "locks": {}}
    return {"responses": {}, "locks": {}}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=4)

DB = load_db()
if "responses" not in DB: DB["responses"] = {}
if "locks" not in DB: DB["locks"] = {}

# 1. أوامر الإدارة الشاملة (كتم، حظر، طرد، رفع)
@client.on(events.NewMessage(outgoing=True))
async def admin_commands(event):
    text = event.raw_text
    chat_id = event.chat_id

    # مسح الرسائل بالعدد (.مسح 10)
    if text.startswith((".حذف ", ".مسح ")):
        try:
            count = int(text.split()[1])
            await event.delete()
            messages = await client.get_messages(chat_id, limit=count)
            await client.delete_messages(chat_id, messages)
        except: pass

    # أوامر الإدارة بالرد
    if event.is_reply:
        reply = await event.get_reply_message()
        user_id = reply.sender_id
        
        if text == "حظر":
            await client(functions.channels.EditBannedRequest(chat_id, user_id, ChatBannedRights(until_date=None, view_messages=True, send_messages=True, send_media=True, send_stickers=True, send_gifs=True, send_games=True, send_inline=True, embed_links=True)))
            await event.edit("**🚫 تم حظر المستخدم بنجاح.**")
        
        elif text == "كتم" or text == "تقييد":
            await client.edit_permissions(chat_id, user_id, send_messages=False)
            await event.edit("**🔇 تم كتم المستخدم.**")
            
        elif text == "طرد":
            await client.kick_participant(chat_id, user_id)
            await event.edit("**🚷 تم طرد المستخدم.**")

        elif text == "رفع مشرف":
            try:
                await client(functions.channels.EditAdminRequest(chat_id, user_id, ChatAdminRights(add_admins=True, ban_users=True, delete_messages=True, pin_messages=True, invite_users=True, change_info=True, manage_call=True), "Admin Rebel"))
                await event.edit("**👑 تم رفعه مشرفاً بصلاحيات كاملة.**")
            except Exception as e: await event.edit(f"**⚠️ فشل الرفع: تأكد أنك مالك المجموعة.**")

        elif text == "تنزيل مشرف":
            await client(functions.channels.EditAdminRequest(chat_id, user_id, ChatAdminRights(add_admins=False, ban_users=False, delete_messages=False, pin_messages=False, invite_users=False, change_info=False, manage_call=False), "Member"))
            await event.edit("**👤 تم تنزيله إلى عضو.**")

# 2. نظام الردود التفاعلي
@client.on(events.NewMessage(outgoing=True))
async def add_res_steps(event):
    user_id, text = event.sender_id, event.raw_text
    if text == "اضف رد":
        ADD_MODE[user_id] = {"step": 1}
        return await event.edit("**🛡️ ارسـل الآن الـكلمة التي تريد الرد عليها..**")
    
    if user_id in ADD_MODE:
        step = ADD_MODE[user_id]["step"]
        if step == 1:
            ADD_MODE[user_id].update({"word": text, "step": 2})
            return await event.edit(f"**✅ تم حفظ الكلمة: ({text})\nارسـل الآن الـرد..**")
        if step == 2:
            word = ADD_MODE[user_id].get("word")
            DB["responses"][word] = text
            save_db(DB)
            del ADD_MODE[user_id]
            return await event.edit(f"**🛡️ تم حفظ الرد بنجاح لـ ({word})**")

# 3. الأيدي الاحترافي (بدون تكرار وبوقت اليمن)
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.ايدي$"))
async def pro_id(event):
    target = (await event.get_reply_message()).sender if event.is_reply else await event.get_sender()
    tz = pytz.timezone('Asia/Aden')
    time_now = datetime.datetime.now(tz).strftime("%I:%M %p")
    caption = f"**🆔 آيدي المستخدم:** `{target.id}`\n**👤 الاسم:** {target.first_name}\n**⏰ توقيت اليمن:** {time_now}\n\n{WAR_IDENTITY}"
    await event.edit(caption)

# 4. تنفيذ الردود والحماية تلقائياً
@client.on(events.NewMessage(incoming=True))
async def auto_guard(event):
    if event.is_private or event.is_group:
        text, chat_id = event.raw_text, str(event.chat_id)
        # الردود
        if text in DB["responses"]:
            await event.reply(DB["responses"][text])
        
        # الأقفال (لغير المطورين)
        if not event.out and event.sender_id not in SUDO_USERS:
            locks = DB["locks"].get(chat_id, {})
            if locks.get("الروابط") and re.search(r"(t\.me|http|@)", text):
                await event.delete()

# 5. التحكم بالأقفال
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.(قفل|فتح) (الروابط|السب)$"))
async def locks_ctrl(event):
    action, item = event.pattern_match.group(1), event.pattern_match.group(2)
    chat_id = str(event.chat_id)
    if chat_id not in DB["locks"]: DB["locks"][chat_id] = {}
    DB["locks"][chat_id][item] = (action == "قفل")
    save_db(DB)
    await event.edit(f"**✅ تم {action} {item} بنجاح.**")
