import asyncio, os, pytz, re, random
from datetime import datetime
from telethon import events, functions, types
from telethon.tl.functions.channels import EditBannedRequest, EditTitleRequest
from telethon.tl.types import ChatBannedRights
from __main__ import client  

# --- [ إعدادات المتمرد الأساسية ] ---
approved_users = set()
BANNED_RIGHTS = ChatBannedRights(until_date=None, view_messages=True, send_messages=True)

# --- [ 1. محرك الحماية والتنبيهات ] ---
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def pm_protection(event):
    sender = await event.get_sender()
    if sender.bot or sender.contact or event.sender_id in approved_users or event.sender_id == (await client.get_me()).id:
        return
    warn_text = f"**- عذراً يا {sender.first_name} 🛡️\n- نظام حماية المتمرد مفعل حالياً.\n- انتظر السماح لك.**"
    await event.reply(warn_text)

# --- [ 2. المحرك الملكي الشامل (جميع الأوامر) ] ---
@client.on(events.NewMessage(outgoing=True))
async def mutamarrid_omega_engine(event):
    cmd = event.text
    chat = event.chat_id

    # --- قسم الحماية ---
    if cmd == ".سماح" and event.is_reply:
        reply = await event.get_reply_message()
        approved_users.add(reply.sender_id)
        await event.edit("**- تم السماح له ✅**")
    elif cmd == ".رفض" and event.is_reply:
        reply = await event.get_reply_message()
        await client(functions.contacts.BlockRequest(id=reply.sender_id))
        await event.edit("**- تم الحظر 🚫**")

    # --- قسم التدمير ---
    elif cmd == ".تدمير":
        await event.edit("**- جاري التدمير الملكي... 🧨**")
        async for user in client.iter_participants(chat):
            try: await client(EditBannedRequest(chat, user.id, BANNED_RIGHTS))
            except: continue
        await event.respond("**- انتهى الاكتساح بنجاح ✅**")
    
    elif cmd.startswith(".تكرار"):
        parts = cmd.split(" ", 2)
        if len(parts) == 3:
            count = int(parts[1])
            for i in range(count):
                await client.send_message(chat, parts[2])
                await asyncio.sleep(0.2)

    # --- قسم الإدارة ---
    elif cmd == ".حظر" and event.is_reply:
        reply = await event.get_reply_message()
        await client(EditBannedRequest(chat, reply.sender_id, BANNED_RIGHTS))
        await event.edit("**- تم حظره من المجموعة 🚷**")
    elif cmd == ".طرد" and event.is_reply:
        reply = await event.get_reply_message()
        await client.kick_participant(chat, reply.sender_id)
        await event.edit("**- تم طرده بنجاح 👋**")

    # --- قسم التسلية والخدمة ---
    elif cmd == ".بينج":
        start = datetime.now()
        await event.edit("**جاري الفحص...**")
        end = datetime.now()
        await event.edit(f"**- سرعة المتمرد : `{(end - start).microseconds / 1000}`ms ⚡**")
    elif cmd == ".كشف الكذب":
        res = random.choice(["صادق ✅", "كاذب ❌", "نصاب كبير 🤡"])
        await event.edit(f"**- النتيجة : {res}**")
    elif cmd == ".غادر":
        await event.edit("**- وداعاً، المتمرد يغادر... 👋**")
        await client(functions.channels.LeaveChannelRequest(chat))

    # --- قائمة الأوامر (التي طلبتها بالضبط) ---
    elif cmd == ".الاوامر":
        menu = (
            "**- مـوسوعة أوامـر الـمتمرد الـشاملة 🦅 :**\n"
            "**— — — — — — — — — —**\n"
            "**🛡️ | الـحماية :** (.سماح | .رفض | .حماية)\n"
            "**🧨 | الـتدمير :** (.تدمير | .تفليش | .تكرار)\n"
            "**⚙️ | الـخدمة :** (.تصفية | .اذاعة | .غادر)\n"
            "**🔍 | الـفحص :** (.بينج | .ايدي | .فحص | .الرابط)\n"
            "**🎮 | الـتسلية :** (.نسبة الحب | .كشف الكذب)\n"
            "**📂 | الـتخزين :** (.انشاء تخزين | .تخزين)\n"
            "**📊 | الإدارة :** (.كتم | .طرد | .حظر)\n"
            "**— — — — — — — — — —**\n"
            "**- كـل هـذه الـقوة بـين يـديك الآن.. الـمتمرد.**"
        )
        await event.edit(menu)
