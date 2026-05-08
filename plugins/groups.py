from main import client, CMD_HELP, SUDO_USERS
from telethon import events, functions, types
import os, asyncio, re, random

# --- [ AL-MUTAMARRID ULTIMATE SOURCE ] ---
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"

# 🗂️ القوائم المقسمة (كما في الصور 1-6)
HELP_TEXTS = {
    "م1": "🛡️ **أوامر الرفع والتنزيل:**\n(رفع - تنزيل) [مالك، مدير، مشرف، مميز]\n• مسح [الكل، المحظورين، المكتومين]\n• مسح + عدد (لتنظيف الشات)",
    "م2": "⚙️ **أوامر الإعدادات:**\n• الرابط، المالكين، الحمايه\n• تفعيل/تعطيل (الايدي، الزواج، الحماية)",
    "م3": "🚫 **أوامر القفل والفتح:**\n• قفل/فتح (الروابط، الصور، الفيديو، السب، التكرار، الدخول، الملغم، التعديل)",
    "م4": "👨‍💻 **أوامر المطور:**\n• حظر عام، كتم عام، إذاعة، تحديث",
    "م5": "🎭 **أوامر التسلية:**\n• (رفع - تنزيل) [هطف، كلب، حمار، بثر، خروف]\n• ز (للزواج العشوائي)",
    "م6": "🛠️ **أوامر الخدمية:**\n• نسبة الحب، تتزوجني، زخرف + اسمك، ايدي (ا)"
}

# 🛠️ دالة التحقق من الصلاحيات
async def is_boss(event):
    if event.out or event.sender_id in SUDO_USERS: return True
    try:
        p = await client.get_permissions(event.chat_id, event.sender_id)
        return p.is_creator or p.is_admin
    except: return False

# --- [ عرض القوائم المقسمة ] ---
@client.on(events.NewMessage(incoming=True, pattern=r"^(الاوامر|م1|م2|م3|م4|م5|م6)$"))
async def show_menus(event):
    cmd = event.raw_text
    if cmd == "الاوامر":
        text = "**أهلاً بك في أوامر سورس المتمرد 🛡️**\n\n• م1 - الإدارة\n• م2 - الإعدادات\n• م3 - القفل والفتح\n• م4 - المطور\n• م5 - التسلية\n• م6 - الخدمية"
        await event.reply(text + f"\n\n{WAR_IDENTITY}")
    elif cmd in HELP_TEXTS:
        await event.reply(HELP_TEXTS[cmd] + f"\n\n{WAR_IDENTITY}")

# --- [ محرك الحماية والمنع (قفل الروابط، الملغم، السب) ] ---
@client.on(events.NewMessage(incoming=True))
async def guard_radar(event):
    if await is_boss(event): return
    text = event.raw_text
    # حماية من الروابط، التفليش، والسب
    if re.search(r"(t\.me|http|@|\.com)", text) or len(text) > 3000 or any(w in text for w in ["سكس", "نيك"]):
        try:
            await event.delete()
            await client(functions.channels.EditBannedRequest(event.chat_id, event.sender_id, types.ChatBannedRights(until_date=None, send_messages=True)))
        except: pass

# --- [ باقي الأوامر (ايدي، ز، رفع/تنزيل) ] ---
@client.on(events.NewMessage(incoming=True, pattern=r"^(ا|ايدي|ز)$"))
async def fun_commands(event):
    cmd = event.raw_text
    if cmd in ["ا", "ايدي"]:
        # (كود الأيدي مع الصورة كما في السابق)
        target = (await event.get_reply_message()).sender if event.is_reply else event.sender
        await event.reply(f"**👤 الاسم:** {target.first_name}\n**🆔 الأيدي:** `{target.id}`")
    elif cmd == "ز":
        users = await client.get_participants(event.chat_id)
        eligible = [u for u in users if not u.bot and u.id != event.sender_id]
        if eligible:
            chosen = random.choice(eligible)
            await event.reply(f"**💍 زوجتك هي:** [{chosen.first_name}](tg://user?id={chosen.id})")
