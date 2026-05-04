import asyncio, os, time, re
from datetime import datetime
from telethon import events, functions, types
from telethon.tl.functions.users import GetFullUserRequest
from __main__ import client 

# --- [ هوية المتمرد التقنية ] ---
WAR_IDENTITY = "**- قـوةُ الـمتمرد الـتقني | الـإصدار الـأعـنف 🏴‍☠️🛡️**"

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
    except: await event.edit("**- فـشل فـي جـلب الـبيانات!**")

# 2. أمر "قصف" (تكرار نص معين بسرعة عالية جداً)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.قصف"))
async def bomber(event):
    try:
        args = event.text.split(" ", 2)
        count = int(args[1])
        text = args[2]
        await event.delete()
        for _ in range(count):
            await client.send_message(event.chat_id, text)
            await asyncio.sleep(0.05) # سرعة جنونية
    except: pass

# 3. أمر "الرادار" (يسحب كل روابط الدعوة والروابط في آخر 100 رسالة)
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

# 4. أمر "الاختفاء" (يحذف كل رسائلك في الكروب أو الخاص بضغطة واحدة)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.مسح"))
async def ghost_mode(event):
    await event.edit("**- جـاري تـدمير الـأدلة والـآثار...**")
    async for msg in client.iter_messages(event.chat_id, from_user="me", limit=100):
        await msg.delete()

# 5. أمر "الهيبة" (يغير اسم الكروب وصورته في ثوانٍ - للمشرفين)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.هيبة"))
async def power_move(event):
    await event.edit("**- جـاري فـرض الـسيطرة...**")
    try:
        await client(functions.channels.EditTitleRequest(event.chat_id, "تـم الـدعس بـواسطة الـمتمرد 🦅"))
        await event.edit("**✅ تـم تـغيير مـعالم الـساحة.**")
    except: await event.edit("**- لا أمـلك صلاحـيات الـتحكم هـنا!**")

# 6. أمر قائمة الأدوات الجديدة
@client.on(events.NewMessage(outgoing=True, pattern=r"\.الادوات"))
async def tool_list(event):
    msg = (
        "**🛠️ تـرسانة الـمتمرد الـتقنية :**\n"
        "**— — — — — — — — — —**\n"
        "**🔍 | .فحص :** لـكشف بـيانات أي شـخص.\n"
        "**🚀 | .قصف + العدد + النص :** لـإرسال رسـائل سـريعة.\n"
        "**📡 | .رادار :** لـسحب جـميع الـروابط مـن الـمحادثة.\n"
        "**🧹 | .مسح :** لـحذف كـل رسـائلك فـي الـدردشة.\n"
        "**🦅 | .هيبة :** لـتغيير اسـم الـمجموعة فوراً.\n"
        "**— — — — — — — — — —**\n"
        f"{WAR_IDENTITY}"
    )
    await event.edit(msg)
