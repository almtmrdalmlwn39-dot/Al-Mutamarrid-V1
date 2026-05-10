import random, os, json
from telethon import events
from main import client, CMD_HELP

# --- [ التخزين ] ---
R_DB = "rebel_replies.json"
def save(data): json.dump(data, open(R_DB, "w", encoding="utf-8"), ensure_ascii=False, indent=4)
def load(): return json.load(open(R_DB, "r", encoding="utf-8")) if os.path.exists(R_DB) else {}
REPLIES = load()
ADD_M = {}

# --- [ أوامر القسم 11: التقنية والألعاب ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"^زواج$"))
async def mry(e):
    u = await client.get_participants(e.chat_id)
    r = [x for x in u if not x.bot]
    a, b = random.sample(r, 2)
    await e.edit(f"**💍 عرسان القروب:**\n🤵: [{a.first_name}](tg://user?id={a.id})\n👰: [{b.first_name}](tg://user?id={b.id})")

# --- [ أوامر القسم 17: الردود الذكية ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"^اضف رد$"))
async def add(e):
    ADD_M[e.sender_id] = {"s": 1}
    await e.edit("**🛡️ أرسل الكلمة الآن:**")

@client.on(events.NewMessage(outgoing=True))
async def hndl(e):
    uid = e.sender_id
    if uid not in ADD_M or e.raw_text == "اضف رد": return
    if ADD_M[uid]["s"] == 1:
        ADD_M[uid].update({"w": e.raw_text, "s": 2})
        await e.edit(f"**✅ حفظنا ({e.raw_text})، أرسل الرد:**")
    elif ADD_M[uid]["s"] == 2:
        REPLIES[ADD_M[uid]["w"]] = e.raw_text
        save(REPLIES); del ADD_M[uid]
        await e.edit("**🛡️ تم حفظ الرد بنجاح!**")

@client.on(events.NewMessage(incoming=True))
async def auto(e):
    if e.raw_text in REPLIES: await e.reply(REPLIES[e.raw_text])

# --- [ التحديث الإجباري للقوائم ] ---
CMD_HELP["التقنية والألعاب"] = [
    "**-** `زواج` | `كشف` | `منو`",
    "**-** `رفع تاج` | `رفع قلبي`",
    "**-** أوامر التقنية الأساسية شغالـة."
]

CMD_HELP["قسم الردود الذكية"] = [
    "**-** `اضف رد` ⇐ لإضافة رد جديد.",
    "**-** `مسح رد` ⇐ لحذف الرد بالرد عليه.",
    "**-** الردود تُحفظ دائمياً."
]
