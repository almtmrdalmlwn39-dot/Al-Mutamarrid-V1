import random, os, json
from telethon import events
from main import client, CMD_HELP

# --- [ التخزين المحلي للألقاب ] ---
G_DB = "rebel_games.json"
def save(d): json.dump(d, open(G_DB, "w", encoding="utf-8"), ensure_ascii=False, indent=4)
def load(): return json.load(open(G_DB, "r", encoding="utf-8")) if os.path.exists(G_DB) else {}
DATA = load()

# 1. أمر الزواج (اللي شغال عندك)
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.زواج$"))
async def marry(e):
    u = await client.get_participants(e.chat_id)
    r = [x for x in u if not x.bot]
    a, b = random.sample(r, 2)
    await e.edit(f"**💍 عرسان القروب:**\n🤵: [{a.first_name}](tg://user?id={a.id})\n👰: [{b.first_name}](tg://user?id={b.id})")

# 2. أمر كشف الكذب
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.كشف$"))
async def lie(e):
    res = ["كذاب 100% 🤥", "صادق وربي ✅", "بيتمصخر عليكم 😂", "نص نص 🧐"]
    await e.edit(f"**🔍 نتيجة الكشف:**\n{random.choice(res)}")

# 3. أمر رفع الألقاب (قلبي، تاج، زوجتي)
@client.on(events.NewMessage(outgoing=True, pattern=r"^رفع (قلبي|تاج|زوجتي)$"))
async def promote(e):
    if not e.is_reply: return await e.edit("**⚠️ رد على الشخص أولاً!**")
    t = e.pattern_match.group(1)
    rep = await e.get_reply_message()
    cid, uid = str(e.chat_id), str(rep.sender_id)
    if cid not in DATA: DATA[cid] = {}
    DATA[cid][uid] = t
    save(DATA)
    await e.edit(f"**🛡️ تم رفع [{rep.sender.first_name}](tg://user?id={uid}) بلقب {t} بنجاح!**")

# 4. أمر منو (لمعرفة اللقب)
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.منو$"))
async def who(e):
    if not e.is_reply: return await e.edit("**⚠️ رد على الشخص!**")
    rep = await e.get_reply_message()
    title = DATA.get(str(e.chat_id), {}).get(str(rep.sender_id), "عضو عادي")
    await e.edit(f"**👤 العضو:** [{rep.sender.first_name}](tg://user?id={rep.sender_id})\n**👑 لقبه:** {title}")

# --- [ تحديث القائمة 11 ] ---
CMD_HELP["التقنية والألعاب"] = [
    "**-** `.زواج` ⇐ اختيار عرسان عشوائياً.",
    "**-** `.كشف` ⇐ جهاز كشف الكذب.",
    "**-** `رفع قلبي/تاج` ⇐ لرفع عضو بلقب.",
    "**-** `.منو` ⇐ لمعرفة لقب العضو (بالرد)."
]
