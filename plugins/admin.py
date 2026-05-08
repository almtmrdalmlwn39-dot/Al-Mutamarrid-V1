from main import client, CMD_HELP
from telethon import events
import datetime

# تعريف الأوامر لكي تظهر في القائمة الملكية (.م)
CMD_HELP.update({
    "الأدمن والحساب": [
        "معلومات", "ايدي", "الرتبة"
    ]
})

# أمر معلومات (بالرد أو عند كتابة ايدي)
@client.on(events.NewMessage(pattern=r'^\.معلومات|^\.ايدي'))
async def get_info(event):
    target_msg = event
    if event.is_reply:
        target_msg = await event.get_reply_message()
    
    try:
        user = await client.get_entity(target_msg.sender_id)
        
        # تحديد الرتبة تلقائياً
        rank = "عضو على قد حالك"
        if event.is_private:
            rank = "مالك الحساب"
        elif event.is_group:
            permissions = await client.get_permissions(event.chat_id, user.id)
            if permissions.is_creator:
                rank = "المالك (الكنق)"
            elif permissions.is_admin:
                rank = "مشرف (الذراع الأيمن)"

        # تنسيق الرسالة بستايل المتمرد
        info_text = f"""
◈ اسمك ⇐ {user.first_name}
◈ يوزرك ⇐ @{user.username if user.username else 'لا يوجد'}
◈ ايديك ⇐ `{user.id}`
◈ رتبتك ⇐ {rank}
◈ الوقت ⇐ {datetime.datetime.now().strftime('%I:%M%p')}
"""
        # إذا كان الأمر منك يعدل الرسالة، وإذا من غيرك يرد عليه
        if event.out:
            await event.edit(info_text)
        else:
            await event.reply(info_text)

    except Exception as e:
        await event.edit(f"**❌ خطأ في جلب البيانات:** `{e}`")
