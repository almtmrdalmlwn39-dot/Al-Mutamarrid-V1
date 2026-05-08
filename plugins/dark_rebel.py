import asyncio, os, time, re
from datetime import datetime
from telethon import events, functions, types
from telethon.tl.functions.users import GetFullUserRequest
# الربط الصحيح بالمحرك لضمان عدم ظهور خطأ NameError
from main import client, CMD_HELP

# --- [ هوية المتمرد التقنية ] ---
WAR_IDENTITY = "**- قـوةُ الـمتمرد الـتقني | الـإصدار الـأعـنف 🏴‍☠️🛡️**"

# إضافة القسم لقائمة الأوامر العامة بستايل المتمرد المرتب
CMD_HELP.update({
    "ترسانة الهيبة": [
        "فحص", "قصف", "رادار", "مسح", "هيبة"
    ]
})

# 1. أمر كشف معلومات أي شخص (بالرد عليه)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.فحص"))
async def deep_scan(event):
    await event.edit("**- جـاري تـشريح بـيانات الـهدف...**")
    reply = await event.get_reply_message()
    user_id = reply.sender_id if reply else "me"
    try:
        full_user = await client(GetFullUserRequest(user_id))
        user = full_user.users[0]
        res = (
            f"**🧬 نـتيجة الـفحص الـعميق :**\n"
            f"**- الـاسم:** {user.first_name}\n"
            f"**- الآيـدي:** `{user.id}`\n"
            f"**- الـبايو:** `{full_user.full_user.about if full_user.full_user.about else 'خـالي'}`\n"
            f"**— — — — — — — — — —**\n"
            f"{WAR_IDENTITY}"
        )
        await event.edit(res)
    except Exception as e: 
        await event.edit(f"**- فـشل فـي جـلب الـبيانات!**")

# 2. أمر "قصف" (تم تحسين الاستجابة والسرعة)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.قصف"))
async def bomber(event):
    try:
        args = event.text.split(" ", 2)
        if len(args) < 3:
            return await event.edit("**⚠️ استخدامه: `.قصف + العدد + النص`**")
        count = int(args[1])
        text = args[2]
        await event.delete()
        for _ in range(count):
            await client.send_message(event.chat_id, text)
            await asyncio.sleep(0.08) # سرعة متوازنة لمنع الحظر
    except: pass

# 3. أمر "الرادار" (يسحب الروابط بدقة عالية)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.رادار"))
async def link_catcher(event):
    await event.edit("**- جـاري مـسح الـدردشة والـتقاط الـروابط...**")
    links = ""
    async for msg in client.iter_messages(event.chat_id, limit=100):
        if msg.text:
            found = re.findall(r'(https?://\S+)', msg.text)
            for l in found: links += f"🔗 {l}\n"
    if links: await event.edit(f"**📡 الـروابط الـمكتشفة :\n{links}**")
    else: await event.edit("**- لا تـوجد روابـط نـشطة!**")

# 4. أمر "الاختفاء" (تدمير الرسائل)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.مسح"))
async def ghost_mode(event):
    await event.edit("**- جـاري تـدمير الـأدلة والـآثار...**")
    count = 0
    async for msg in client.iter_messages(event.chat_id, from_user="me", limit=100):
        await msg.delete()
        count += 1
    await event.respond(f"**✅ تـم تـدمير {count} رسـالة بـنجاح.**", delete_after=5)

# 5. أمر "الهيبة" (تغيير اسم الكروب)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.هيبة"))
async def power_move(event):
    await event.edit("**- جـاري فـرض الـسيطرة...**")
    try:
        await client(functions.channels.EditTitleRequest(event.chat_id, "تـم الـدعس بـواسطة الـمتمرد 🦅"))
        await event.edit("**✅ تـم تـغيير مـعالم الـساحة.**")
    except: await event.edit("**- لا أمـلك صلاحـيات الـتحكم هـنا!**")
