import os
import sys
import asyncio
from telethon import events
from __main__ import client  # السطر الأهم لربط الملف بالبوت الأساسي

# --- 1. أمر إعادة التشغيل (Restart) ---
@client.on(events.NewMessage(pattern=r"\.اعادة تشغيل", outgoing=True))
async def restart_bot(event):
    await event.edit("**‹ جـاري إعـادة تـشـغـيـل الـمـتـمـرد الـتـقـنـي... ⚡ ›**")
    await asyncio.sleep(2)
    # ينهي العملية الحالية ويشغل البوت من جديد
    os.execl(sys.executable, sys.executable, *sys.argv)

# --- 2. أمر التحديث الجذري (Rebuild/Update) ---
@client.on(events.NewMessage(pattern=r"\.تحديث", outgoing=True))
async def update_bot(event):
    await event.edit("**‹ جـاري سـحـب الـتـحـديـثات مـن الـمـسـتـودع... 📥 ›**")
    try:
        # يسحب آخر التغييرات من GitHub ويمسح أي تعديلات يدوية قديمة
        os.system("git fetch --all && git reset --hard origin/main") 
        await event.edit("**‹ تـم سـحـب الـمـلـفـات بـنـجـاح! جـاري إعـادة الـتـشـغـيل... 🔄 ›**")
        await asyncio.sleep(2)
        os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception as e:
        await event.edit(f"**⚠️ حدث خطأ أثناء التحديث:**\n`{str(e)}`")

# --- 3. أمر تفعيل التخزين ---
@client.on(events.NewMessage(pattern=r"\.تفعيل التخزين", outgoing=True))
async def start_storage(event):
    await event.edit("**‹ جـاري تـفـعـيـل مـيـزة الـتـخـزيـن الـفـخـمـة... 🔥 ›**")
    # يقوم بإرسال أمر الإنشاء الموجود في ملف log.py
    await event.respond(".انشاء تخزين")
    await event.delete()
