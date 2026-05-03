import asyncio
from datetime import datetime
import pytz
from telethon import events
from telethon.tl.functions.account import UpdateProfileRequest
from __main__ import client

# 1. ميزة الاسم الوقتي: اسمك ثابت والساعة تتغير تلقائياً كل دقيقة
@client.on(events.NewMessage(pattern=r'\.اسم وقتي', outgoing=True))
async def autoname(event):
    await event.edit("**✅ تم تفعيل ميزة الاسم الوقتي لـ فــرانــكَـَۄ!**")
    while True:
        # توقيت اليمن (آسيا/عدن) لضمان الدقة
        now = datetime.now(pytz.timezone('Asia/Aden'))
        time_str = now.strftime("%I:%M %p")
        
        # الاسم الذي طلبته مع الساعة
        name_fixed = "فــرانــكَـَۄ|| 𝗟َِ𝗢َِ𝗿َِ𝗶َِ𝗙َِ𝗲َِ𝗹↜͟͞💸⁩"
        new_name = f"{name_fixed} | {time_str}"
        
        try:
            # تحديث الاسم الأول في البروفايل
            await client(UpdateProfileRequest(first_name=new_name))
        except Exception as e: 
            print(f"Error updating name: {e}")
            
        # الانتظار 60 ثانية للتحديث القادم
        await asyncio.sleep(60)

# 2. ميزة فحص السرعة (بينج)
@client.on(events.NewMessage(pattern=r'\.بينج', outgoing=True))
async def ping(event):
    start = datetime.now()
    await event.edit("**🚀 جاري قياس السرعة...**")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(f"**⚡ سرعة استجابة المتمرد: {ms}ms**")
