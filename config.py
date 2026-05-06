async def time_name_task():
    while True:
        try:
            import pytz
            from datetime import datetime
            
            # 1. جلب معلومات حسابك الحالية
            me = await client.get_me()
            # سحب الاسم الحالي (بدون الوقت القديم)
            # نفترض أنك تفصل بين اسمك والوقت بـ "|"
            current_full_name = me.first_name
            if " | " in current_full_name:
                base_name = current_full_name.split(" | ")[0]
            else:
                base_name = current_full_name

            # 2. ضبط توقيت صنعاء
            yemen_tz = pytz.timezone('Asia/Aden')
            current_time = datetime.now(yemen_tz).strftime("%I:%M")
            
            # 3. تحديث الحساب بالاسم الذي اخترته أنت + الوقت
            await client(functions.account.UpdateProfileRequest(
                first_name=f"{base_name} | {current_time}"
            ))
            
            await asyncio.sleep(300) # تحديث كل 5 دقائق
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(600)

client.loop.create_task(time_name_task())
