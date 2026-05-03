from telethon import events, functions
from __main__ import client
import random

# --- [ 1. أوامر التسلية والترفيه ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.نسبة الحب"))
async def love(event):
    await event.edit(f"**- نسبة الحب هي : {random.randint(0, 100)}% ❤️**")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.كشف الكذب"))
async def lie(event):
    results = ["كاذب ❌", "صادق ✅", "نصاب كبير 🤡", "ماشاء الله صادق 🙏"]
    await event.edit(f"**- النتيجة هي : {random.choice(results)}**")

# --- [ 2. أوامر المجموعات الإضافية ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.غادر"))
async def leave(event):
    await event.edit("**- المتمرد يغادر المكان.. وداعاً 🦅**")
    await client(functions.channels.LeaveChannelRequest(event.chat_id))

@client.on(events.NewMessage(outgoing=True, pattern=r"\.الرابط"))
async def get_link(event):
    res = await client(functions.messages.ExportChatInviteRequest(event.chat_id))
    await event.edit(f"**- رابط المجموعة : {res.link}**")

# --- [ 3. أوامر المعلومات ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.ايدي"))
async def get_id(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        await event.edit(f"**- ايدي الشخص : `{reply.sender_id}`**")
    else:
        await event.edit(f"**- ايدي الدردشة : `{event.chat_id}`**")
