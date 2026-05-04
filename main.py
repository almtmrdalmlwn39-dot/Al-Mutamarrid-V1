import asyncio, os, pytz, re, random
from datetime import datetime
from telethon import events, functions, types
# تصحيح الاستيرادات لضمان عمل النبذة والأوامر
from telethon.tl.functions.messages import EditChatAboutRequest
from telethon.tl.functions.channels import EditBannedRequest, EditTitleRequest
from telethon.tl.types import ChatBannedRights
from __main__ import client  

# --- [ إعدادات الهوية والوقت ] ---
YEMEN_TZ = pytz.timezone('Asia/Aden')
approved_users = set() 
warned_users = set() 
BANNED_RIGHTS = ChatBannedRights(until_date=None, view_messages=True, send_messages=True, send_media=True, send_stickers=True, send_gifs=True, send_games=True, send_inline=True, embed_links=True)

CYBER_IDENTITY = "**- نـحنُ حـماةُ الـخصوصيةِ فـي زمنِ الاختراق 🦅💻🛡️**"

# --- [ تثبيت النبذة الشخصية ] ---
async def set_my_bio():
    try:
        # النبذة التي طلبتها ثابتة وقوية
        fixed_bio = "نبذة تعريفية شخص مغرم بنفسه ولايتنازل لـ خلق الله ابدا"
        await client(functions.account.UpdateProfileRequest(about=fixed_bio))
    except: pass

client.loop.create_task(set_my_bio())

# --- [ 1. محرك الترحيب والرد الآلي بصورتك ] ---
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def pm_welcome(event):
    if event.is_bot: return
    sender = await event.get_sender()
    if not sender or event.sender_id in approved_users or event.sender_id in warned_users:
        return
    me = await client.get_me()
    if event.sender_id == me.id: return 
    
    time_now = datetime.now(YEMEN_TZ).strftime("%I:%M %p")
    welcome_msg = (
        f"**- مـرحباً بـك يـا {sender.first_name} فـي سـيرفر الـمتمرد 🦅\n"
        f"**- تـوقيت الـيمن الآن: {time_now}**\n"
        "**— — — — — — — — — —**\n"
        "**🛡️ | جـدار الـحماية مـفعل تـلقائياً.**\n"
        "**⏳ | جـاري تـحليل طـلبك، انـتظر الـمطور.**\n"
        f"{CYBER_IDENTITY}"
    )
    
    try:
        # سحب صورتك الشخصية وإرسالها ترحيباً
        photo = await client.download_profile_photo(me.id)
        if photo:
            await client.send_file(event.chat_id, photo, caption=welcome_msg)
        else:
            await event.reply(welcome_msg)
        warned_users.add(event.sender_id)
    except: pass

# --- [ 2. المحرك الرئيسي للأوامر ] ---
@client.on(events.NewMessage(outgoing=True))
async def mutamarrid_engine(event):
    cmd = event.text
    chat = event.chat_id

    # --- [ أوامر الخاص ] ---
    if cmd == ".سماح":
        if event.is_private:
            approved_users.add(event.chat_id)
            await event.edit("**✅ تـم الـسماح لـهذا الـمستخدم بـتخطي الـرد الـآلي.**")
    
    elif cmd == ".رفض":
        if event.is_private:
            if event.chat_id in approved_users: approved_users.remove(event.chat_id)
            await event.edit("**❌ تـم إلـغاء الـسماح، سـيعود الـرد الـآلي لـلعمل.**")

    elif cmd == ".حظر_خاص":
        if event.is_private:
            await event.edit("**🚫 جـاري حـظر الـمستخدم مـن الـقاعدة..**")
            await client(functions.contacts.BlockRequest(id=event.chat_id))
            await event.edit("**✅ تـم الـحظر بـنجاح، وداعـاً.**")

    # --- [ أوامر السيطرة والخدمة ] ---
    elif cmd in [".تدمير", ".تفليش"]:
        await event.edit("**- جـاري الـتطهير.. الـتدمير بـدأ 🧨**")
        async for user in client.iter_participants(chat):
            if user.is_self or user.admin_rights: continue 
            try: await client(EditBannedRequest(chat, user.id, BANNED_RIGHTS))
            except: continue
        await event.respond(f"**- تـم سـحق الـجروب بـواسطة الـمتمرد ✅**\n{CYBER_IDENTITY}")

    elif cmd == ".بينج":
        start = datetime.now()
        await event.edit("**- جـاري فـحص بـرودة الـسيرفر...**")
        ms = (datetime.now() - start).microseconds / 1000
        await event.edit(f"**- الـسرعة : `{ms}`ms ⚡**")

    elif cmd == ".ايدي":
        me = await client.get_me()
        await event.edit(f"**- أيـدي الـدردشة: `{chat}`\n- أيـديك يـا مـتمرد: `{me.id}`**")

    elif cmd in [".الاوامر", ".اوامر"]:
        await event.edit(
            f"**- أوامـر الـمتمرد الـشاملة 🦅:**\n"
            "**— — — — — — — — — —**\n"
            "**🛡️ | الـخاص :** (.سماح | .رفض | .حظر_خاص)\n"
            "**🧨 | الـسيطرة :** (.تفليش | .تدمير)\n"
            "**⚙️ | الـخدمة :** (.بينج | .ايدي)\n"
            "**— — — — — — — — — —**\n"
            f"{CYBER_IDENTITY}"
        )
