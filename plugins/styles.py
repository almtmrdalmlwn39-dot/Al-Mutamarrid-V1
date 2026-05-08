import asyncio
from datetime import datetime
import pytz
from telethon import events
from telethon.tl.functions.account import UpdateProfileRequest, GetFullUserRequest
from main import client, CMD_HELP, WAR_IDENTITY

# إعداد توقيت اليمن
YEMEN_TZ = pytz.timezone('Asia/Aden')

# تسجيل القسم في قائمة المساعدة
CMD_HELP.update({
    "الأنماط والوقت": ["اسم_وقتي", "نبذة_وقتية", "بينج"]
})

# 1. ميزة الاسم الوقتي الذكية (تأخذ اسم الشخص الحالي)
@client.on(events.NewMessage(pattern=r'\.اسم_وقتي', outgoing=True))
async def autoname(event):
    await event.edit("**✅ تم تفعيل الاسم الوقتي.. سيتم دمج الوقت مع اسمك الحالي!**")
    
    # جلب معلومات المستخدم الحالي لمرة واحدة
    me = await client.get_me()
    base_name = me.first_name # يأخذ اسم الشخص المنصب للسورس
    
    while True:
        now = datetime.now(YEMEN_TZ)
        time_str = now.strftime("%I:%M %p")
        # دمج اسم الشخص مع الوقت تلقائياً
        new_name = f"{base_name} | {time_str}"
        try:
            await client(UpdateProfileRequest(first_name=new_name))
        except Exception as e: 
            print(f"Error: {e}")
        await asyncio.sleep(60)

# 2. ميزة النبذة الوقتية الذكية (تأخذ نبذة الشخص الحالية)
@client.on(events.NewMessage(pattern=r'\.نبذة_وقتية', outgoing=True))
async def autobio(event):
    await event.edit("**✅ تم تفعيل النبذة الوقتية.. سيتم إضافة الوقت لنبذتك الحالية!**")
    
    # جلب نبذة الشخص الحالية (المنصب للسورس)
    full_me = await client(GetFullUserRequest('me'))
    base_bio = full_me.full_user.about or "" # يأخذ النبذة الحالية
    
    while True:
        now = datetime.now(YEMEN_TZ)
        time_str = now.strftime("%I:%M %p")
        # دمج نبذة الشخص مع الوقت
        new_bio = f"{base_bio} | {time_str}"
        try:
            await client(UpdateProfileRequest(about=new_bio))
        except Exception as e: 
            print(f"Error: {e}")
        await asyncio.sleep(60)
