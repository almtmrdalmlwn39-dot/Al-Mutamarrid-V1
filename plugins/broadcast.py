from telethon import events
from config import SUDO_USERS
from __main__ import client

@client.on(events.NewMessage(pattern=r'\.اذاعة للخاص', outgoing=True))
async def bc_private(event):
    if event.sender_id not in SUDO_USERS: return
    msg = await event.get_reply_message()
    if not msg: return await event.edit("**⚠️ رد على الرسالة التي تريد إذاعتها أولاً!**")
    
    await event.edit("**🚀 جاري الإذاعة للمحادثات الخاصة...**")
    count = 0
    async for dialog in client.iter_dialogs():
        if dialog.is_user and not dialog.entity.bot:
            try:
                await client.send_message(dialog.id, msg)
                count += 1
            except: pass
    await event.edit(f"**✅ تمت الإذاعة بنجاح لـ {count} شخص!**")

@client.on(events.NewMessage(pattern=r'\.اذاعة للجروبات', outgoing=True))
async def bc_groups(event):
    if event.sender_id not in SUDO_USERS: return
    msg = await event.get_reply_message()
    if not msg: return await event.edit("**⚠️ رد على الرسالة التي تريد إذاعتها أولاً!**")
    
    await event.edit("**🚀 جاري الإذاعة لجميع الجروبات...**")
    count = 0
    async for dialog in client.iter_dialogs():
        if dialog.is_group:
            try:
                await client.send_message(dialog.id, msg)
                count += 1
            except: pass
    await event.edit(f"**✅ تمت الإذاعة بنجاح لـ {count} جروب!**")
