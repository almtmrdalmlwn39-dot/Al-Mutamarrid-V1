from telethon import events
@events.register(events.NewMessage(pattern=".فحص"))
async def check(event):
    await event.edit("**سورس المتمرد شغال بنجاح! ⚡**")
