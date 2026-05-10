import os, json
from telethon import events
# استيراد الأدوات من الملف الرئيسي
from main import client, CMD_HELP

# --- [ إعدادات التخزين ] ---
R_DB_FILE = "rebel_replies.json"

def load_db():
    if os.path.exists(R_DB_FILE):
        try:
            with open(R_DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}
    return {}

def save_db(data):
    with open(R_DB_FILE, "w", encoding="utf-8") as f: 
        json.dump(data, f, ensure_ascii=False, indent=4)

REPLIES = load_db()
ADD_MODE = {}

# 1. أمر إضافة رد جديد
@client.on(events.NewMessage(outgoing=True, pattern=r"^اضف رد$"))
async def start_add(event):
    ADD_MODE[event.sender_id] = {"step": 1}
    await event.edit("**🛡️ أهلاً بك في معالج الردود..\nأرسل الآن (الكلمة) التي تريد الرد عليها:**")

# 2. معالج خطوات الإضافة (تم فصله لتجنب التعليق)
@client.on(events.NewMessage(outgoing=True))
async def handle_addition(event):
    uid = event.sender_id
    if uid not in ADD_MODE or event.raw_text == "اضف رد":
        return

    step = ADD_MODE[uid]["step"]
    
    if step == 1:
        ADD_MODE[uid].update({"word": event.raw_text, "step": 2})
        await event.edit(f"**✅ تم حفظ الكلمة: ({event.raw_text})\nأرسل الآن (الرد) المطلوب:**")
    
    elif step == 2:
        word = ADD_MODE[uid]["word"]
        REPLIES[word] = event.raw_text
        save_db(REPLIES)
        del ADD_MODE[uid]
        await event.edit(f"**🛡️ تم تفعيل الرد بنجاح!\n• الكلمة: {word}\n• الرد: {event.raw_text}**")

# 3. معالج الرد التلقائي (هذا هو اللي كان ناقصك)
@client.on(events.NewMessage(incoming=False, outgoing=True)) # لردودك أنت
async def auto_reply_self(event):
    if event.sender_id in ADD_MODE: return # تجاهل لو كنت في وضع الإضافة
    if event.raw_text in REPLIES:
        await event.respond(REPLIES[event.raw_text])

@client.on(events.NewMessage(incoming=True)) # لردود الأشخاص الآخرين
async def auto_reply_others(event):
    if event.raw_text in REPLIES:
        await event.reply(REPLIES[event.raw_text])

# 4. أمر مسح رد
@client.on(events.NewMessage(outgoing=True, pattern=r"^مسح رد$"))
async def delete_rep(event):
    if not event.is_reply: return await event.edit("**⚠️ رد على الكلمة لمسحها.**")
    reply = await event.get_reply_message()
    word = reply.raw_text
    if word in REPLIES:
        del REPLIES[word]
        save_db(REPLIES)
        await event.edit(f"**🗑️ تم حذف الرد لـ ({word})**")
    else:
        await event.edit("**⚠️ هذه الكلمة ليس لها رد.**")

# --- [ التحديث للقائمة 17 ] ---
CMD_HELP["قسم الردود الذكية"] = [
    "**-** `اضف رد` ⇐ إضافة رد جديد.",
    "**-** `مسح رد` ⇐ حذف رد (بالرد عليه).",
    "**-** الردود تعمل تلقائياً فور كتابة الكلمة."
]
