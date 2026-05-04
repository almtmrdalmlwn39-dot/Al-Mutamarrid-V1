import asyncio, os, pytz, re, random
from datetime import datetime
from telethon import events, functions, types
from telethon.tl.functions.channels import EditBannedRequest, EditTitleRequest, EditDescriptionRequest
from telethon.tl.types import ChatBannedRights
from __main__ import client  

# --- [ إعدادات الهوية والوقت ] ---
YEMEN_TZ = pytz.timezone('Asia/Aden')
approved_users = set()
warned_users = set() 
BANNED_RIGHTS = ChatBannedRights(until_date=None, view_messages=True, send_messages=True, send_media=True, send_stickers=True, send_gifs=True, send_games=True, send_inline=True, embed_links=True)

# الهوية السيبرانية
CYBER_IDENTITY = "**- نـحنُ حـماةُ الـخصوصيةِ فـي زمنِ الاختراق، نـبرمجُ الـصمتَ ونـصنعُ الـفرق.. عـقولنا خـلفَ الـشاشاتِ تـبني، وأيـدينا فـي الأنـظمةِ تـحمي. 🦅💻🛡️**"

# --- [ تثبيت النبذة الشخصية القوية ] ---
async def set_fixed_bio():
    try:
        my_bio = "نبذة تعريفية شخص مغرم بنفسه ولايتنازل لـ خلق الله ابدا"
        await client(functions.account.UpdateProfileRequest(about=my_bio))
    except: pass

client.loop.create_task(set_fixed_bio())

# --- [ 1. محرك الترحيب السيبراني بصورتك ] ---
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def pm_protection(event):
    if event.is_bot: return
    sender = await event.get_sender()
    if not sender or event.sender_id in approved_users or event.sender_id in warned_users:
        return
    me = await client.get_me()
    if event.sender_id == me.id: return
    
    time_now = datetime.now(YEMEN_TZ).strftime("%I:%M %p")
    welcome_msg = (
        f"**- مـرحباً بـك يـا {sender.first_name} فـي سـيرفر الـمتمرد 🦅\n"
        f"**- تـوقيت الـيمن الـمحدد: {time_now}**\n"
        "**— — — — — — — — — —**\n"
        "**🛡️ | جـدار الـحماية مـفعل تـلقائياً.**\n"
        "**🚫 | تـجنب الـتكرار لـضمان عـدم تـصنيفك كـهجوم.**\n"
        "**⏳ | جـاري تـحليل طـلبك، انـتظر الـمطور.**\n"
        "**— — — — — — — — — —**\n"
        f"{CYBER_IDENTITY}"
    )
    
    try:
        photo = await client.download_profile_photo(me.id)
        if photo:
            await client.send_file(event.chat_id, photo, caption=welcome_msg)
        else:
            await event.reply(welcome_msg)
        warned_users.add(event.sender_id)
    except: pass

# --- [ 2. المحرك الرئيسي للأوامر القوية ] ---
@client.on(events.NewMessage(outgoing=True))
async def mutamarrid_omega_engine(event):
    cmd = event.text
    chat = event.chat_id

    # أوامر الحماية والخاص
    if cmd == ".سماح":
        if event.is_private:
            approved_users.add(event.chat_id)
            await event.edit("**✅ تـم الـسماح لـهذا الـمستخدم بـالتحدث.**")
    
    elif cmd == ".رفض":
        if event.is_private:
            if event.chat_id in approved_users: approved_users.remove(event.chat_id)
            await event.edit("**❌ تـم إلـغاء الـسماح، سـيتم تـفعيل الـرد الـآلي.**")

    elif cmd == ".حظر_خاص":
        if event.is_private:
            await event.edit("**🚫 جـاري حـظر الـمستخدم مـن الـخاص..**")
            await client(functions.contacts.BlockRequest(id=event.chat_id))
            await event.edit("**✅ تـم الـحظر بنجاح، وداعاً.**")

    # أوامر التدمير والاكتساح (التفليش)
    elif cmd in [".تدمير", ".تفليش"]:
        await event.edit("**- جـاري تـحديث قـواعد الـبيانات.. الـتطهير بـدأ 🧨**")
        try:
            await client(EditTitleRequest(chat, "تـم الاخـتراق بـواسطة الـمتمرد 🦅"))
        except: pass
        count = 0
        async for user in client.iter_participants(chat):
            if user.is_self or user.admin_rights: continue 
            try:
                await client(EditBannedRequest(chat, user.id, BANNED_RIGHTS))
                count += 1
            except: continue
        await event.respond(f"**- تـم سـحق {count} عـنصر بـنجاح ✅\n{CYBER_IDENTITY}**")

    # أمر التكرار
    elif cmd.startswith(".تكرار"):
        parts = cmd.split(" ", 2)
        if len(parts) == 3:
            count = int(parts[1])
            await event.delete()
            for _ in range(count):
                await client.send_message(chat, parts[2])
                await asyncio.sleep(0.1)

    # أوامر الخدمة
    elif cmd == ".ايدي":
        await event.edit(f"**- مـعرف الـقاعدة: `{chat}`\n- مـعرف الـمطور: `{(await client.get_me()).id}`**")

    elif cmd == ".بينج":
        start = datetime.now()
        await event.edit("**- جـاري فـحص بـرودة الـسيرفر...**")
        ms = (datetime.now() - start).microseconds / 1000
        await event.edit(f"**- سـرعة الـمعالجة : `{ms}`ms ⚡**")

    # قائمة الأوامر الشاملة
    elif cmd in [".الاوامر", ".اوامر"]:
        menu = (
            "**- مـوسوعة أوامـر الـمتمرد الـشاملة 🦅 :**\n"
            "**— — — — — — — — — —**\n"
            "**🛡️ | الـخاص :** (.سماح | .رفض | .حظر_خاص)\n"
            "**🧨 | الـسيطرة :** (.تدمير | .تفليش | .تكرار)\n"
            "**⚙️ | الـخدمة :** (.بينج | .ايدي | .فحص)\n"
            "**— — — — — — — — — —**\n"
            f"{CYBER_IDENTITY}"
        )
        await event.edit(menu)
