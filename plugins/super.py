import asyncio
import os
import pytz
from datetime import datetime
from telethon import events, functions, types

# --- إعدادات الحماية والبيانات ---
approved_users = set()
muted_users = set()
pm_warner = {}
PM_MAX_REPS = 3
security_enabled = True # ميزة إيقاف الحماية

# --- 1. ميزة ساعة النبذة (بتوقيت اليمن الدقيق) ---
async def bio_time_updater(client):
    while True:
        try:
            # استخدام توقيت آسيا/عدن ليتطابق مع ساعة الاسم
            now = datetime.now(pytz.timezone('Asia/Aden'))
            current_time = now.strftime('%I:%M %p')
            my_bio = f"نبذة تعریفیه شخص مغرم بنفسه ولایتنازل لـ خلق الله أبداً {current_time}"
            await client(functions.account.UpdateProfileRequest(about=my_bio))
        except:
            pass
        await asyncio.sleep(60)

# --- 2. حماية الخاص الشاملة (للجميع بلا استثناء) ---
@events.register(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def mutamarrid_guard(event):
    global security_enabled
    if not security_enabled: return # الحماية معطلة
    
    sender = await event.get_sender()
    me = await event.client.get_me()
    
    # استثناءات (أنت، المسموح لهم، البوتات)
    if not sender or sender.id in approved_users or sender.bot or sender.id == me.id:
        return

    # حذف رسائل المكتومين فوراً
    if sender.id in muted_users:
        await event.delete()
        return
    
    if sender.id not in pm_warner: pm_warner[sender.id] = 1
    else: pm_warner[sender.id] += 1
    
    if pm_warner[sender.id] <= PM_MAX_REPS:
        # استخدام event.client بدلاً من الكلاينت المستدعى
        photo = await event.client.download_profile_photo(me.id)
        caption = f"""**‹ مـمـلـكـة الـمـتـمـرد الـتـقـنـيـة ⚡ ›**
**— — — — — — — — — —**
**• عـذراً يـا هـذا.. لـقـد وصـلـت إلـى مـنـطـقـة مـحـظـورة.**
**• خـاص الـمـطـور مـحـمـي بـأنـظـمـة الـرصـد والـحـمـايـة.**

**• الـتـحـذيـر : ({pm_warner[sender.id]} مـن {PM_MAX_REPS})**
**• ارسـل سـبـب تـواجـدك هـنـا بـوضـوح وانـتـظـر الـرد.**

**— — — — — — — — — —**
**‹ نـحـن لا نـنـتـظـر الـفـرص.. نـحـن نـصـنـعـهـا ›**"""
        await event.client.send_file(event.chat_id, photo, caption=caption)
        if photo and os.path.exists(photo): os.remove(photo)
    else:
        await event.reply("**لـقـد نـفـدت فـرصـك.. تـم الـحـظـر! 🔇**")
        await event.client(functions.contacts.BlockRequest(id=sender.id))

# --- 3. أوامر الإدارة (سماح، رفض، كتم، الغاء كتم، تفعيل/تعطيل الحماية) ---
@events.register(events.NewMessage(pattern=r"\.(سماح|رفض|كتم|الغاء الكتم|تفعيل الحماية|تعطيل الحماية)", outgoing=True))
async def admin_cmds(event):
    global security_enabled
    cmd = event.pattern_match.group(1)
    
    if cmd == "تعطيل الحماية":
        security_enabled = False
        return await event.edit("**🛡️ تم تعطيل حماية الخاص بنجاح ❌**")
    elif cmd == "تفعيل الحماية":
        security_enabled = True
        return await event.edit("**🛡️ تم تفعيل حماية الخاص بنجاح ✅**")

    if not event.is_reply: return await event.edit("**⚠️ رد على رسالة الشخص أولاً!**")
    reply = await event.get_reply_message()
    sid = reply.sender_id

    if cmd == "سماح":
        approved_users.add(sid)
        await event.edit("**تـم الـسـماح لـه بـالـدخول ✅**")
    elif cmd == "رفض":
        if sid in approved_users: approved_users.remove(sid)
        await event.edit("**❌ تم الرفض وإلغاء السماح.**")
    elif cmd == "كتم":
        muted_users.add(sid)
        await event.edit("**تـم كـتـم الـمـسـتـخـدم 🤐**")
    elif cmd == "الغاء الكتم":
        if sid in muted_users: muted_users.remove(sid)
        await event.edit("**🔊 تم إلغاء الكتم عن المستخدم.**")

# --- 4. أوامر الفحص والأيدي والألعاب ---
@events.register(events.NewMessage(pattern=r"\.فحص", outgoing=True))
async def check_mutamarrid(event):
    start = datetime.now()
    await event.edit("**جـاري الـفـحـص...**")
    end = datetime.now()
    ms = (round((end - start).total_seconds() * 1000, 2))
    me = await event.client.get_me()
    photo = await event.client.download_profile_photo(me.id)
    await event.client.send_file(event.chat_id, photo, caption=f"**‹ نـظـام الـمـتـمـرد يـعـمـل بـكـفـاءة ⚡ ›**\n**• الـسـرعـة:** `{ms}ms` \n**• الـحـالـة:** مـتـصـل 🦾")
    await event.delete()
    if photo and os.path.exists(photo): os.remove(photo)

@events.register(events.NewMessage(pattern=r"\.(رمي|قمار|سهم|كرة)", outgoing=True))
async def games(event):
    emoji = {"رمي": "🎲", "قمار": "🎰", "سهم": "🎯", "كرة": "⚽"}
    cmd = event.pattern_match.group(1)
    await event.client.send_file(event.chat_id, types.InputMediaDice(emoticon=emoji[cmd]))
    await event.delete()
