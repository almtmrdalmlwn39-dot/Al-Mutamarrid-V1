import asyncio, random
from telethon import events, functions, types
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from main import client, CMD_HELP

# --- [ AL-MUTAMARRID GROUP IDENTITY ] ---
# البصمة الملكية الموحدة بالخط الإنجليزي العريض
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"
GROUP_BRAND = "**⚖️ 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗖𝗢𝗡𝗧𝗥𝗢𝗟**"

# تسجيل القسم في قائمة المساعدة
CMD_HELP.update({
    "الإدارة والترفيه": [
        "حظر", "طرد", "حظي", "نسبة", "اوامر_الكروب"
    ]
})

# 1. أمر الطرد الملكي (بالرد)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.طرد"))
async def kick_user(event):
    if event.is_private: return
    reply = await event.get_reply_message()
    if not reply: 
        return await event.edit("**⚠️ يـجب الـرد عـلى الـهدف لـطرده مـن الـساحة!**")
    
    await event.edit("**🔄 جـاري تـنفيذ أمـر الـطرد...**")
    try:
        await client.kick_participant(event.chat_id, reply.sender_id)
        await event.edit(
            f"**👞 تـم طـرد الـمخرب بنجاح.**\n"
            f"**👤 الـمطرود: [{reply.sender.first_name}](tg://user?id={reply.sender_id})**\n\n"
            f"{WAR_IDENTITY}"
        )
    except: 
        await event.edit("**⚠️ عـذراً، لا أمـلك صـلاحـيات الإدارة كـامـلة هـنا!**")

# 2. أمر الحظر النهائي (بالرد)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.حظر"))
async def ban_user(event):
    if event.is_private: return
    reply = await event.get_reply_message()
    if not reply: 
        return await event.edit("**⚠️ يـجب الـرد عـلى الـشخص لـنـفـيـه نـهائياً!**")
    
    await event.edit("**🚫 جـاري نـفي الـهدف إلـى خـارج الـمملكة...**")
    try:
        await client(EditBannedRequest(
            event.chat_id, 
            reply.sender_id, 
            ChatBannedRights(until_date=None, view_messages=True)
        ))
        await event.edit(
            f"**🚫 تـم حـظر الـمخرب نـهائياً مـن الـمجموعة.**\n"
            f"**👤 الـمحظور: [{reply.sender.first_name}](tg://user?id={reply.sender_id})**\n\n"
            f"{WAR_IDENTITY}"
        )
    except: 
        await event.edit("**⚠️ نـقص فـي الـصلاحيات الـمطلوبة لـلحظر!**")

# 3. أمر "لعبة الحظ" (ترفيه)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.حظي"))
async def luck_game(event):
    results = ["مـمتاز ✨", "سـيء جـداً 💀", "مـتوسط ⚖️", "أسـطوري 🔥", "نـحس 🌚"]
    await event.edit(
        f"**🔮 نـتـيـجة حـظـك الـيوم مـع الـمتمرد هـي :**\n"
        f"**↳ `{random.choice(results)}`**\n\n"
        f"{WAR_IDENTITY}"
    )

# 4. أمر "نسبة الحب" (مزح)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.نسبة"))
async def love_percent(event):
    reply = await event.get_reply_message()
    name = reply.sender.first_name if reply else "الـمجهول"
    percent = random.randint(0, 100)
    await event.edit(
        f"**❤️ نـسـبة مـحـبـتـك لـ {name} هـي :**\n"
        f"**↳ `{percent}%`**\n\n"
        f"{WAR_IDENTITY}"
    )

# 5. استعراض أوامر الكروب
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اوامر_الكروب"))
async def group_help(event):
    help_text = (
        f"**{GROUP_BRAND}**\n"
        "**— — — — — — — — — —**\n"
        "**🚫 | `.حظر` :** لـنـفي شـخص نـهائياً.\n"
        "**👞 | `.طرد` :** لـتطهير الـساحة مـن الـمخربين.\n"
        "**🔮 | `.حظي` :** لـقراءة الـحظ الـيومي.\n"
        "**❤️ | `.نسبة` :** لـقياس الـنسبة مـع الآخـرين.\n"
        "**— — — — — — — — — —**\n"
        f"{WAR_IDENTITY}"
    )
    await event.edit(help_text)
