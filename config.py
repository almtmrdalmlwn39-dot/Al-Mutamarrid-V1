async def time_name_task():
    while True:
        try:
            import pytz
            from datetime import datetime
            from telethon import functions

            # 1. جلب اسمك الحالي بالكامل
            me = await client.get_me()
            full_name = me.first_name

            # 2. جلب وقت صنعاء
            yemen_tz = pytz.timezone('Asia/Aden')
            current_time = datetime.now(yemen_tz).strftime("%I:%M")
            new_time_string = f" | {current_time}"

            # 3. تنظيف الساعة القديمة بدون حذف أي شيء من اسمك
            # نبحث عن مكان آخر علامة " | " ونحذف ما بعدها فقط
            if " | " in full_name:
                # نأخذ كل شيء قبل آخر ظهور للعلامة
                clean_name = full_name.rsplit(" | ", 1)[0]
            else:
                clean_name = full_name

            # 4. تحديث الحساب: اسمك كما هو + الوقت الجديد
            await client(functions.account.UpdateProfileRequest(
                first_name=f"{clean_name}{new_time_string}"
            ))
            
            await asyncio.sleep(300) # تحديث كل 5 دقائق
        except:
            await asyncio.sleep(600)

client.loop.create_task(time_name_task())
