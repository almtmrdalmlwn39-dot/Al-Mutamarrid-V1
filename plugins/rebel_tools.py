import asyncio, os
from datetime import datetime
from telethon import events, functions, types
from main import client, CMD_HELP

# --- [ AL-MUTAMARRID TOOLS BRAND ] ---
# الهوية الموحدة لضمان ثبات الحقوق والمظهر الملكي
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"
TOOL_BRAND = "**🛠️ 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗧𝗢𝗢𝗟𝗦**"

# تسجيل القسم في قائمة المساعدة
CMD_HELP.update({
    "الأدوات والتحويلات": [
        "الوقت", "رابط", "عد", "لملف", "اوامر_الادوات"
    ]
})

# 1. أمر الوقت والتاريخ (بتوقيت اليمن الفخم)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.الوقت"))
async def get_time(event):
    now = datetime.now()
    time_str = now.strftime("%I:%M %p")
    date_str = now.strftime("%Y/%m/%d")
    await event.edit(
        f"**🕒 الـتوقيت الـآن فـي الـيمن الـحبيب :**\n"
        f"**— — — — — — — — — — —**\n"
        f"**- الـساعة:** `{time_str}`\n"
        f"**- الـتاريخ:** `{date_str}`\n"
        f"**— — — — — — — — — — —**\n"
        f"{WAR_IDENTITY}"
    )

# 2. أمر استخراج رابط الميديا (داخلي)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.رابط"))
async def get_link(event):
    reply = await event.get_reply_message()
    if not reply or not reply.media:
        return await event.edit("**⚠️ يـجب الـرد عـلى مـيديا (صـورة/فـيديو) أولاً!**")
    
    await event.edit("**🔄 جـاري تـوليد رابـط الـوصول الـسريع...**")
    try:
        # توليد رابط مباشر للرسالة يسهل العودة إليها
        chat_id = str(event.chat_id).replace("-100", "")
        msg_link = f"https://t.me/c/{chat_id}/{reply.id}"
        await event.edit(
            f"**🔗 رابـط الـميديا الـمباشر :**\n\n"
            f"`{msg_link}`\n\n"
            f"{WAR_IDENTITY}"
        )
    except Exception as e:
        await event.edit(f"**❌ فـشل التوليد:** `{e}`")

# 3. أمر العد التنازلي الحماسي
@client.on(events.NewMessage(outgoing=True, pattern=r"\.عد (.*)"))
async def countdown(event):
    try:
        seconds = int(event.pattern_match.group(1))
        await event.edit(f"**⏳ بـدأ الـتـنـازل لـمـدة: `{seconds}` ثـانـية**")
        await asyncio.sleep(1)
        
        for i in range(seconds, 0, -1):
            await event.edit(f"**🧨 الـانـفـجـار بـعـد: `{i}`**")
            await asyncio.sleep(1)
        
        await event.edit(f"**💥 بـووووم ! انـتهى الـوقت.**\n\n{WAR_IDENTITY}")
    except ValueError:
        await event.edit("**⚠️ يـرجى كـتابة رقـم صحيح بـعد الأمر (مثال: .عد 5)**")

# 4. تحويل النص المكتوب إلى ملف نصي
@client.on(events.NewMessage(outgoing=True, pattern=r"\.لملف (.*)"))
async def text_to_file(event):
    content = event.pattern_match.group(1)
    file_name = "rebel_tech_doc.txt"
    
    await event.edit("**📄 جـاري تـحـويـل الـنـص إلـى مـسـتـند...**")
    
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(content)
        
    await client.send_file(
        event.chat_id, 
        file_name, 
        caption=f"**✅ تـم تـحـويـل الـنـص لـمـلف بـنـجاح.\n\n{WAR_IDENTITY}**"
    )
    os.remove(file_name)
    await event.delete()

# 5. قائمة أوامر الأدوات
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اوامر_الادوات"))
async def tools_help(event):
    help_text = (
        f"**{TOOL_BRAND}**\n"
        "**— — — — — — — — — — —**\n"
        "**🕒 | `.الوقت` :** لـعـرض تـوقـيت الـيمن الـآن.\n"
        "**🔗 | `.رابط` :** لـسـحب رابـط الـمـيديات بـالـرد.\n"
        "**🧨 | `.عد [ثواني]` :** عـد تـنـازلـي لـلـمـسـابقـات.\n"
        "**📄 | `.لملف [النص]` :** تـحـويـل الـكـود/الـنص لـمـلف.\n"
        "**— — — — — — — — — — —**\n"
        f"{WAR_IDENTITY}"
    )
    await event.edit(help_text)
