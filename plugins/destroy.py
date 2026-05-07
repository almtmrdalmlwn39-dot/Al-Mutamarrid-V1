@client.on(events.NewMessage(outgoing=True, pattern=r"\.تلفيش"))
async def rebel_destruction_engine(event):
    chat = await event.get_chat()
    admin_id = (await client.get_me()).id
    count = 0
    
    await event.edit("**🛡️ جاري إحكام السيطرة على المجموعة... ⚠️**")
    await asyncio.sleep(1)
    await event.edit("**🧨 بدأ الانفجار.. لا مكان للضعفاء هنا 🧨**")
    
    # سحب الأعضاء بشكل قسري ومباشر من السيرفر
    async for user in client.iter_participants(chat):
        # تخطي نفسك عشان ما ينحظر الحساب المشغل
        if user.id == admin_id or user.is_self:
            continue
            
        try:
            # أقوى أمر حظر نهائي في تليجرام
            await client(functions.channels.EditBannedRequest(
                channel=chat,
                participant=user.id,
                banned_rights=types.ChatBannedRights(
                    until_date=None,
                    view_messages=True,
                    send_messages=True,
                    send_media=True,
                    send_stickers=True,
                    send_gifs=True,
                    send_games=True,
                    send_inline=True,
                    embed_links=True
                )
            ))
            count += 1
            # تحديث العداد كل 5 أعضاء عشان تلاحظ الحركة
            if count % 5 == 0:
                await event.edit(f"**🔥 جاري الانفجار.. الضحايا: {z_nums(str(count))}**")
        except Exception:
            # يتخطى المشرفين أو الحسابات المحمية بصمت
            continue

    msg = f"**✅ انتهت المهمة بنجاح**\n"
    msg += f"**- الأرض أصبحت قاعاً صفصفاً بعد مرور المتمرد.**\n"
    msg += f"**- اجمالي الضحايا: {z_nums(str(count))}**\n"
    msg += f"**- المتمرد التقني مر من هنا 🦅**"
    await event.edit(msg)
