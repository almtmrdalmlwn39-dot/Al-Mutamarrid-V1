import csv
import asyncio
import os
from telethon import events
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch, UserStatusOnline, UserStatusRecent
from telethon.errors import FloodWaitError

# تفعيل الأمر عند كتابة (.سحب) أو (.scr) في التليجرام
@bot.on(events.NewMessage(pattern=r"\.(سحب|scr)(.*)"))
async def advanced_scraper(event):
    # التحقق من أنك أنت المالك أو "SUDO"
    if not event.out:
        return

    # أخذ المعرف أو الرابط المكتوب بعد الأمر
    input_text = event.pattern_match.group(2).strip()
    
    if not input_text:
        await event.edit("**🚸 يرجى كتابة يوزر القروب بعد الأمر. مثال:\n`.سحب معرف_القروب`**")
        return

    await event.edit("**🔍 جاري فحص القروب والاتصال بقاعدة البيانات...**")
    
    # تنظيف الرابط إذا تم إدخاله كاملاً
    if '/' in input_text:
        input_text = input_text.split('/')[-1]

    try:
        target_group = await event.client.get_entity(input_text)
    except Exception as e:
        await event.edit(f"**❌ تعذر الوصول للقروب المستهدف.**\nالسبب: `{e}`")
        return

    await event.edit(f"**📥 جاري سحب أعضاء: ( {target_group.title} )**\n⚡ يتم الآن تشغيل الفلتر الذكي المدفوع ضد الحظر...")

    all_participants = []
    offset = 0
    limit = 100  # دفعة آمنة ومستقرة جداً

    while True:
        try:
            participants = await event.client(GetParticipantsRequest(
                channel=target_group,
                filter=ChannelParticipantsSearch(''),
                offset=offset,
                limit=limit,
                hash=0
            ))
        except FloodWaitError as e:
            # حماية ذكية لتجنب تبنيد حسابك أثناء السحب
            await event.respond(f"⚠️ تليجرام يفرض قيوداً مؤقتة! سيتوقف السحب تلقائياً لـ `{e.seconds}` ثانية للحفاظ على الحساب.")
            await asyncio.sleep(e.seconds + 2)
            continue
        except Exception as e:
            break

        if not participants.users:
            break

        for user in participants.users:
            if user.bot: # تخطي البوتات تلقائياً
                continue
            
            # فلتر السورسات المدفوعة: سحب الأعضاء المتفاعلين (أونلاين أو تواجدوا مؤخراً) لضمان جودة اللستة
            if isinstance(user.status, (UserStatusOnline, UserStatusRecent)):
                all_participants.append(user)

        offset += len(participants.users)
        # فاصل زمني متغير (تلقائي) لمنع رادارات الحماية في تليجرام من كشف السحب السريع
        await asyncio.sleep(1.2)

    # حفظ اللستة في ملف CSV داخل مجلد السورس
    file_name = f"members_{input_text}.csv"
    
    try:
        with open(file_name, "w", encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            # كتابة العناوين وتخزين الـ Access Hash وهو السر لمنع أخطاء الإضافة لاحقاً
            writer.writerow(['ID', 'Username', 'Access Hash', 'First Name', 'Last Name'])
            
            for user in all_participants:
                username = user.username if user.username else ""
                first_name = user.first_name if user.first_name else ""
                last_name = user.last_name if user.last_name else ""
                writer.writerow([user.id, username, user.access_hash, first_name, last_name])
                
        # إرسال ملف الأعضاء الجاهز مباشرة إلى المحادثة
        await event.client.send_file(
            event.chat_id,
            file_name,
            caption=f"✅ **اكتمل السحب بنجاح بمواصفات مدفوعة!**\n\n👥 **اسم القروب:** {target_group.title}\n📊 **إجمالي الأعضاء المتفاعلين:** `{len(all_participants)}`\n⚙️ **الملف جاهز للإضافة الآن.**"
        )
        
        # حذف الملف مؤقتاً من السيرفر بعد إرساله للحفاظ على المساحة
        if os.path.exists(file_name):
            os.remove(file_name)

    except Exception as e:
        await event.respond(f"❌ حدث خطأ أثناء توليد ملف البيانات: `{e}`")
