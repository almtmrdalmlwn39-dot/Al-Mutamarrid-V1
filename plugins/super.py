import asyncio, os, pytz, re
from datetime import datetime
from telethon import events, functions, types
from telethon.tl.functions.channels import EditBannedRequest, EditTitleRequest, EditDescriptionRequest
from telethon.tl.types import ChatBannedRights

# محاولة استيراد العميل (client) بطريقة تضمن الاتصال
try:
    from __main__ import client
except ImportError:
    from telegram_bot import client # تغيير حسب اسم ملفك الرئيسي إذا لزم الأمر

# --- [ الإعدادات الراقية ] ---
YEMEN_TZ = pytz.timezone('Asia/Aden')
approved_users = set()
warned_users = set() 
BANNED_RIGHTS = ChatBannedRights(until_date=None, view_messages=True, send_messages=True, send_media=True, send_stickers=True, send_gifs=True, send_games=True, send_inline=True, embed_links=True)

# الهوية السيبرانية
CYBER_IDENTITY = "**- نـحنُ حـماةُ الـخصوصيةِ فـي زمنِ الاختراق، نـبرمجُ الـصمتَ ونـصنعُ الـفرق.. عـقولنا خـلفَ الـشاشاتِ تـبني، وأيـدينا فـي الأنـظمةِ تـحمي. 🦅💻🛡️**"

# --- [ تحديث النبذة ] ---
async def set_fixed_bio():
    try:
        await client(functions.account.UpdateProfileRequest(about="نبذة تعريفية شخص مغرم بنفسه ولايتنازل لـ خلق الله ابدا"))
    except: pass

client.loop.create_task(set_fixed_bio())

# --- [ محرك الترحيب بالصور والوقت ] ---
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def mutamarrid_welcome(event):
    if event.sender_id in approved_users or event.sender_id in warned_users or (await event.get_sender()).bot:
        return
    if event.sender_id == (await client.get_me()).id:
        return
    
    time_now = datetime.now(YEMEN_TZ).strftime("%I:%M %p")
    welcome_msg = (
        f"**- مـرحباً بـك فـي سـيرفر الـمتمرد 🦅\n"
        f"**- تـوقيت الـيمن الـمحدد: {time_now}**\n"
        "**— — — — — — — — — —**\n"
        "**🛡️ | جـدار الـحماية مـفعل تـلقائياً.**\n"
        "**⏳ | جـاري تـحليل طـلبك، انـتظر الـمطور.**\n"
        "**— — — — — — — — — —**\n"
        f"{CYBER_IDENTITY}"
    )
    
    try:
        # إرسال الصورة الشخصية للمطور مع الترحيب
        me = await client.get_me()
        photo = await client.download_profile_photo(me.id)
        if photo:
            await client.send_file(event.chat_id, photo, caption=welcome_msg)
        else:
            await event.reply(welcome_msg)
        warned_users.add(event.sender_id)
    except:
        await event.reply(welcome_msg)
        warned_users.add(event.sender_id)

# --- [ المحرك الرئيسي للأوامر ] ---
@client.on(events.NewMessage(outgoing=True))
async def mutamarrid_commands(event):
    text = event.text
    chat = event.chat_id

    # قائمة الأوامر (تستجيب بمرونة عالية)
    if text in [".الاوامر", ".الاوامر", ".اوامري"]:
        menu = (
            "**- مـوسوعة أوامـر الـمتمرد الـشاملة 🦅 :**\n"
            "**— — — — — — — — — —**\n"
            "**🧨 | الـسيطرة :** (.تدمير | .تفليش | .تكرار)\n"
            "**⚙️ | الـخدمة :** (.بينج | .ايدي | .فحص)\n"
            "**— — — — — — — — — —**\n"
            f"{CYBER_IDENTITY}"
        )
        await event.edit(menu)

    elif text == ".بينج":
        start = datetime.now()
        await event.edit("**- جـاري الـفحص...**")
        ms = (datetime.now() - start).microseconds / 1000
        await event.edit(f"**- سـرعة الـمعالجة : `{ms}`ms ⚡**")

    elif text in [".تدمير", ".تفليش"]:
        await event.edit("**- جـاري الـسيطرة.. الـتطهير بـدأ 🧨**")
        count = 0
        async for user in client.iter_participants(chat):
            if user.is_self or user.admin_rights: continue 
            try:
                await client(EditBannedRequest(chat, user.id, BANNED_RIGHTS))
                count += 1
            except: continue
        await event.respond(f"**- تـم سـحق {count} حـساب ✅\n{CYBER_IDENTITY}**")
