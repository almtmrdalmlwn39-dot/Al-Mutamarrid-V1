from telethon import events
from config import SUDO_USERS

# استخدام register بدلاً من client.on
@events.register(events.NewMessage(pattern=r"\.اذاعة للخاص", outgoing=True))
async def bc_private(event):
    # الكود الخاص بك هنا مع تعديل بسيط
    await event.edit("**🚀 جاري الإذاعة للمحادثات الخاصة...**")
    count = 0
    async for dialog in event.client.iter_dialogs():
        if dialog.is_user and not dialog.entity.bot:
            try:
                await event.client.send_message(dialog.id, event.text.replace(".اذاعة للخاص", ""))
                count += 1
            except:
                pass
    await event.edit(f"**✅ تم الإرسال إلى {count} شخص!**")
