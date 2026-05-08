import asyncio
from datetime import datetime
import pytz
from telethon import events
# تم التصحيح: نقل GetFullUserRequest من account إلى users
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest
from main import client, CMD_HELP, WAR_IDENTITY

# إعداد توقيت اليمن
YEMEN_TZ = pytz.timezone('Asia/Aden')

# تسجيل القسم في قائمة المساعدة
CMD_HELP.update({
    "الأنماط والوقت": ["اسم_وقتي", "نبذة_وقتية"]
})

# 1. ميزة الاسم الوقتي الذكية
@client.on(events.NewMessage(pattern=r'\.اسم_وقتي', outgoing=True))
async def autoname(event):
    await event.edit("**✅ تم تفعيل الاسم الوقتي.. سيتم دمج الوقت مع اسمك الحالي!**")
    me = await client.get_me()
    base_name = me.first_name 
    while True:
        time_str = datetime.now(YEMEN_TZ).strftime("%I:%M %p")
        new_name = f"{base_name} | {time_str}"
        try:
            await client(UpdateProfileRequest(first_name=new_name))
        except: pass
        await asyncio.sleep(60)

# 2. ميزة النبذة الوقتية الذكية
@client.on(events.NewMessage(pattern=r'\.نبذة_وقتية', outgoing=True))
async def autobio(event):
    await event.edit("**✅ تم تفعيل النبذة الوقتية.. سيتم إضافة الوقت لنبذتك الحالية!**")
    try:
        full_me = await client(GetFullUserRequest('me'))
        base_bio = full_me.full_user.about or ""
    except: base_bio = ""
    
    while True:
        time_str = datetime.now(YEMEN_TZ).strftime("%I:%M %p")
        new_bio = f"{base_bio} | {time_str}"
        try:
            await client(UpdateProfileRequest(about=new_bio))
        except: pass
        await asyncio.sleep(60)
