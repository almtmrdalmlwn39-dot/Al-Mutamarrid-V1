import asyncio
import os
import pytz
from datetime import datetime
from telethon import events, functions, types, Button
from __main__ import client  # استدعاء الكلاينت الرئيسي للتشغيل

# --- إعدادات الحماية والبيانات ---
approved_users = set()
muted_users = set()
pm_warner = {}
PM_MAX_REPS = 3
security_enabled = True 

# --- 1. ميزة ساعة النبذة (بتوقيت اليمن) ---
async def bio_time_updater():
    while True:
        try:
            tz = pytz.timezone('Asia/Aden')
            now = datetime.now(tz)
            current_time = now.strftime('%I:%M %p')
            # النبذة الخاصة بك مع الوقت
            my_bio = f"نبذة تعریفیه شخص مغرم بنفسه ولایتنازل لـ خلق الله أبداً {current_time}"
            await client(functions.account.UpdateProfileRequest(about=my_bio))
        except Exception as e:
            print(f"Error in bio: {e}")
        await asyncio.sleep(60)

# تشغيل الساعة تلقائياً في الخلفية
client.loop.create_task(bio_time_updater())

# --- 2. حماية الخاص الشاملة بالأزرار الشفافة ---
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def mutamarrid_guard(event):
    global security_enabled
    if not security_enabled: return
    
    sender = await event.get_sender()
    me = await event.client.get_me()
    
    # استثناء نفسك والبوتات والمسموح لهم سابقاً
    if not sender or sender.bot or sender.id == me.id or sender.id in approved_users:
        return

    if sender.id in muted_users:
        return await event.delete()
    
    if sender.id not in pm_warner: pm_warner[sender.id] = 1
    else: pm_warner[sender.id] += 1
    
    if pm_warner[sender.id] <= PM_MAX_REPS:
        photo = await event.client.download_profile_photo(me.id)
        
        caption = (
            "**‹ مـمـلـكـة الـمـتـمـرد الـتـقـنـيـة ⚡ ›**\n"
            "**— — — — — — — — — —**\n"
            "**• عـذراً يـا هـذا.. لـقـد وصـلـت إلـى مـنـطـقـة مـحـظـورة.**\n"
            "**• خـاص الـمـطـور مـحـمـي بـأنـظـمـة الـرصـد والـحـمـايـة.**\n\n"
            f"**• الـتـحـذيـر : ({pm_warner[sender.id]} مـن {PM_MAX_REPS})**\n"
            "**• حـدد سـبـب تـواجـدك بـالضغط على الأزرار :**\n"
            "**— — — — — — — — — —**\n"
            "**‹ نـحـن لا نـنـتـظـر الـفـرص.. نـحـن نـصـنـعـهـا ›**"
        )
        
        buttons = [
            [Button.url("• طـلـب مـسـاعـدة •", f"tg://user?id={me.id}")],
            [Button.url("• مـراسـلـة الـمـطـور •", f"tg://user?id={me.id}")]
        ]
        
        await event.client.send_file(event.chat_id, photo, caption=caption, buttons=buttons)
        if photo and os.path.exists(photo): os.remove(photo)
    else:
        await event.reply("**لـقـد نـفـدت فـرصـك.. تـم الـحـظـر! 🔇**")
        await event.client(functions.contacts.BlockRequest(id=sender.id))

# --- 3. أوامر الإدارة ---
@client.on(events.NewMessage(pattern=r"\.(سماح|كتم)", outgoing=True))
async def admin_cmds(event):
    if not event.is_reply: return await event.edit("**⚠️ رد على رسالة الشخص!**")
    reply = await event.get_reply_message()
    sid = reply.sender_id
    if ".سماح" in event.text:
        approved_users.add(sid)
        await event.edit("**تـم الـسـماح لـه بـالـدخول ✅**")
    elif ".كتم" in event.text:
        muted_users.add(sid)
        await event.edit("**تـم كـتـم الـمـسـتـخـدم 🤐**")

# أمر الفحص
@client.on(events.NewMessage(pattern=r"\.فحص", outgoing=True))
async def ping_cmd(event):
    await event.edit("**⚡ سـورس الـمـتـمـرد يـعـمـل بـنـجـاح!**")
