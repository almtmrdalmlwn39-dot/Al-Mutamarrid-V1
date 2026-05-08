import random
from telethon import events, functions
from main import client, CMD_HELP

# --- [ AL-MUTAMARRID GLOBAL IDENTITY ] ---
# البصمة الإنجليزية الفخمة التي تظهر في نهاية كل رسالة
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"

# إضافة القسم للقائمة
CMD_HELP.update({
    "الإضافات والترفيه": [
        "حب", "كذب", "غادر", "الرابط", "ايدي"
    ]
})

# --- [ 1. أوامر التسلية والترفيه ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.نسبة الحب"))
async def love(event):
    score = random.randint(0, 100)
    await event.edit(f"**❤️ نسبة الحب هي : {score}%**\n\n{WAR_IDENTITY}")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.كشف الكذب"))
async def lie(event):
    results = ["كاذب ❌", "صادق ✅", "نصاب كبير 🤡", "ماشاء الله صادق 🙏"]
    res = random.choice(results)
    await event.edit(f"**⚖️ النتيجة هي : {res}**\n\n{WAR_IDENTITY}")

# --- [ 2. أوامر المجموعات الإضافية ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.غادر"))
async def leave(event):
    await event.edit(f"**🦅 المتمرد يغادر المكان.. وداعاً**\n\n{WAR_IDENTITY}")
    await client(functions.channels.LeaveChannelRequest(event.chat_id))

@client.on(events.NewMessage(outgoing=True, pattern=r"\.الرابط"))
async def get_link(event):
    try:
        res = await client(functions.messages.ExportChatInviteRequest(event.chat_id))
        await event.edit(f"**🔗 رابط المجموعة : {res.link}**\n\n{WAR_IDENTITY}")
    except:
        await event.edit("**❌ لا أملك صلاحيات لاستخراج الرابط!**")

# --- [ 3. أوامر المعلومات ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.ايدي"))
async def get_id(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        await event.edit(f"**👤 ايدي الشخص : `{reply.sender_id}`**\n\n{WAR_IDENTITY}")
    else:
        await event.edit(f"**📍 ايدي الدردشة : `{event.chat_id}`**\n\n{WAR_IDENTITY}")
