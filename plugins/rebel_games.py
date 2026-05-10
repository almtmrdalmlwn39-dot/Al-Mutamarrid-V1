import random, os, json
from telethon import events
from main import client, CMD_HELP

# --- [ أوامر القسم 11: التقنية والألعاب ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"^زواج$"))
async def mry(e):
    u = await client.get_participants(e.chat_id)
    r = [x for x in u if not x.bot]
    if len(r) < 2: return await e.edit("**⚠️ مابش أعضاء كفاية.**")
    a, b = random.sample(r, 2)
    await e.edit(f"**💍 عرسان القروب:**\n🤵: [{a.first_name}](tg://user?id={a.id})\n👰: [{b.first_name}](tg://user?id={b.id})")

# --- [ التحديث الإجباري للقائمة 11 ] ---
CMD_HELP["التقنية والألعاب"] = [
    "**-** `زواج` | `كشف` | `منو`",
    "**-** `رفع تاج` | `رفع قلبي`",
    "**-** أوامر التقنية الأساسية شغالـة."
]
