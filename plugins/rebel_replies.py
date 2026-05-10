import os, json
from telethon import events
# استيراد الأدوات اللازمة من الملف الرئيسي
from main import client, CMD_HELP, WAR_IDENTITY

# --- [ تخزين الردود ] ---
REPLIES_DB = "rebel_replies_db.json"

def load_replies():
    if os.path.exists(REPLIES_DB):
        try:
            with open(REPLIES_DB, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}
    return {}

def save_replies(data):
    with open(REPLIES_DB, "w", encoding="utf-8") as f: 
        json.dump(data, f, ensure_ascii=False, indent=4)

R_DB = load_replies()
ADD_MODE = {}

# 1. معالج إضافة رد جديد
@client.on(events.NewMessage(outgoing=True, pattern=r"^اضف رد$"))
async def start_add_reply(event):
    user_id = event.sender_id
    ADD_MODE[user_id] = {"step": 1}
    await event.edit("**🛡️ أهلاً بك في معالج الردود..\nأرسل الآن (الكلمة) التي تريد الرد عليها:**")

@client.on(events.NewMessage(outgoing=True))
async def process_add_reply(event):
    user_id = event.sender_id
    if user_id not in ADD_MODE: return
    
    step = ADD_MODE[user_id]["step"]
    text = event.raw_text

    if step == 1:
        ADD_MODE[user_id].update({"word": text, "step": 2})
        await event.edit(f"**✅ تم حفظ الكلمة: ({text})\nأرسل الآن (الرد) الذي تريد أن يرسله البوت:**")
    
    elif step == 2:
        word = ADD_MODE[user_id]["word"]
        R_DB[word] = text
        save_replies(R_DB)
        del ADD_MODE[user_id]
        await event.edit(f"**🛡️ تم تفعيل الرد بنجاح!\n\n• الكلمة: {word}\n• الرد: {text}**")

# 2. أمر مسح رد (بالرد على الكلمة)
@client.on(events.NewMessage(outgoing=True, pattern=r"^مسح رد$"))
async def delete_reply(event):
    if not event.is_reply:
        return await event.edit("**⚠️ رد على الكلمة التي تريد مسح ردها.**")
    
    reply_msg = await event.get_reply_message()
    word = reply_msg.raw_text
    
    if word in R_DB:
        del R_DB[word]
        save_replies(R_DB)
        await event.edit(f"**🗑️ تم حذف الرد الخاص بـ ({word}) من السجل.**")
    else:
        await event.edit(f"**⚠️ الكلمة ({word}) ليس لها رد محفوظ أصلاً.**")

# 3. تشغيل الردود تلقائياً لجميع المستخدمين
@client.on(events.NewMessage(incoming=True))
async def listen_replies(event):
    if event.raw_text in R_DB:
        await event.reply(R_DB[event.raw_text])

# --- [ دمج الردود مع القسم رقم 17 ] ---
CMD_HELP.update({
    "قسم الردود الذكية": [
        "**• الأمر:** `اضف رد` ⇐ لبدء إضافة رد جديد للسورس.",
        "**• الأمر:** `مسح رد` ⇐ لحذف رد (بالرد على الكلمة).",
        "**• ميزة:** الردود تُحفظ في ملف JSON دائم ولا تضيع.",
        "**• ميزة:** تعمل الردود تلقائياً عند كتابة الكلمة."
    ]
})
