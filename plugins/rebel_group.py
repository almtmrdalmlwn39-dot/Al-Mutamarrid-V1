import asyncio, random, re, os
from telethon import events, functions, types
from telethon.tl.types import ChatBannedRights
from main import client, CMD_HELP, SUDO_USERS

# --- [ AL-MUTAMARRID GROUP IDENTITY ] ---
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"

# 1. قائمة الأوامر المقسمة (عرض فقط - كما في الصور)
@client.on(events.NewMessage(incoming=True, pattern=r"^(م1|م2|م3|م4|م5|م8|الاوامر)$"))
async def almutamarrid_menus(event):
    cmd = event.pattern_match.group(1)
    
    if cmd == "م1": # أوامر الطرد والمسح (الصورة 1)
        text = "**🗑️ أوامر المسح والطرد (م1):**\n• مسح + عدد | مسح بالرد\n• مسح (المحظورين/المكتومين)\n• طرد البوتات | طرد المحذوفين\n• حظر | كتم | تقييد | فك التقييد"
    elif cmd == "م2": # أوامر الإعدادات والتحميل (الصورة 2)
        text = "**⚙️ أوامر الإعدادات (م2):**\n• اضف رابط | انشاء رابط\n• ضع (الترحيب/القوانين)\n• تعيين الايدي\n• بحث (يوتيوب) | تيك + الرابط | ساوند + الرابط"
    elif cmd == "م3": # أوامر التفعيل والتعطيل (الصورة 3)
        text = "**🛡️ أوامر التفعيل/التعطيل (م3):**\n• تفعيل/تعطيل (الحماية/الايدي/الردود/الانذار)\n• قفل/فتح (الصور/الفيديو/الروابط)"
    elif cmd == "م4": # أوامر العام (الصورة 4)
        text = "**🌍 أوامر العام (م4):**\n• حظر عام | كتم عام\n• قائمة العام | مسح رتب العام\n• اضافة رد عام | تحديث"
    elif cmd == "م5": # أوامر التسلية والزواج (الصورة 5)
        text = "**🎭 أوامر التسلية (م5):**\n• رفع/تنزيل (هطف/كلب/بثر/خروف/بقلبي)\n• طلاق - زواج | زوجي - زوجتي | تتزوجني"
    elif cmd == "م8": # أوامر التحويل والصيغ (الصورة 8)
        text = "**🔄 أوامر التحويل والخدمية (م8):**\n• تحويل (صوت/متحركه/بصمه)\n• ايدت | ميمز | افتارات | هيدرات"
    elif cmd == "الاوامر":
        text = "**📚 قوائم أوامر المتمرد:**\n• م1 | م2 | م3 | م4 | م5 | م8"

    await event.reply(text + f"\n\n{WAR_IDENTITY}")

# 2. رادار الحماية (منع السب، الملغم، التفليش)
@client.on(events.NewMessage(incoming=True))
async def protection_radar(event):
    if event.out or event.sender_id in SUDO_USERS: return
    text = event.raw_text
    # منع التفليش والسب والروابط
    if len(text) > 3000 or re.search(r"(t\.me|http|@|\.com)", text) or any(w in text for w in ["سكس", "نيك", "قحبة"]):
        try:
            await event.delete()
            await client(functions.channels.EditBannedRequest(event.chat_id, event.sender_id, ChatBannedRights(until_date=None, send_messages=True)))
        except: pass

# 3. أمر "ز" (الزواج العشوائي)
@client.on(events.NewMessage(incoming=True, pattern=r"^ز$"))
async def quick_marriage(event):
    users = await client.get_participants(event.chat_id)
    eligible = [u for u in users if not u.bot and u.id != event.sender_id]
    if eligible:
        chosen = random.choice(eligible)
        await event.reply(f"**💍 زوجتك هي:** [{chosen.first_name}](tg://user?id={chosen.id})\n**ألف مبروك من سورس المتمرد!**")

# 4. أمر الأيدي (ا)
@client.on(events.NewMessage(incoming=True, pattern=r"^ا$"))
async def quick_id(event):
    target = (await event.get_reply_message()).sender if event.is_reply else event.sender
    info = f"**🆔 أيدي:** `{target.id}`\n**👤 الاسم:** {target.first_name}\n\n{WAR_IDENTITY}"
    try:
        photo = await client.download_profile_photo(target.id)
        await client.send_file(event.chat_id, photo, caption=info)
        os.remove(photo)
    except: await event.reply(info)
