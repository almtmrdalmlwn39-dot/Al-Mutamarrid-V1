import asyncio, time
from datetime import datetime
from telethon import events, functions, types
from __main__ import client 

# هوية الأدوات
TOOL_IDENTITY = "**- مـختبر الأدوات الـمتقدمة | الـمتمرد الـتقني 🛠️⚡**"

# 1. أمر معرفة الوقت والتاريخ في اليمن (بشكل فخم)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.الوقت"))
async def get_time(event):
    now = datetime.now()
    time_str = now.strftime("%I:%M %p")
    date_str = now.strftime("%Y/%m/%d")
    await event.edit(f"**🕒 الـتوقيت الـآن فـي الـيمن :**\n**— — — — — — — — — —**\n**- الـساعة:** `{time_str}`\n**- الـتاريخ:** `{date_str}`\n**— — — — — — — — — —**\n{TOOL_IDENTITY}")

# 2. أمر استخراج رابط أي صورة أو فيديو (للمطورين)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.رابط"))
async def get_link(event):
    reply = await event.get_reply_message()
    if not reply or not reply.media:
        return await event.edit("**- يـجب الـرد عـلى وسـائط (صـورة/فـيديو) أولاً!**")
    await event.edit("**- جـاري تـوليد رابـط الـميديا...**")
    # ملاحظة: يعطيك رابط داخلي للتليجرام يسهل الوصول إليه
    try:
        msg_link = f"https://t.me/c/{str(event.chat_id)[4:]}/{reply.id}"
        await event.edit(f"**🔗 رابـط الـرسالة الـمباشر :\n\n`{msg_link}`\n\n{TOOL_IDENTITY}**")
    except: await event.edit("**- فـشل فـي تـوليد الـرابط.**")

# 3. أمر "العد التنازلي" (مفيد للمسابقات أو الانتظار)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.عد (.*)"))
async def countdown(event):
    seconds = int(event.pattern_match.group(1))
    await event.edit(f"**⏳ بـدأ الـعد الـتنازلي لـثوانٍ: `{seconds}`**")
    for i in range(seconds, 0, -1):
        await event.edit(f"**🧨 الـانفجار بـعد: `{i}`**")
        await asyncio.sleep(1)
    await event.edit("**💥 بـووووم ! تـم الـوقت.**")

# 4. أمر "تحويل النص إلى ملف" (مثلا لو كتبت كود طويل)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.لملف (.*)"))
async def text_to_file(event):
    text = event.pattern_match.group(1)
    await event.edit("**- جـاري تـحويل الـنص إلـى مـلف وتـرفيعه...**")
    with open("rebel_doc.txt", "w") as f:
        f.write(text)
    await client.send_file(event.chat_id, "rebel_doc.txt", caption=f"**✅ تـم تـحويل الـنص لـملف بنـجاح.\n\n{TOOL_IDENTITY}**")
    import os
    os.remove("rebel_doc.txt")
    await event.delete()

# --- [ قسم استعراض أوامر الأدوات ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اوامر_الادوات"))
async def tools_help(event):
    help_text = (
        "**🛠️ أوامـر الأدوات والـتحويلات :**\n"
        "**— — — — — — — — — —**\n"
        "**🕒 | `.الوقت` :** لـمعرفة الـوقت والـتاريخ الـآن.\n"
        "**🔗 | `.رابط` :** لـسحب رابـط أي مـيديا (بالرد).\n"
        "**🧨 | `.عد [ثواني]` :** لـعمل عـد تـنازلي حـماسي.\n"
        "**📄 | `.لملف [النص]` :** لـتحويل أي كـلام لـملف نصي.\n"
        "**— — — — — — — — — —**\n"
        f"{TOOL_IDENTITY}"
    )
    await event.edit(help_text)
