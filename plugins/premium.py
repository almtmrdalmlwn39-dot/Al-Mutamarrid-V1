import asyncio
from telethon import events, functions, types
from main import client, CMD_HELP

# --- [ AL-MUTAMARRID PREMIUM IDENTITY ] ---
# البصمة الملكية الموحدة بالخط الإنجليزي العريض
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"

# تسجيل القسم في قائمة المساعدة
CMD_HELP.update({
    "ميزات السيطرة": [
        "تغيير", "تسلل", "كرر", "مميزاتي"
    ]
})

# 1. ميزة تغيير الهوية (الاسم الأول)
@client.on(events.NewMessage(outgoing=True, pattern=r'^\.تغيير (.*)'))
async def change_rebel(event):
    new_name = event.pattern_match.group(1)
    try:
        await client(functions.account.UpdateProfileRequest(first_name=new_name))
        await event.edit(f"**🎭 تـم تـغيير الـهوية إلـى: {new_name}**\n\n{WAR_IDENTITY}")
    except Exception as e:
        await event.edit(f"⚠️ **فشل التغيير:** {e}")

# 2. ميزة القراءة المتخفية (التسلل)
@client.on(events.NewMessage(outgoing=True, pattern=r'^\.تسلل'))
async def sneaky_read(event):
    await event.edit("**👁️ جـاري الـتسلل وقـراءة الـمحادثة بـصمت..**")
    try:
        await client(functions.messages.ReadHistoryRequest(peer=event.chat_id, max_id=0))
        await asyncio.sleep(1)
        await event.edit(f"**✅ تـم الـتسلل وقـراءة الـرسايل بـنجاح!**\n\n{WAR_IDENTITY}")
    except Exception as e:
        await event.edit(f"⚠️ **خطأ في التسلل:** {e}")

# 3. ميزة التكرار (إغراق الدردشة)
@client.on(events.NewMessage(outgoing=True, pattern=r'^\.كرر (\d+) (.*)'))
async def rebel_spam(event):
    count = int(event.pattern_match.group(1))
    text = event.pattern_match.group(2)
    await event.delete()
    for _ in range(count):
        await client.send_message(event.chat_id, text)
        await asyncio.sleep(0.5) # حماية من الحظر (Flood)

# 4. قائمة أوامر الميزات (بصياغة فخمة)
@client.on(events.NewMessage(outgoing=True, pattern=r'^\.مميزاتي'))
async def features_help(event):
    help_text = (
        "**⚡️ أوامـر الـسيطرة والـتـميّز :**\n"
        "**— — — — — — — — — —**\n"
        "**🎭 | `.تغيير [الاسم]` :** لـتغيير اسـم حـسابك فـوراً.\n"
        "**👁️ | `.تسلل` :** لـقراءة الـرسايل بـدون ظـهور الـصحين.\n"
        "**🔥 | `.كرر [العدد] [النص]` :** لإغـراق الـدردشة بـالـرسائل.\n"
        "**— — — — — — — — — —**\n"
        f"{WAR_IDENTITY}"
    )
    await event.edit(help_text)
