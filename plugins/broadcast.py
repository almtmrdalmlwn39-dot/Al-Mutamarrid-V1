from main import client, CMD_HELP
from telethon import events
import config

# إضافة الأمر لقائمة المتمرد بستايل زدثون
CMD_HELP.update({
    "الإذاعة والنشر": [
        "للخاص"
    ]
})

# أمر الإذاعة للمحادثات الخاصة
@client.on(events.NewMessage(outgoing=True, pattern=r"\.للخاص"))
async def bc_private(event):
    await event.edit("**🚀 جاري الإذاعة للمحادثات الخاصة...**")
    count = 0
    
    # جلب كافة المحادثات
    async for dialog in client.iter_dialogs():
        # التحقق أن المحادثة مستخدم وليست بوت أو جروب
        if dialog.is_user and not dialog.entity.bot:
            try:
                # إرسال الرسالة (يجب أن تكون رداً على الرسالة المراد إذاعتها)
                if event.is_reply:
                    msg = await event.get_reply_message()
                    await client.send_message(dialog.id, msg)
                else:
                    return await event.edit("**⚠️ يجب الرد على الرسالة التي تريد إذاعتها أولاً!**")
                
                count += 1
            except Exception:
                pass
                
    await event.edit(f"**✅ تم الإرسال إلى {count} شخص بنجاح.**")
