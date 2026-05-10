import os, json
from telethon import events
from main import client, CMD_HELP, WAR_IDENTITY

# --- [ تخزين الردود ] ---
REPLIES_DB = "rebel_replies_db.json"
def load_db():
    if os.path.exists(REPLIES_DB):
        try:
            with open(REPLIES_DB, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}
    return {}
def save_db(data):
    with open(REPLIES_DB, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=4)
R_DB = load_db()
ADD_MODE = {}

# --- [ الأوامر ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"^اضف رد$"))
async def start_add(event):
    ADD_MODE[event.sender_id] = {"step": 1}
    await event.edit("**🛡️ أرسل الآن الكلمة التي تريد الرد عليها:**")

@client.on(events.NewMessage(outgoing=True))
async def handle_steps(event):
    uid = event.sender_id
    if uid not in ADD_MODE or event.raw_text == "اضف رد": return
    if ADD_MODE[uid]["step"] == 1:
        ADD_MODE[uid].update({"word": event.raw_text, "step": 2})
        await event.edit(f"**✅ حفظنا ({event.raw_text})، أرسل الرد الآن:**")
    elif ADD_MODE[uid]["step"] == 2:
        R_DB[ADD_MODE[uid]["word"]] = event.raw_text
        save_db(R_DB)
        del ADD_MODE[uid]
        await event.edit(f"**🛡️ تم حفظ الرد بنجاح!**")

@client.on(events.NewMessage(incoming=True))
async def replies(event):
    if event.raw_text in R_DB: await event.reply(R_DB[event.raw_text])

# --- [ التحديث للقائمة 17 ] ---
CMD_HELP.update({
    "قسم الردود الذكية": [
        "**• أوامـر الـردود:**",
        "**-** `اضف رد` ⇐ لإضافة رد جديد.",
        "**-** `الردود` ⇐ عرض ردودك المحفوظة.",
        "**-** `مسح رد` ⇐ لحذف رد بالرد عليه.",
        "**--------------------------**",
        "**• ميزة:** الردود تُحفظ في ملف JSON."
    ]
})
