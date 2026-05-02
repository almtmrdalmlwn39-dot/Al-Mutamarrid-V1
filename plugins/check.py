from telethon import events
from . import client

@client.on(events.NewMessage(outgoing=True, pattern=r"\.فحص"))
async def check(event):
    await event.edit("**⚡ سورس المتمرد شغال بنجاح!**")
