import asyncio, os, pytz, re, random
from datetime import datetime
from telethon import events, functions, types, Button
from __main__ import client  

# --- [ إعدادات المتمرد والقائمة البيضاء ] ---
approved_users = set()
muted_users = set()
pm_warner = {}
PM_MAX_REPS = 3
security_enabled = True 

# --- [ 1. محرك الوقت والنبذة اليمنية ] ---
async def bio_time_updater():
    while True:
        try:
            tz = pytz.timezone('Asia/Aden')
            current_time = datetime.now(tz).strftime('%I:%M %p')
            my_bio = f"نبذة تعریفیه شخص مغرم بنفسه ولایتنازل لـ خلق الله أبداً | {current_time}"
            await client(functions.account.UpdateProfileRequest(about=my_bio))
        except: pass
        await asyncio.sleep(60)
client.loop.create_task(bio_time_updater())

# --- [ 2. محرك التلفيش الحقيقي والسبام والإدارة ] ---
@client.on(events.NewMessage(outgoing=True))
async def mutamarrid_war_engine(event):
    cmd = event.text
    chat = event.chat_id

    # 1. تفليش القروب (طرد جماعي)
    if cmd == ".تفليش":
        await event.edit("**🔥 جاري تـصـفـيـة الـقـروب بـالـكـامـل...**")
        async for user in event.client.iter_participants(chat):
            try:
                if not user.admin and not user.is_self:
                    await event.client.kick_participant(chat, user.id)
                    await asyncio.sleep(0.1)
            except: continue
        await event.respond("**✅ تم تفليش القروب بنجاح بواسطة المتمرد!**")

    # 2. تكرار (سبام رسائل)
    elif cmd.startswith(".تكرار"):
        try:
            args = cmd.split(" ", 2)
            count = int(args[1])
            message = args[2]
            await event.delete()
            for i in range(count):
                await event.client.send_message(chat, message)
                await asyncio.sleep(0.05)
        except: await event.edit("**⚠️ استخدم: `.تكرار [العدد] [النص]`**")

    # 3. أمر الايدي (ID) الاحترافي
    elif cmd == ".ايدي" or cmd == "ايدي":
        target = await event.get_reply_message() if event.is_reply else await event.client.get_me()
        user = await event.client.get_entity(target.sender_id if event.is_reply else target.id)
        caption = (
            f"**‹ مـعـلـومـات الـمـسـتـخـدم 🛡️ ›**\n"
            f"**— — — — — — — — — —**\n"
            f"**• الاسم : {user.first_name}**\n"
            f"**• الايدي : `{user.id}`**\n"
            f"**• الرتبة : {'الـمـتـمـرد' if not event.is_reply else 'ضـحـيـة'}**\n"
            f"**• الدولة : اليمن 🇾🇪**\n"
            f"**— — — — — — — — — —**"
        )
        photo = await event.client.download_profile_photo(user.id)
        if photo: 
            await event.client.send_file(chat, photo, caption=caption)
            await event.delete()
        else: await event.edit(caption)

    # 4. أوامر الإدارة (سماح، رفض، كتم)
    if event.is_reply:
        reply = await event.get_reply_message()
        sid = reply.sender_id
        if cmd == ".سماح":
            approved_users.add(sid); await event.edit("**✅ تم السماح له.**")
        elif cmd == ".رفض":
            if event.is_private:
                await event.client(functions.contacts.BlockRequest(id=sid))
                await event.edit("**🚫 تم الحظر من الخاص.**")
            else:
                try: await client.kick_participant(chat, sid); await event.edit("**🚷 تم طرده.**")
                except: await event.edit("**⚠️ لست مشرفاً!**")

    # 5. قائمة الأوامر الشاملة
    elif cmd == ".الاوامر":
        menu = (
            "**📜 قـائـمـة أوامـر الـمـتـمـرد الـخـارقـة :**\n"
            "**— — — — — — — — — —**\n"
            "**🛠️ أوامـر الـتـفـلـيش :**\n"
            "• `.تفليش` : طرد كل أعضاء القروب.\n"
            "• `.تكرار [العدد] [النص]` : سبام رسائل.\n"
            "**👤 أوامـر الـحـسـاب :**\n"
            "• `.ايدي` | `.فحص` | `.المطور`\n"
            "**⚙️ أوامـر الإدارة :**\n"
            "• `.سماح` | `.رفض` | `.كتم`\n"
            "**🎭 أوامـر الـهـيـاط :**\n"
            "• `.تهكير` | `.تلفيش` | `.كشف`\n"
            "**— — — — — — — — — —**\n"
            "**‹ قـوتـنـا فـي تـمـردنا.. الـمـتـمـرد ›**"
        )
        await event.edit(menu)

print("🔥 أوامر المتمرد جاهزة.. تم تعطيل الحماية القديمة لتفعيل الأزرار!")
