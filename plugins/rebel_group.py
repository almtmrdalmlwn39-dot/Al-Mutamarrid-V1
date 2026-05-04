import asyncio, random
from telethon import events, functions, types
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from __main__ import client 

# هوية الإدارة
GROUP_IDENTITY = "**- قـطاع الـسيطرة والـترفيه | الـمتمرد الـتقني 🦅⚖️**"

# 1. أمر الطرد (بالرد على الشخص)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.طرد"))
async def kick_user(event):
    if event.is_private: return
    reply = await event.get_reply_message()
    if not reply: return await event.edit("**- يـجب الـرد عـلى مـستخدم لـطرده!**")
    await event.edit("**- جـاري طـرد الـهدف مـن الـمجموعة...**")
    try:
        await client.kick_participant(event.chat_id, reply.sender_id)
        await event.edit(f"**✅ تـم طـرد [{reply.sender_name}](tg://user?id={reply.sender_id}) بـنجاح.**")
    except: await event.edit("**- لا أمـلك صلاحـيات الـطرد هـنا!**")

# 2. أمر الحظر (بالرد على الشخص)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.حظر"))
async def ban_user(event):
    if event.is_private: return
    reply = await event.get_reply_message()
    if not reply: return await event.edit("**- يـجب الـرد عـلى مـستخدم لـحظره!**")
    await event.edit("**- جـاري نـفي الـهدف نـهائياً...**")
    try:
        await client(EditBannedRequest(event.chat_id, reply.sender_id, ChatBannedRights(until_date=None, view_messages=True)))
        await event.edit(f"**🚫 تـم حـظر [{reply.sender_name}](tg://user?id={reply.sender_id}) لـلأبد.**")
    except: await event.edit("**- نـقص فـي الـصلاحيات!**")

# 3. أمر "لعبة الحظ" (ترفيه)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.حظي"))
async def luck_game(event):
    results = ["مـمتاز ✨", "سـيء جـداً 💀", "مـتوسط ⚖️", "أسـطوري 🔥", "نـحس 🌚"]
    await event.edit(f"**🔮 نـتيجة حـظك الـيوم هـي : `{random.choice(results)}`**")

# 4. أمر "نسبة الحب" (مزح)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.نسبة"))
async def love_percent(event):
    reply = await event.get_reply_message()
    name = reply.first_name if reply else "الـمجهول"
    percent = random.randint(0, 100)
    await event.edit(f"**❤️ نـسبة مـحبتك لـ {name} هـي : `{percent}%`**")

# --- [ قسم استعراض الأوامر المدمج ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اوامر_الكروب"))
async def group_help(event):
    help_text = (
        "**⚖️ أوامـر الـسيطرة والـترفيه :**\n"
        "**— — — — — — — — — —**\n"
        "**🚫 | `.حظر` :** لـحظر شـخص مـن الـمجموعة (بالرد).\n"
        "**👞 | `.طرد` :** لـطرد شـخص مـن الـمجموعة (بالرد).\n"
        "**🔮 | `.حظي` :** لـمعرفة حـظك الـيوم.\n"
        "**❤️ | `.نسبة` :** لـقياس الـنسبة مـع الـطرف الآخـر.\n"
        "**— — — — — — — — — —**\n"
        f"{GROUP_IDENTITY}"
    )
    await event.edit(help_text)
