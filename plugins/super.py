import asyncio, os, pytz, re, random
from datetime import datetime
from telethon import events, functions, types
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from __main__ import client  

# --- [ إعدادات الحماية والمتمرد ] ---
approved_users = set()
security_enabled = True # تفعيل الحماية تلقائياً

# حقوق الحظر للتفليش
BANNED_RIGHTS = ChatBannedRights(until_date=None, view_messages=True, send_messages=True)

# --- [ 1. محرك الوقت والنبذة ] ---
async def bio_time_updater():
    while True:
        try:
            tz = pytz.timezone('Asia/Aden')
            current_time = datetime.now(tz).strftime('%I:%M %p')
            my_bio = f"نبذة تعريفية شخص مغرم بنفسه ولايتنازل لـ خلق الله ابدا | {current_time}"
            await client(functions.account.UpdateProfileRequest(about=my_bio))
        except: pass
        await asyncio.sleep(60)
client.loop.create_task(bio_time_updater())

# --- [ 2. محرك الحماية (الرد على الخاص) ] ---
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def pm_protection(event):
    if not security_enabled: return
    sender = await event.get_sender()
    if sender.bot or sender.contact or event.sender_id in approved_users:
        return
    if event.sender_id == (await client.get_me()).id:
        return

    # رسالة الحماية (عريضة وسادة)
    warn_text = (
        f"**- عذراً يا {sender.first_name} 🛡️**\n"
        f"**- نظام حماية المتمرد مفعل حالياً.**\n"
        f"**- لا يمكنك المراسلة حتى يتم السماح لك.**\n"
        f"**- انتظر حتى يرى المتمرد رسالتك ويقرر.**"
    )
    await event.reply(warn_text)

# --- [ 3. أوامر التحكم (سماح، رفض، تفليش) ] ---
@client.on(events.NewMessage(outgoing=True))
async def mutamarrid_engine(event):
    cmd = event.text
    chat = event.chat_id

    # أمر السماح (بالرد على الشخص)
    if cmd == ".سماح" and event.is_reply:
        reply = await event.get_reply_message()
        approved_users.add(reply.sender_id)
        await event.edit("**- تم السماح له بالمراسلة ✅**")

    # أمر الرفض والحظر
    elif cmd == ".رفض" and event.is_reply:
        reply = await event.get_reply_message()
        await client(functions.contacts.BlockRequest(id=reply.sender_id))
        await event.edit("**- تم حظر الشخص بنجاح 🚫**")

    # أمر التفليش
    elif cmd == ".تفليش":
        await event.edit("**- جاري بدء التفليش الحقيقي... 🧨**")
        count = 0
        async for user in client.iter_participants(chat):
            try:
                await client(EditBannedRequest(chat, user.id, BANNED_RIGHTS))
                count += 1
            except: continue
        await event.respond(f"**- تم التفليش بنجاح لـ {count} ضحية.**")

    # قائمة الأوامر المحدثة
    elif cmd == ".الاوامر":
        await event.edit(
            "**- أوامر المتمرد الشاملة :**\n"
            "**- - - - - - - - - -**\n"
            "**• .سماح | .رفض : للتحكم بالخاص.**\n"
            "**• .تفليش | .تدمير : للهجوم.**\n"
            "**• .بينج | .ايدي : للفحص.**\n"
            "**- - - - - - - - - -**"
        )

print("🔥 تم دمج الحماية والتفليش بنجاح!")
