import random, asyncio, os, json
from telethon import events
from main import client, WAR_IDENTITY

# --- [ تخزين بيانات الألعاب ] ---
GAMES_DB = "rebel_games_db.json"

def load_games():
    if os.path.exists(GAMES_DB):
        try:
            with open(GAMES_DB, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}
    return {}

def save_games(data):
    with open(GAMES_DB, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=4)

G_DB = load_games()

# 1. أوامر الرفع (بالرد)
@client.on(events.NewMessage(outgoing=True))
async def promotions(event):
    text = event.raw_text
    chat_id = str(event.chat_id)
    
    # أوامر الرفع المتاحة
    titles = {
        "رفع زوجتي": "💍 زوجته المصونة",
        "رفع تاج": "👑 تاجه وراسه",
        "رفع قلبي": "❤️ قطعة من قلبه",
        "رفع كلب": "🐕 الكلب الوفي حق القروب",
        "رفع بصلة": "🧅 بصلة القروب المعفنة",
        "رفع قمر": "🌕 قمر القروب"
    }

    if event.is_reply and text in titles:
        reply = await event.get_reply_message()
        user_id = str(reply.sender_id)
        user_name = reply.sender.first_name
        
        if chat_id not in G_DB: G_DB[chat_id] = {}
        G_DB[chat_id][user_id] = titles[text]
        save_games(G_DB)
        
        await event.edit(f"**🛡️ تم رفـع الـعـضو:** [{user_name}](tg://user?id={user_id})\n**👑 الـلقب:** {titles[text]}")

# 2. أمر "منو" لمعرفة اللقب
@client.on(events.NewMessage(outgoing=True, pattern=r"^منو$"))
async def who_is(event):
    if not event.is_reply: return await event.edit("**⚠️ رد على الشخص عشان أبسر لقبه.**")
    reply = await event.get_reply_message()
    user_id = str(reply.sender_id)
    chat_id = str(event.chat_id)
    
    title = G_DB.get(chat_id, {}).get(user_id, "عضو ماله أي لقب حالياً 🤷‍♂️")
    await event.edit(f"**🛡️ لـقب الـعضو في سورس المتمرد:**\n\n**👤 الاسـم:** {reply.sender.first_name}\n**👑 الـلـقب:** {title}")

# 3. لعبة الزواج العشوائي
@client.on(events.NewMessage(outgoing=True, pattern=r"^زواج$"))
async def random_marry(event):
    users = await client.get_participants(event.chat_id)
    # تصفية البوتات والحسابات المحذوفة
    real_users = [u for u in users if not u.bot and not u.deleted]
    if len(real_users) < 2: return await event.edit("**⚠️ مابش أعضاء كفاية للزواج!**")
    
    u1, u2 = random.sample(real_users, 2)
    await event.edit(f"**💍 باركوا لأطلق عرسان في القروب:**\n\n**🤵 العريس:** [{u1.first_name}](tg://user?id={u1.id})\n**👰 العروسة:** [{u2.first_name}](tg://user?id={u2.id})\n\n**ألف مبروك، منك المال ومنها العيال! 😂**")

# 4. ألعاب النسب (بالرد)
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.(نسبة الحب|نسبة الغباء|نسبة الانوثة|نسبة الرجولة)$"))
async def percents(event):
    cmd = event.pattern_match.group(1)
    percent = random.randint(0, 100)
    if event.is_reply:
        reply = await event.get_reply_message()
        await event.edit(f"**🛡️ {cmd} لـ [{reply.sender.first_name}](tg://user?id={reply.sender_id}) هي: {percent}%**")
    else:
        await event.edit(f"**🛡️ {cmd} عندك هي: {percent}%**")

# 5. لعبة كشف الكذب
@client.on(events.NewMessage(outgoing=True, pattern=r"^كشف$"))
async def lie_detector(event):
    if not event.is_reply: return await event.edit("**⚠️ رد على الشخص اللي تبي تكشفه!**")
    res = random.choice(["كذاب ومن الدرجة الأولى 🤥", "صادق والله، أهنيك ✅", "نص نص، فيه شوية بهارات 🌶️", "أشك في كلامه!"])
    await event.edit(f"**🛡️ جهاز كشف الكذب يقول:**\n\n**[{res}]**")
