from telethon import events, Button, functions
from datetime import datetime
import pytz

# سجل لتتبع عدد الرسائل
user_counts = {}

def get_rebel_design(u_id, name, count):
    tz = pytz.timezone('Asia/Riyadh')
    current_time = datetime.now(tz).strftime("%I:%M %p")
    status = f"⚠️ تحذير: ({count}/5)" if count > 1 else "📡 الحالة: نشط"
    
    return f"""
┏━━━━━━━ ● ⚖️ ● ━━━━━━━┓
     مساحة المتمرد التقنية
┗━━━━━━━ ● ⚖️ ● ━━━━━━━┛

👤 الضيف : {name}
🆔 الأيدي : `{u_id}`
🕒 الوقت : `{current_time}`
{status}

📜 النبذة: شخص مغرم بنفسه ولا يتنازل لخلق الله ابداً.
- - - - - - - -
┗━━━━━━━━━━━━━━━━━━━━━┛
"""

# دالة المعالجة الأساسية
async def start_welcome(event, client):
    if event.is_private and not event.out:
        u_id = event.sender_id
        name = (event.sender.first_name or "مجهول")
        
        if u_id not in user_counts: user_counts[u_id] = 0
        user_counts[u_id] += 1

        if user_counts[u_id] >= 5:
            await event.respond("🚫 تم الحظر التلقائي لتجاوز الحد.")
            await client(functions.contacts.BlockRequest(id=u_id))
            return

        await event.respond(get_rebel_design(u_id, name, user_counts[u_id]),
            buttons=[[Button.inline("💠 سماح", data=f"ok_{u_id}"), 
                     Button.inline("🚫 حظر", data=f"no_{u_id}")]])

# دالة معالجة الأزرار
async def start_callbacks(event, client):
    data = event.data.decode('utf-8')
    t_id = int(data.split('_')[1])
    if data.startswith('ok'):
        user_counts[t_id] = 0
        await event.edit("✅ تم السماح له.")
    elif data.startswith('no'):
        await event.edit("🚫 تم الحظر النهائي.")
        await client(functions.contacts.BlockRequest(id=t_id))
