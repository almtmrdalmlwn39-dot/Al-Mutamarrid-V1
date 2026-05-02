import asyncio
from datetime import datetime
import pytz
from telethon import events  # تصحيح: إضافة استيراد الأحداث
from telethon.tl.functions.account import UpdateProfileRequest
from __main__ import client

# 1. ميزة الاسم الوقتي: تحديث اسمك تلقائياً كل دقيقة مع الساعة
@client.on(events.NewMessage(pattern=r'\.اسم وقتي', outgoing=True))
async def autoname(event):
    await event.edit("**✅ تم تفعيل ميزة الاسم الوقتي للمتمرد!**")
    while True:
        # توقيت اليمن (آسيا/عدن)
        now = datetime.now(pytz.timezone('Asia/Aden'))
        time_str = now.strftime("%I:%M %p")
        new_name = f"المتمرد | {time_str}"
        try:
            # التعديل: قمنا بإضافة first_name=new_name لضمان التحديث
            await client(UpdateProfileRequest(first_name=new_name))
        except Exception as e: 
            print(f"Error: {e}")
        # الانتظار دقيقة كاملة قبل التحديث القادم
        await asyncio.sleep(60)

# 2. ميزة فحص السرعة البسيطة
@client.on(events.NewMessage(pattern=r'\.بينج', outgoing=True))
async def ping(event):
    start = datetime.now()
    await event.edit("**🚀 جاري قياس سرعة المتمرد...**")
    end = datetime.now()
    # حساب سرعة الاستجابة بالملي ثانية
    ms = (end - start).microseconds / 1000
    await event.edit(f"**🛡️ سورس المتمرد التقني شغال!\n⚡ السرعة: {ms}ms**")
