from telethon import events, functions, types
import asyncio
import os
from datetime import datetime
from __main__ import client # تصحيح 1: ربط الملف بمحرك البوت

# --- إعدادات الحماية والبيانات ---
approved_users = set()
muted_users = set()
pm_warner = {}
PM_MAX_REPS = 3

# --- 1. ميزة ساعة النبذة (تحديث الوقت تلقائياً) ---
async def bio_time_updater():
    while True:
        try:
            # وقت اليمن الآن بتنسيق 12 ساعة
            current_time = datetime.now().strftime('%I:%M %p')
            # النبذة التي حددتها أنت
            my_bio = f"نبذة تعریفیه شخص مغرم بنفسه ولایتنازل لـ خلق الله أبداً {current_time}"
            await client(functions.account.UpdateProfileRequest(about=my_bio))
        except:
            pass
        await asyncio.sleep(60) # تحديث كل دقيقة

# تصحيح 2: تشغيل دالة الساعة في الخلفية فور تشغيل البوت
client.loop.create_task(bio_time_updater())

# --- 2. حماية الخاص (الرد الهيبة بصورتك الشخصية) ---
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def mutamarrid_guard(event):
    sender = await event.get_sender()
    me = await client.get_me()
    
    # استثناءات (أنت، المسموح لهم، جهات الاتصال، البوتات)
    if not sender or sender.id in approved_users or sender.contact or sender.bot or sender.id == me.id:
        return
    
    if sender.id not in pm_warner: pm_warner[sender.id] = 1
    else: pm_warner[sender.id] += 1
    
    if pm_warner[sender.id] <= PM_MAX_REPS:
        my_photo = await client.download_profile_photo(me.id)
        caption = f"""**‹ مـمـلـكـة الـمـتـمـرد الـتـقـنـيـة ⚡ ›**
**— — — — — — — — — —**
**• عـذراً يـا هـذا.. لـقـد وصـلـت إلـى مـنـطـقـة مـحـظـورة.**
**• خـاص الـمـطـور مـحـمـي بـأنـظـمـة الـرصـد والـحـمـايـة.**

**• الـتـحـذيـر : ({pm_warner[sender.id]} مـن {PM_MAX_REPS})**
**• ارسـل سـبـب تـواجـدك هـنـا بـوضـوح وانـتـظـر الـرد.**

**— — — — — — — — — —**
**‹ نـحـن لا نـنـتـظـر الـفـرص.. نـحـن نـصـنـعـهـا ›**"""
        await client.send_file(event.chat_id, my_photo, caption=caption)
        if my_photo and os.path.exists(my_photo): os.remove(my_photo)
    else:
        await event.reply("**لـقـد نـفـدت فـرصـك.. تـم الـحـظـر! 🔇**")
        await client(functions.contacts.BlockRequest(id=sender.id))

# --- 3. أوامر الفحص والأيدي (بالصور) ---
@client.on(events.NewMessage(pattern=r"\.فحص", outgoing=True))
async def check_mutamarrid(event):
    start = datetime.now()
    await event.edit("**جـاري الـفـحـص...**")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    me = await client.get_me()
    photo = await client.download_profile_photo(me.id)
    await client.send_file(event.chat_id, photo, caption=f"**‹ نـظـام الـمـتـمـرد يـعـمـل بـكـفـاءة ⚡ ›**\n**• الـسـرعـة:** `{ms}ms` \n**• الـحـالـة:** مـتـصـل 🦾")
    await event.delete()
    if photo and os.path.exists(photo): os.remove(photo)

@client.on(events.NewMessage(pattern=r"\.ايدي", outgoing=True))
async def get_id(event):
    user_msg = await event.get_reply_message()
    target = user_msg.sender if user_msg else await client.get_me()
    photo = await client.download_profile_photo(target.id)
    caption = f"**• الأيـدي:** `{target.id}`\n**• الإسـم:** {target.first_name}"
    await client.send_file(event.chat_id, photo, caption=caption)
    await event.delete()
    if photo and os.path.exists(photo): os.remove(photo)

# --- 4. أوامر الإدارة (سماح، كتم، تفليش) ---
@client.on(events.NewMessage(pattern=r"\.سماح", outgoing=True))
async def allow(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        approved_users.add(reply.sender_id)
        await event.edit("**تـم الـسـماح لـه بـالـدخول ✅**")

@client.on(events.NewMessage(pattern=r"\.كتم", outgoing=True))
async def mute(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        muted_users.add(reply.sender_id)
        await event.edit("**تـم كـتـم الـمـسـتـخـدم 🤐**")

@client.on(events.NewMessage(incoming=True))
async def delete_muted(event):
    if event.sender_id in muted_users: await event.delete()

@client.on(events.NewMessage(pattern=r"\.تفليش", outgoing=True))
async def destruction(event):
    await event.edit("**جـاري الـتـفـلـيش.. 🔥**")
    async for user in client.iter_participants(event.chat_id):
        try: await client.kick_participant(event.chat_id, user)
        except: continue

# --- 5. أوامر التسلية ---
@client.on(events.NewMessage(pattern=r"\.رمي", outgoing=True))
async def dice(event):
    await client.send_file(event.chat_id, types.InputMediaDice(emoticon="🎲"))
    await event.delete()
