import random, asyncio, os, json
from telethon import events
from main import client, WAR_IDENTITY, CMD_HELP 

GAMES_DB = "rebel_games_db.json"
def load_db():
    if os.path.exists(GAMES_DB):
        try:
            with open(GAMES_DB, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}
    return {}
def save_db(data):
    with open(GAMES_DB, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=4)
G_DB = load_db()

@client.on(events.NewMessage(outgoing=True))
async def promotions(event):
    text = event.raw_text
    titles = {"رفع زوجتي": "💍 زوجته المصونة", "رفع تاج": "👑 تاجه وراسه", "رفع قلبي": "❤️ قطعة من قلبه", "رفع كلب": "🐕 الكلب الوفي", "رفع قمر": "🌕 قمر القروب"}
    if event.is_reply and text in titles:
        reply = await event.get_reply_message()
        cid, uid = str(event.chat_id), str(reply.sender_id)
        if cid not in G_DB: G_DB[cid] = {}
        G_DB[cid][uid] = titles[text]
        save_db(G_DB)
        await event.edit(f"**🛡️ تم رفـع الـعـضو:** [{reply.sender.first_name}](tg://user?id={uid})\n**👑 الـلقب:** {titles[text]}")

@client.on(events.NewMessage(outgoing=True, pattern=r"^منو$"))
async def who_is(event):
    if not event.is_reply: return await event.edit("**⚠️ رد على الشخص.**")
    reply = await event.get_reply_message()
    title = G_DB.get(str(event.chat_id), {}).get(str(reply.sender_id), "عضو بلا لقب")
    await event.edit(f"**👤 الاسـم:** {reply.sender.first_name}\n**👑 الـلـقب:** {title}")

@client.on(events.NewMessage(outgoing=True, pattern=r"^زواج$"))
async def random_marry(event):
    users = await client.get_participants(event.chat_id)
    real = [u for u in users if not u.bot and not u.deleted]
    if len(real) < 2: return await event.edit("**⚠️ مابش أعضاء.**")
    u1, u2 = random.sample(real, 2)
    await event.edit(f"**🤵 العريس:** [{u1.first_name}](tg://user?id={u1.id})\n**👰 العروسة:** [{u2.first_name}](tg://user?id={u2.id})\n**ألف مبروك! 😂**")

CMD_HELP.update({
    "التقنية والألعاب": [
        "**• أوامر التسلية والرفع الجديدة:**",
        "**-** `زواج` ، `كشف` ، `منو`",
        "**-** `رفع تاج` ، `رفع قلبي` ، `رفع زوجتي`",
        "**--------------------------**",
        "**• أوامر التقنية:** (تسريع، تشكيلة، تقييم)"
    ]
})
