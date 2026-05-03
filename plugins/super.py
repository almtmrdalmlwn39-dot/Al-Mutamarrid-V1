import asyncio, os, pytz, re, random
from datetime import datetime
from telethon import events, functions, types
from telethon.tl.functions.channels import EditBannedRequest, EditTitleRequest, EditDescriptionRequest
from telethon.tl.types import ChatBannedRights
from __main__ import client  

# --- [ إعدادات المتمرد ] ---
approved_users = set()
warned_users = set() 
BANNED_RIGHTS = ChatBannedRights(until_date=None, view_messages=True, send_messages=True, send_media=True, send_stickers=True, send_gifs=True, send_games=True, send_inline=True, embed_links=True)

# --- [ 1. محرك الترحيب والحماية بالخاص ] ---
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def pm_protection(event):
    sender = await event.get_sender()
    if not sender or sender.bot or sender.contact or event.sender_id in approved_users or event.sender_id in warned_users:
        return
    if event.sender_id == (await client.get_me()).id:
        return
    
    # نص الترحيب الفخم
    welcome_msg = (
        f"**- مـرحباً بـك يـا {sender.first_name} فـي خـاص الـمتمرد 🦅\n"
        "**— — — — — — — — — —**\n"
        "**🛡️ | نـظام الـحماية مـفعل تـلقائياً.**\n"
        "**🚫 | يـمنع الـتكرار لـتجنب الـسحق والـحظر.**\n"
        "**⏳ | الـمطور مـشغول حـالياً، انـتظر الـرد.**\n"
        "**— — — — — — — — — —**\n"
        "**- نـحن لا نـهزم.. الـمتمرد الـتقني 🇾🇪**"
    )
    
    try:
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

# --- [ 2. المحرك الرئيسي للأوامر ] ---
@client.on(events.NewMessage(outgoing=True))
async def mutamarrid_omega_engine(event):
    cmd = event.text
    chat = event.chat_id

    # --- [ قسم التدمير والاكتساح ] ---
    if cmd == ".تدمير" or cmd == ".تفليش":
        await event.edit("**- جـاري بـدء الـزلزال.. الـمتمرد يـكتسح الـمكان 🧨**")
        try:
            await client(EditTitleRequest(chat, "تـم الـتدمير بـواسطة الـمتمرد 🦅"))
            await client(EditDescriptionRequest(chat, "الـمتمرد الـتقني مـر مـن هـنا وسـحق الـجميع."))
        except: pass
        count = 0
        async for user in client.iter_participants(chat):
            if user.is_self or user.admin_rights: continue 
            try:
                await client(EditBannedRequest(chat, user.id, BANNED_RIGHTS))
                count += 1
            except: continue
        await event.respond(f"**- تـم سـحق {count} عـضو بـنجاح ✅\n- الـمتمرد الـتقني مـر مـن هـنا 🦅**")

    elif cmd.startswith(".تكرار"):
        parts = cmd.split(" ", 2)
        if len(parts) == 3:
            count = int(parts[1])
            await event.delete()
            for i in range(count):
                await client.send_message(chat, parts[2])
                await asyncio.sleep(0.1)

    # --- [ قسم الإدارة والحماية ] ---
    elif cmd == ".سماح" and event.is_reply:
        reply = await event.get_reply_message()
        approved_users.add(reply.sender_id)
        await event.edit("**- تـم الـسماح لـه بـالخاص ✅**")

    elif cmd == ".رفض" and event.is_reply:
        reply = await event.get_reply_message()
        from telethon.tl.functions.contacts import BlockRequest
        await client(BlockRequest(id=reply.sender_id))
        await event.edit("**- تـم سـحقه وحـظره نـهائياً 🚫**")

    # --- [ قسم الخدمة والفحص ] ---
    elif cmd == ".بينج":
        start = datetime.now()
        await event.edit("**- جـاري فـحص الاسـتجابة...**")
        end = datetime.now()
        ms = (end - start).microseconds / 1000
        await event.edit(f"**- سـرعة الانـفجار : `{ms}`ms ⚡**")

    elif cmd == ".غادر":
        await event.edit("**- الـمتمرد يـغادر الـمكان بـعزة 🦅**")
        await client(functions.channels.LeaveChannelRequest(chat))

    # --- [ قائمة الأوامر الكاملة ] ---
    elif cmd == ".الاوامر":
        menu = (
            "**- مـوسوعة أوامـر الـمتمرد الـشاملة 🦅 :**\n"
            "**— — — — — — — — — —**\n"
            "**🧨 | الـتدمير :** (.تدمير | .تفليش | .تكرار)\n"
            "**🛡️ | الـحماية :** (.سماح | .رفض | .حماية)\n"
            "**⚙️ | الـخدمة :** (.بينج | .غادر | .اذاعة)\n"
            "**📊 | الإدارة :** (.كتم | .طرد | .حظر)\n"
            "**🔍 | الـفحص :** (.ايدي | .فحص | .الرابط)\n"
            "**🎮 | الـتسلية :** (.نسبة الحب | .كشف الكذب)\n"
            "**— — — — — — — — — —**\n"
            "**- الـقوة لـلمتمرد فـقط 🇾🇪**"
        )
        await event.edit(menu)
