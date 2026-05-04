import asyncio, os, pytz, re
from datetime import datetime
from telethon import events, functions, types
from telethon.tl.functions.channels import EditBannedRequest, EditTitleRequest, EditDescriptionRequest
from telethon.tl.types import ChatBannedRights

# استدعاء العميل بطريقة تضمن العمل على أغلب السورسات
try:
    from __main__ import client
except:
    try:
        from k_rebel import client # محاولة استدعاء حسب اسم السورس
    except:
        pass

# --- [ الإعدادات الراقية ] ---
YEMEN_TZ = pytz.timezone('Asia/Aden')
approved_users = set() 
BANNED_RIGHTS = ChatBannedRights(until_date=None, view_messages=True, send_messages=True, send_media=True, send_stickers=True, send_gifs=True, send_games=True, send_inline=True, embed_links=True)
CYBER_IDENTITY = "**- نـحنُ حـماةُ الـخصوصيةِ فـي زمنِ الاختراق.. عـقولنا تـبني وأيـدينا تـحمي. 🦅💻🛡️**"

# --- [ 1. أوامر الحماية والسيطرة (outgoing) ] ---
@client.on(events.NewMessage(outgoing=True))
async def mutamarrid_core(event):
    text = event.text
    chat_id = event.chat_id

    # قائمة الأوامر
    if text in [".الاوامر", ".الاوامر"]:
        res = f"**- مـوسوعة أوامـر الـمتمرد الـشاملة 🦅 :**\n**— — — — — — — — — —**\n**🛡️ | الـحماية :** (.سماح | .رفض)\n**🧨 | الـسيطرة :** (.تفليش | .تدمير | .تكرار)\n**⚙️ | الـخدمة :** (.بينج | .ايدي | .فحص)\n**— — — — — — — — — —**\n{CYBER_IDENTITY}"
        await event.edit(res)

    elif text == ".سماح" and event.is_private:
        approved_users.add(chat_id)
        await event.edit("**- تـم الـسماح لـهذا الـمستخدم ✅**")

    elif text == ".رفض" and event.is_private:
        if chat_id in approved_users: approved_users.remove(chat_id)
        await event.edit("**- تـم تـفعيل الـحماية ضـده 🚫**")

    elif text in [".تفليش", ".تدمير"]:
        await event.edit("**- جـاري الـتطهير الـشامل.. 🧨**")
        count = 0
        async for u in client.iter_participants(chat_id):
            if u.is_self or u.admin_rights: continue
            try:
                await client(EditBannedRequest(chat_id, u.id, BANNED_RIGHTS))
                count += 1
            except: continue
        await event.respond(f"**- تـم سـحق {count} عـنصر بـنجاح ✅\n{CYBER_IDENTITY}**")

    elif text == ".بينج":
        start = datetime.now()
        await event.edit("**- جـاري الـفحص...**")
        ms = (datetime.now() - start).microseconds / 1000
        await event.edit(f"**- سـرعة الـمعالجة : `{ms}`ms ⚡**")

# --- [ 2. ترحيب الخاص بالوقت والصورة (incoming) ] ---
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def welcome_handler(event):
    if event.sender_id in approved_users or (await event.get_sender()).bot: return
    if event.sender_id == (await client.get_me()).id: return
    
    time_now = datetime.now(YEMEN_TZ).strftime("%I:%M %p")
    msg = f"**- مـرحباً بـك فـي سـيرفر الـمتمرد 🦅\n- تـوقيت الـيمن: {time_now}**\n\n{CYBER_IDENTITY}"
    try:
        me = await client.get_me()
        await client.send_file(event.chat_id, me.id, caption=msg)
    except:
        await event.reply(msg)
