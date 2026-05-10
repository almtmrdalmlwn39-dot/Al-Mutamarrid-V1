import random, os, json, asyncio
from telethon import events
# استدعاء client و CMD_HELP بشكل يضمن التحديث
try:
    from main import client, CMD_HELP
except ImportError:
    from __main__ import client, CMD_HELP

# --- [ التخزين المحلي للألقاب ] ---
G_DB = "rebel_games.json"

def save_g(d):
    with open(G_DB, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=4)

def load_g():
    if os.path.exists(G_DB):
        try:
            with open(G_DB, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}
    return {}

DATA_G = load_g()

# 1. أمر ز (تطوير لإظهار الأسماء بشكل أجمل)
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.زواج$"))
async def marry(e):
    await e.edit("**🔍 جاري البحث عن عرسان...**")
    await asyncio.sleep(1)
    u = await client.get_participants(e.chat_id)
    r = [x for x in u if not x.bot and not x.deleted]
    if len(r) < 2: return await e.edit("**⚠️ مابش أعضاء كفاية في القروب!**")
    a, b = random.sample(r, 2)
    await e.edit(f"**💍 عرسان القروب الليلة:**\n🤵: [{a.first_name}](tg://user?id={a.id})\n👰: [{b.first_name}](tg://user?id={b.id})\n\n**الف مبروك للمتمردين! 😂🔥**")

# 2. أمر كشف الكذب
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.كشف$"))
async def lie(e):
    res = ["كذاب 100% 🤥", "صادق وربي ✅", "بيتمصخر عليكم 😂", "نص نص 🧐", "هذا أصدق واحد بالقروب 🫡"]
    await e.edit(f"**🔍 نتيجة الكشف:**\n{random.choice(res)}")

# 3. أمر ر الألقاب (قلبي، تاج، زوجتي)
@client.on(events.NewMessage(outgoing=True, pattern=r"^رفع (قلبي|تاج|زوجتي)$"))
async def promote(e):
    if not e.is_reply: return await e.edit("**⚠️ رد على الشخص اللي تشتي ترفعه!**")
    t = e.pattern_match.group(1)
    rep = await e.get_reply_message()
    cid, uid = str(e.chat_id), str(rep.sender_id)
    if cid not in DATA_G: DATA_G[cid] = {}
    DATA_G[cid][uid] = t
    save_g(DATA_G)
    await e.edit(f"**🛡️ تم رفع [{rep.sender.first_name}](tg://user?id={uid}) بلقب {t} بنجاح!**")

# 4. أمر م (لمعرفة اللقب)
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.منو$"))
async def who(e):
    if not e.is_reply: return await e.edit("**⚠️ رد على الشخص!**")
    rep = await e.get_reply_message()
    title = DATA_G.get(str(e.chat_id), {}).get(str(rep.sender_id), "عضو عادي")
    await e.edit(f"**👤 العضو:** [{rep.sender.first_name}](tg://user?id={rep.sender_id})\n**👑 لقبه:** {title}")

# --- [ تحديث القائمة لضمان الظهور ] ---
CMD_HELP.update({
    "التقنية والألعاب": [
        "**-** `.ز` ⇐ اختيار عرسان عشوائياً.",
        "**-** `.كشف` ⇐ جهاز كشف الكذب.",
        "**-** `ر قلبي` | `ت تاج` ⇐ لرفع عضو بلقب.",
        "**-** `.م` ⇐ لمعرفة لقب العضو (بالرد)."
    ]
})
