import asyncio
from datetime import datetime
import pytz
from telethon import events
from telethon.tl.functions.account import UpdateProfileRequest
from __main__ import client

# --- [ إعدادات الهوية الثابتة ] ---
NAME_FIXED = "فــرانــكَـَۄ|| 𝗟َِ𝗢َِ𝗿َِ𝗶َِ𝗙َِ𝒆َِل↜͟͞💸⁩"
BIO_FIXED = "نبذة تعريفية شخص مغرم بنفسه ولايتنازل لـ خلق الله ابدا"
YEMEN_TZ = pytz.timezone('Asia/Aden')

# 1. ميزة الاسم الوقتي (تحدث الاسم فقط)
@client.on(events.NewMessage(pattern=r'\.اسم وقتي', outgoing=True))
async def autoname(event):
    await event.edit("**✅ تم تفعيل ميزة الاسم الوقتي لـ فــرانــكَـَۄ!**")
    while True:
        now = datetime.now(YEMEN_TZ)
        time_str = now.strftime("%I:%M %p")
        new_name = f"{NAME_FIXED} | {time_str}"
        try:
            await client(UpdateProfileRequest(first_name=new_name))
        except Exception as e: 
            print(f"Error in autoname: {e}")
        await asyncio.sleep(60)

# 2. ميزة النبذة الوقتية (تحدث النبذة فقط)
@client.on(events.NewMessage(pattern=r'\.نبذة وقتية', outgoing=True))
async def autobio(event):
    await event.edit("**✅ تم تفعيل ميزة النبذة الوقتية بـفخامة! ⏳**")
    while True:
        now = datetime.now(YEMEN_TZ)
        time_str = now.strftime("%I:%M %p")
        new_bio = f"{BIO_FIXED} | {time_str}"
        try:
            await client(UpdateProfileRequest(about=new_bio))
        except Exception as e: 
            print(f"Error in autobio: {e}")
        await asyncio.sleep(60)

# 3. ميزة فحص السرعة (بينج)
@client.on(events.NewMessage(pattern=r'\.بينج', outgoing=True))
async def ping(event):
    start = datetime.now()
    await event.edit("**🚀 جاري قياس السرعة...**")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(f"**⚡ سرعة استجابة المتمرد: {ms}ms**")
