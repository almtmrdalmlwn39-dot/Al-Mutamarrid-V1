import asyncio
import os
import pytz
from datetime import datetime
from telethon import events, functions, types, Button
from __main__ import client  

# --- إعدادات الحماية (تخزين في الذاكرة لتجاوز خطأ قاعدة البيانات) ---
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
            my_bio = f"نبذة تعریفیه شخص مغرم بنفسه ولایتنازل لـ خلق الله أبداً {current_time}"
            await client(functions.account.UpdateProfileRequest(about=my_bio))
        except: pass
        await asyncio.sleep(60)

client.loop.create_task(bio_time_updater())

# --- 2. حماية الخاص وإظهار الأزرار ---
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def mutamarrid_guard(event):
    global security_enabled
    if not security_enabled: return
    sender = await event.get_sender()
    me = await event.client.get_me()
    
    if not sender or sender.bot or sender.id == me.id or sender.id in approved_users: return
    if sender.id in muted_users: return
    
    if sender.id not in pm_warner: pm_warner[sender.id] = 1
    else: pm_warner[sender.id] += 1
    
    if pm_warner[sender.id] <= PM_MAX_REPS:
        photo = await event.client.download_profile_photo(me.id)
        caption = (
            "**‹ مـمـلـكـة الـمـتـمـرد الـتـقـنـيـة ⚡ ›**\n"
            "**— — — — — — — — — —**\n"
            f"**• الـتـحـذيـر : ({pm_warner[sender.id]} مـن {PM_MAX_REPS})**\n"
            "**• حـدد سـبـب تـواجـدك بـالأزرار لـتـفـادي الـحـظـر :**\n"
            "**— — — — — — — — — —**\n"
        )
        # مصفوفة الأزرار الشفافة
        buttons = [
            [Button.url("• طـلـب مـسـاعـدة •", f"tg://user?id={me.id}")],
            [Button.url("• مـراسـلـة الـمـطـور •", f"tg://user?id={me.id}")]
        ]
        await event.client.send_file(event.chat_id, photo, caption=caption, buttons=buttons)
        if photo and os.path.exists(photo): os.remove(photo)
    else:
        await event.client(functions.contacts.BlockRequest(id=sender.id))

# --- 3. أوامر الإدارة الشاملة (تعديل لضمان الظهور) ---
@client.on(events.NewMessage(pattern=r"\.(سماح|كتم|رفض|فحص)", outgoing=True))
async def admin_cmds(event):
    try:
        # أمر الفحص للتأكد من عمل السورس
        if ".فحص" in event.text:
            return await event.edit("**⚡ سـورس الـمـتـمـرد شـغـال والأوامـر سـبـرت!**")
        
        if not event.is_reply: 
            return await event.edit("**⚠️ يجب الرد على رسالة المستخدم لتنفيذ الأمر!**")
        
        reply = await event.get_reply_message()
        sid = reply.sender_id
        
        if ".سماح" in event.text:
            approved_users.add(sid)
            await event.edit(f"**تـم الـسـماح لـه بـالـدخول ✅**")
            
        elif ".كتم" in event.text:
            muted_users.add(sid)
            await event.edit(f"**تـم كـتـم الـمـسـتـخـدم 🤐**")
            
        elif ".رفض" in event.text:
            if event.is_private:
                await event.client(functions.contacts.BlockRequest(id=sid))
                await event.edit("**🚫 تم رفض المستخدم وحظره من الخاص.**")
            else:
                try:
                    await client.kick_participant(event.chat_id, sid)
                    await event.edit("**🚷 تم طرد المستخدم بنجاح.**")
                except:
                    await event.edit("**⚠️ فشل الطرد! تأكد من صلاحيات المشرف.**")
                    
    except Exception as e: await event.edit(f"**خطأ: {e}**")
