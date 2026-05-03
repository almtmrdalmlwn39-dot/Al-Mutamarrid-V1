import asyncio, os, pytz, re, random
from datetime import datetime
from telethon import events, functions, types, Button
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from __main__ import client  

# --- [ اعدادات المتمرد ] ---
approved_users = set()

# حقوق الحظر الكاملة للتفليش
BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

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

# --- [ 2. محرك التفليش الحقيقي والادارة ] ---
@client.on(events.NewMessage(outgoing=True))
async def mutamarrid_engine(event):
    cmd = event.text
    chat = event.chat_id

    # 1. تفليش القروب (طرد جماعي حقيقي مع عبارة المتمرد)
    if cmd == ".تفليش":
        await event.edit("**- جاري بدء عملية التفليش الحقيقية... 🧨**")
        count = 0
        async for user in client.iter_participants(chat):
            if user.id == (await client.get_me()).id: continue
            try:
                await client(EditBannedRequest(chat, user.id, BANNED_RIGHTS))
                count += 1
            except: continue
        
        # عبارة المتمرد عند الانتهاء
        await event.respond(
            f"**- تم تفليش المجموعة بنجاح ✅**\n"
            f"**- عدد المطرودين : {count}**\n\n"
            f"**- هنا سادت القوة، وهنا فرض المتمرد سيطرته.. لا احد ينجو من طغيان المتمرد 🦅**"
        )

    # 2. تصفية الحسابات المحذوفة
    elif cmd == ".تصفية":
        await event.edit("**- جاري تصفية الحسابات المحذوفة... 🔍**")
        count = 0
        async for user in client.iter_participants(chat):
            if user.deleted:
                try:
                    await client.kick_participant(chat, user.id)
                    count += 1
                except: continue
        await event.edit(f"**- تمت التصفية بنجاح ✅**\n**- تم حذف {count} حساب محذوف.**")

    # 3. سبام (تكرار)
    elif cmd.startswith(".تكرار"):
        try:
            args = cmd.split(" ", 2)
            count = int(args[1])
            message = args[2]
            await event.delete()
            for i in range(count):
                await client.send_message(chat, message)
                await asyncio.sleep(0.1)
        except: await event.edit("**- استخدم: .تكرار [العدد] [النص]**")

    # 4. أمر الايدي (ID) العريض
    elif cmd == ".ايدي" or cmd == "ايدي":
        target = await event.get_reply_message() if event.is_reply else await client.get_me()
        user = await client.get_entity(target.sender_id if event.is_reply else target.id)
        caption = (
            f"**- معلومات المستخدم 🛡️**\n"
            f"**- - - - - - - - - -**\n"
            f"**- الاسم : {user.first_name}**\n"
            f"**- الايدي : `{user.id}`**\n"
            f"**- الرتبة : {'المتمرد' if not event.is_reply else 'الضحية'}**\n"
            f"**- الدولة : اليمن 🇾🇪**\n"
            f"**- - - - - - - - - -**"
        )
        photo = await client.download_profile_photo(user.id)
        if photo: 
            await client.send_file(chat, photo, caption=caption)
            await event.delete()
        else: await event.edit(caption)

    # 5. قائمة الاوامر
    elif cmd == ".الاوامر":
        menu = (
            "**- قائمة اوامر المتمرد الخارقة :**\n"
            "**- - - - - - - - - -**\n"
            "**- اوامر التفليش :**\n"
            "**• .تفليش : طرد كل اعضاء القروب.**\n"
            "**• .تصفية : حذف الحسابات المحذوفة.**\n"
            "**• .تكرار [العدد] [النص] : سبام رسائل.**\n\n"
            "**- اوامر الحساب :**\n"
            "**• .ايدي | .فحص | .المطور**\n\n"
            "**- اوامر الادارة :**\n"
            "**• .سماح | .رفض | .حظر**\n"
            "**- - - - - - - - - -**\n"
            "**- قوتنا في تمردنا.. المتمرد**"
        )
        await event.edit(menu)

print("🔥 تم التحديث.. سورس المتمرد جاهز للانفجار!")
