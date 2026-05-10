import os, json, asyncio
from telethon import events
# استيراد الأدوات من الملف الرئيسي بشكل آمن
try:
    from main import client, CMD_HELP
except ImportError:
    from __main__ import client, CMD_HELP

# --- [ إعدادات التخزين ] ---
R_DB_FILE = "rebel_replies.json"

def load_db():
    if os.path.exists(R_DB_FILE):
        try:
            with open(R_DB_FILE, "r", encoding="utf-8") as f: 
                return json.load(f)
        except: return {}
    return {}

def save_db(data):
    with open(R_DB_FILE, "w", encoding="utf-8") as f: 
        json.dump(data, f, ensure_ascii=False, indent=4)

# تحميل الردود عند بدء التشغيل
REPLIES = load_db()
ADD_MODE = {}

# 1. أمر إضافة رد جديد
@client.on(events.NewMessage(outgoing=True, pattern=r"^اضف رد$"))
async def start_add(event):
    ADD_MODE[event.sender_id] = {"step": 1}
    await event.edit("**🛡️ أهلاً بك في معالج الردود..\nأرسل الآن (الكلمة) التي تريد الرد عليها:**")

# 2. معالج خطوات الإضافة
@client.on(events.NewMessage(outgoing=True))
async def handle_addition(event):
    uid = event.sender_id
    if uid not in ADD_MODE or event.raw_text == "اضف رد":
        return

    step = ADD_MODE[uid]["step"]
    
    if step == 1:
        word = event.raw_text
        ADD_MODE[uid].update({"word": word, "step": 2})
        await event.edit(f"**✅ تم حفظ الكلمة: ({word})\nأرسل الآن (الرد) المطلوب:**")
    
    elif step == 2:
        word = ADD_MODE[uid]["word"]
        reply_text = event.raw_text
        REPLIES[word] = reply_text
        save_db(REPLIES)
        del ADD_MODE[uid]
        await event.edit(f"**🛡️ تم تفعيل الرد بنجاح!\n• الكلمة: {word}\n• الرد: {reply_text}**")

# 3. معالج الرد التلقائي الشامل (مطور)
@client.on(events.NewMessage(incoming=True)) # للرد على الآخرين
async def auto_reply_others(event):
    # تحديث الذاكرة لضمان قراءة الردود الجديدة
    current_replies = load_db()
    if event.raw_text in current_replies:
        await event.reply(current_replies[event.raw_text])

@client.on(events.NewMessage(outgoing=True)) # للرد على رسائلك أنت
async def auto_reply_self(event):
    if event.sender_id in ADD_MODE: return
    current_replies = load_db()
    if event.raw_text in current_replies:
        await event.respond(current_replies[event.raw_text])

# 4. أمر مسح رد
@client.on(events.NewMessage(outgoing=True, pattern=r"^مسح رد$"))
async def delete_rep(event):
    if not event.is_reply: 
        return await event.edit("**⚠️ رد على الكلمة التي تريد مسح ردها.**")
    reply = await event.get_reply_message()
    word = reply.raw_text
    if word in REPLIES:
        del REPLIES[word]
        save_db(REPLIES)
        await event.edit(f"**🗑️ تم حذف الرد لـ ({word})**")
    else:
        await event.edit("**⚠️ هذه الكلمة ليس لها رد مبرمج.**")

# --- [ تحديث القائمة لضمان الظهور في م17 ] ---
CMD_HELP.update({
    "قسم الردود الذكية": [
        "**-** `اضف رد` ⇐ إضافة رد جديد.",
        "**-** `مسح رد` ⇐ حذف رد (بالرد عليه).",
        "**-** الردود تعمل تلقائياً فور كتابة الكلمة."
    ]
})
