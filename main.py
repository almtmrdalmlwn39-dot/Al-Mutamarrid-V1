# --- [ إضافات المتمرد الاحترافية ] ---

# 1. أمر الوقت والسرعة المدمج (بدون تغيير الاسم)
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.حالة_السورس$"))
async def status_check(event):
    # حساب السرعة
    start = datetime.now()
    await client(functions.PingRequest(ping_id=0))
    ms = (datetime.now() - start).microseconds / 1000
    
    # جلب الوقت بزخرفة فخمة
    nums = {'0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵'}
    time_now = datetime.now(YEMEN_TZ).strftime("%I:%M")
    fancy_time = "".join(nums.get(c, c) for c in time_now)
    
    await event.edit(
        f"**🚀 نـظام الـمتمرد يـعمل بـكفاءة:**\n"
        f"**— — — — — — — — — —**\n"
        f"**⌚ الـوقت الآن : `{fancy_time}`**\n"
        f"**⚡ الـسرعة : `{ms}` ms**\n"
        f"**🛡️ الـحماية : نـشطة ✅**\n"
        f"**— — — — — — — — — —**\n"
        f"{CYBER_IDENTITY}"
    )

# 2. ميزة التفاعل التلقائي (محاكاة البريميوم)
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def premium_react(event):
    if event.sender_id in approved_users:
        try:
            await event.react("🔥") # يتفاعل بنار لو الشخص مسموح له
        except: pass

# 3. أمر كشف معلومات الحساب العميق
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.كشف$"))
async def who_is(event):
    if not event.is_reply:
        return await event.edit("**⚠️ رد عـلى رسـالة الـشخص أولاً!**")
    
    await event.edit("**🔍 جـاري سـحب الـبيانات...**")
    reply = await event.get_reply_message()
    user = await client.get_entity(reply.sender_id)
    
    info = (
        f"**👤 بـيانات الـمستهدف:**\n"
        f"**— — — — — — — — — —**\n"
        f"**- الاسـم:** {user.first_name}\n"
        f"**- الأيـدي:** `{user.id}`\n"
        f"**- الـرابط:** [اضـغط هـنا](tg://user?id={user.id})\n"
        f"**— — — — — — — — — —**\n"
        f"{CYBER_IDENTITY}"
    )
    await event.edit(info)

# 4. منع "جاري الكتابة" عند قراءة الرسائل (Ghost Mode)
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def ghost_reading(event):
    await client.send_read_acknowledge(event.chat_id, event.message) # يقرأ بدون ما يظهر للطرف الثاني
