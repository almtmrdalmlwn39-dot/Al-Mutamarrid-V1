import asyncio
from telethon import events, functions, types
import main 

client = main.client
ID_REBEL = "**- نـظام الـمتمرد الـتقني | مـيزات الـسيطرة 🛡️**"

# 1. ميزة تغيير الهوية
@client.on(events.NewMessage(outgoing=True, pattern=r'^\.تغيير (.*)'))
async def change_rebel(event):
    new_name = event.pattern_match.group(1)
    try:
        await client(functions.account.UpdateProfileRequest(first_name=new_name))
        await event.edit(f"**🎭 تـم تـغيير الـهوية إلـى: {new_name}\n\n{ID_REBEL}**")
    except Exception as e:
        await event.edit(f"⚠️ **فشل التغيير:** {e}")

# 2. ميزة القراءة المتخفية (تم تصحيح الدالة هنا)
@client.on(events.NewMessage(outgoing=True, pattern=r'^\.تسلل'))
async def sneaky_read(event):
    await event.edit("**👁️ جـاري قـراءة الـمحادثة بـشكل مـخفي..**")
    try:
        await client(functions.messages.ReadHistoryRequest(peer=event.chat_id, max_id=0))
        await asyncio.sleep(1)
        await event.edit(f"**✅ تـم الـتسلل وقـراءة الـرسايل بنجاح!\n\n{ID_REBEL}**")
    except Exception as e:
        await event.edit(f"⚠️ **خطأ في التسلل:** {e}")

# 3. ميزة إغراق الدردشة
@client.on(events.NewMessage(outgoing=True, pattern=r'^\.كرر (\d+) (.*)'))
async def rebel_spam(event):
    count = int(event.pattern_match.group(1))
    text = event.pattern_match.group(2)
    await event.delete()
    for _ in range(count):
        await client.send_message(event.chat_id, text)
        await asyncio.sleep(0.5) # زيادة الوقت قليلاً لتجنب الحظر

# 4. قائمة أوامر الميزات
@client.on(events.NewMessage(outgoing=True, pattern=r'^\.مميزاتي'))
async def features_help(event):
    help_text = (
        "**⚡️ أوامـر الـسيطرة والـتميز :**\n"
        "**— — — — — — — — — —**\n"
        "**🎭 | `.تغيير [الاسم]` :** لـتغيير اسـم حـسابك فـوراً.\n"
        "**👁️ | `.تسلل` :** لـقراءة الـرسايل بـدون ظـهور الـصحين.\n"
        "**🔥 | `.كرر [العدد] [النص]` :** لإغـراق الـدردشة بـالـرسائل.\n"
        "**— — — — — — — — — —**\n"
        f"{ID_REBEL}"
    )
    await event.edit(help_text)
