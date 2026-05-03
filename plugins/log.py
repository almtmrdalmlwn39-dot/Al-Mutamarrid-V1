from telethon import events, functions, types
import os

# --- كود إنشاء جروب التخزين الفخم تلقائياً ---

# متغير لتخزين أيدي الجروب برمجياً لكي لا تضطر لكتابته يدوياً
LOG_GROUP_ID = None 

@events.register(events.NewMessage(pattern=r"\.انشاء تخزين", outgoing=True))
async def create_fakhama_log(event):
    global LOG_GROUP_ID
    await event.edit("**جـاري تـأسـيـس مـمـلـكـة الـتـخـزيـن الـفـخـمـة... 🔥**")
    
    try:
        me = await event.client.get_me()
        
        # 1. إنشاء الجروب
        result = await event.client(functions.channels.CreateChannelRequest(
            title="سجل رسائل المتمرد التقني 📥",
            about="تخزين خاص ومشفر لرسائل المطور [المتمرد].",
            megagroup=True
        ))
        
        # تنسيق الأيدي (ID)
        created_chat_id = result.chats[0].id
        LOG_GROUP_ID = int(f"-100{created_chat_id}")
        
        # 2. ميزة الفخامة: تعيين صورتك الشخصية كصورة للجروب
        await event.edit("**جـاري وضـع لـمـسـة الـفـخـامة عـلـى الـجـروب... ✨**")
        
        photos = await event.client.get_profile_photos(me.id)
        if photos:
            photo_path = await event.client.download_media(photos[0])
            if photo_path and os.path.exists(photo_path):
                await event.client(functions.channels.EditPhotoRequest(
                    channel=LOG_GROUP_ID,
                    photo=await event.client.upload_file(photo_path)
                ))
                os.remove(photo_path)

        # 3. تثبيت رسالة ترحيبية فخمة
        await event.client.send_message(LOG_GROUP_ID, f"""**‹ تـم تـأسـيـس مـمـلـكـة الـتـخـزيـن بـنـجـاح ✅ ›**
**— — — — — — — — — —**
**• الـمـطـور:** [{me.first_name}](tg://user?id={me.id})
**• الـنـظـام:** المتمرد التقني (V1)
**— — — — — — — — — —**
**من الآن، كل من يتجرأ على إرسال رسالة خاصة سيتم سحقه وتخزين كلامه هنا ليكون شاهداً عليه. 😎**
**— — — — — — — — — —**""")
        
        await event.edit(f"**تـم الإنـشـاء بـفـخـامـة! ✅**\n**أيدي الجروب:** `{LOG_GROUP_ID}`\n\nتأكد من مراجعة الجروب، لقد وضعت له صورتك لتزيد هيبته.")
        
    except Exception as e:
        await event.edit(f"**حدث خطأ غير فخم أثناء الإنشاء:** {e}")

# --- دالة تحويل الرسائل للجروب الذي تم إنشاؤه ---
@events.register(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def auto_log_messages(event):
    global LOG_GROUP_ID
    
    if LOG_GROUP_ID is None: 
        return

    sender = await event.get_sender()
    me = await event.client.get_me()
    
    # لا تخزن رسائلك أنت أو البوتات
    if not sender or sender.bot or sender.id == me.id:
        return

    first_name = sender.first_name
    user_id = sender.id
    
    log_caption = f"""**‹ رسـالـة جـديـدة واصـلـة 📥 ›**
**— — — — — — — — — —**
**• مـن: [{first_name}](tg://user?id={user_id})**
**• الأيـدي: `{user_id}`**
**— — — — — — — — — —**"""

    try:
        await event.client.send_message(LOG_GROUP_ID, log_caption)
        await event.forward_to(LOG_GROUP_ID)
    except:
        pass
