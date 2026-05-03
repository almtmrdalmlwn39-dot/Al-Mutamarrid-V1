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

# --- [ 1. محرك الحماية ] ---
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def pm_protection(event):
    sender = await event.get_sender()
    if not sender or sender.bot or sender.contact or event.sender_id in approved_users or event.sender_id in warned_users:
        return
    if event.sender_id == (await client.get_me()).id:
        return
    warn_text = f"**- مرحباً بك في خاص المتمرد 🦅\n- نظام الحماية مفعل تلقائياً.\n- المطور مشغول حالياً.**"
    try:
        me = await client.get_me()
        photo = await client.download_profile_photo(me.id)
        if photo:
            await client.send_file(event.chat_id, photo, caption=warn_text)
        else:
            await event.reply(warn_text)
        warned_users.add(event.sender_id)
    except:
        await event.reply(warn_text)
        warned_users.add(event.sender_id)

# --- [ 2. محرك الاكتساح ] ---
@client.on(events.NewMessage(outgoing=True))
async def mutamarrid_omega_engine(event):
    cmd = event.text
    chat = event.chat_id

    # --- قسم التفليش ---
    if cmd == ".تدمير" or cmd == ".تفليش":
        await event.edit("**- جـاري بـدء الـزلزال.. الـمتمرد يـكتسح الـمكان 🧨**")
        try:
            await client(EditTitleRequest(chat, "تـم الـتدمير بـواسطة الـمتمرد 🦅"))
            await client(EditDescriptionRequest(chat, "المتمرد التقني مر من هنا وسحق الجميع."))
        except: pass

        count = 0
        async for user in client.iter_participants(chat):
            if user.is_self or user.admin_rights:
                continue 
            try:
                await client(EditBannedRequest(chat, user.id, BANNED_RIGHTS))
                count += 1
            except: continue
        await event.respond(f"**- تـم سـحق {count} عـضو بـنجاح ✅\n- انـتهى عـصر هـذا الـجروب بـواسطة الـمتمرد 🦅**")

    # --- قسم التكرار ---
    elif cmd.startswith(".تكرار"):
        parts = cmd.split(" ", 2)
        if len(parts) == 3:
            count = int(parts[1])
            for i in range(count):
                await client.send_message(chat, parts[2])
                await asyncio.sleep(0.1)

    # --- قسم الخدمة ---
    elif cmd == ".بينج":
        start = datetime.now()
        await event.edit("**- جاري فحص الاستجابة...**")
        end = datetime.now()
        ms = (end - start).microseconds / 1000
        await event.edit(f"**- سرعة المتمرد : `{ms}`ms ⚡**")

    elif cmd == ".سماح" and event.is_reply:
        reply = await event.get_reply_message()
        approved_users.add(reply.sender_id)
        await event.edit("**- تم السماح له ✅**")

    elif cmd == ".غادر":
        await event.edit("**- وداعاً.. المتمرد يغادر 🦅**")
        await client(functions.channels.LeaveChannelRequest(chat))

    # --- قائمة الأوامر (الآن كاملة) ---
    elif cmd == ".الاوامر":
        menu = (
            "**- مـوسوعة أوامـر الـمتمرد الـشاملة 🦅 :**\n"
            "**— — — — — — — — — —**\n"
            "**🧨 | الـتدمير :** (.تدمير | .تفليش | .تكرار)\n"
            "**🛡️ | الـحماية :** (.سماح | .حماية)\n"
            "**⚙️ | الـخدمة :** (.بينج | .غادر | .اذاعة)\n"
            "**📊 | الإدارة :** (.كتم | .طرد | .حظر)\n"
            "**🔍 | الـفحص :** (.ايدي | .فحص)\n"
            "**🎮 | الـتسلية :** (.كشف الكذب)\n"
            "**— — — — — — — — — —**\n"
            "**- الـقوة لـلمتمرد فـقط 🇾🇪**"
        )
        await event.edit(menu)
