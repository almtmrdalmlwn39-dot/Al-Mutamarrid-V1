import pytz
from datetime import datetime
from telethon import events
from __main__ import client

# 1. الرد التلقائي الذكي
@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    if event.is_private:
        if 'يا متمرد' in event.raw_text or 'المتمرد' in event.raw_text:
            await event.reply("**لبييييه! المتمرد التقني @Vi_ti0 معك، اؤمرني؟ 😎**")

# 2. أمر الوقت المطور (بتوقيت اليمن)
@client.on(events.NewMessage(pattern=r'\.الوقت', outgoing=True))
async def get_time(event):
    now = datetime.now(pytz.timezone('Asia/Aden'))
    time_str = now.strftime("%I:%M %p")
    date_str = now.strftime("%Y/%m/%d")
    await event.edit(f"🛡️ **سورس المتمرد التقني**\n\n**⌚ الوقت:** `{time_str}`\n**📅 التاريخ:** `{date_str}`")

# 3. أمر الطرد السريع (للمشرفين)
@client.on(events.NewMessage(pattern=r'\.طرد', outgoing=True))
async def kick_user(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        try:
            await client.kick_participant(event.chat_id, reply.sender_id)
            await event.edit("**✅ تم طرد العضو بنجاح!**")
        except:
            await event.edit("**⚠️ لا أملك صلاحيات الطرد!**")

