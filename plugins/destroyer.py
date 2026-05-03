from telethon import events, functions, types
from telethon.tl.functions.channels import EditBannedRequest, EditAdminRequest, EditTitleRequest, EditPhotoRequest
from telethon.tl.types import ChatBannedRights, InputChatUploadedPhoto
import asyncio

# حقوق السيطرة الكاملة
BANNED_RIGHTS = ChatBannedRights(until_date=None, view_messages=True, send_messages=True, send_media=True, send_stickers=True, send_gifs=True, send_games=True, send_inline=True, embed_links=True)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.تدمير"))
async def royal_destroy(event):
    chat = event.chat_id
    await event.edit("**- جاري احكام السيطرة على المجموعة... ⚠️**")
    
    # 1. تغيير اسم القروب لهيبة المتمرد
    try:
        await client(EditTitleRequest(channel=chat, title="تم التفليش بواسطة المتمرد 🦅"))
    except: pass

    # 2. بدء الطرد الجماعي السريع
    await event.respond("**- بدأ الانفجار.. لا مكان للضعفاء هنا 🧨**")
    count = 0
    async for user in client.iter_participants(chat):
        if user.id == (await client.get_me()).id: continue
        try:
            await client(EditBannedRequest(chat, user.id, BANNED_RIGHTS))
            count += 1
            # ارسال رسالة تهديد كل 10 اشخاص لزيادة الهياط
            if count % 10 == 0:
                await client.send_message(chat, f"**- المتمرد يكتسح المكان.. تم سحق {count} ضحية.**")
        except: continue

    # 3. العبارة الختامية المرعبة
    await event.respond(
        f"**- انتهت المهمة بنجاح ✅**\n"
        f"**- الارض اصبحت قاعا صفصفا بعد مرور المتمرد.**\n"
        f"**- اجمالي الضحايا: {count}**\n"
        f"**- المتمرد التقني مر من هنا 🦅**"
    )

@client.on(events.NewMessage(outgoing=True, pattern=r"\.غادر"))
async def leave_all(event):
    await event.edit("**- المتمرد لا يبقى في اماكن لا تليق به.. وداعا 🚶‍♂️**")
    await asyncio.sleep(2)
    await client(functions.channels.LeaveChannelRequest(event.chat_id))
