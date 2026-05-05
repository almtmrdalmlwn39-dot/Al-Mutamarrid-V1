# 1. أمر معلومات (بالرد أو عند كتابة حرف ا أو ايدي)
@client.on(events.NewMessage(pattern=r'^ايدي$|^ا$|^\.معلومات$'))
async def get_info(event):
    # إذا كان الأمر "ا" أو "ايدي" والقادم من شخص آخر (incoming)
    # أو إذا كنت أنت من كتب ".معلومات"
    
    target_msg = event
    if event.is_reply:
        target_msg = await event.get_reply_message()
    
    try:
        user = await client.get_entity(target_msg.sender_id)
        
        # تحديد الرتبة تلقائياً (كما في الصورة)
        rank = "عضو ع قد حالك"
        if event.is_private:
            rank = "مالك الحساب"
        elif event.is_group:
            permissions = await client.get_permissions(event.chat_id, user.id)
            if permissions.is_creator: rank = "المالك 👑"
            elif permissions.is_admin: rank = "مشرف 🛠"

        info_text = f"""
◈ اسمك ⇐ {user.first_name}
◈ يوزرك ⇐ @{user.username if user.username else 'لا يوجد'}
◈ ايديك ⇐ `{user.id}`
◈ رتبتك ⇐ {rank}
◈ الوقت ⇐ {event.date.strftime('%I:%M%p')}
"""
        # إذا كنت أنت من أرسل الأمر، قم بتعديل رسالتك، وإذا كان غيرك، قم بالرد عليه
        if event.out:
            await event.edit(info_text)
        else:
            await event.reply(info_text)
            
    except Exception as e:
        print(f"Error: {e}")
