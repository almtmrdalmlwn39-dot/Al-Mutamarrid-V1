from telethon import events, Button, functions
from datetime import datetime
import pytz

user_counts = {}

def get_rebel_design(u_id, name, count):
    tz = pytz.timezone('Asia/Riyadh')
    current_time = datetime.now(tz).strftime("%I:%M %p")
    status = f"⚠️ تحذير: ({count}/5)" if count > 1 else "📡 الحالة: نشط"
    return f"\n┏━━━━━━━ ● ⚖️ ● ━━━━━━━┓\n     مساحة المتمرد التقنية\n┗━━━━━━━ ● ⚖️ ● ━━━━━━━┛\n\n👤 الضيف : {name}\n🆔 الأيدي : `{u_id}`\n🕒 الوقت : `{current_time}`\n{status}\n\n📜 النبذة: شخص مغرم بنفسه ولا يتنازل لخلق الله ابداً.\n- - - - - - - -\n┗━━━━━━━━━━━━━━━━━━━━━┛\n"

async def start_welcome(event, client):
    if event.is_private and not event.out:
        try:
            u_id = event.sender_id
            sender = await event.get_sender()
            name = getattr(sender, 'first_name', "مجهول") or "مجهول"
            if u_id not in user_counts: user_counts[u_id] = 0
            user_counts[u_id] += 1
            if user_counts[u_id] >= 5:
                await event.respond("🚫 تم الحظر التلقائي لتجاوز الحد.")
                await client(functions.contacts.BlockRequest(id=u_id))
                return
            await event.respond(get_rebel_design(u_id, name, user_counts[u_id]),
                buttons=[[Button.inline("💠 سماح", data=f"ok_{u_id}"), Button.inline("🚫 حظر", data=f"no_{u_id}")]])
        except: pass

async def start_callbacks(event, client, bot):
    try:
        data = event.data.decode('utf-8')
        t_id = int(data.split('_')[1])
        if data.startswith('ok'):
            user_counts[t_id] = 0
            await event.edit("✅ تم منح السماح لهذا الشخص بنجاح.")
        elif data.startswith('no'):
            await client(functions.contacts.BlockRequest(id=t_id))
            await event.edit("🚫 تم الحظر النهائي لهذا الشخص.")
    except: pass
