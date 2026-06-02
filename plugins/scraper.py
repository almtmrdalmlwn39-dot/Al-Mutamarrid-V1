import csv
import asyncio
import os
from telethon import events
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch, UserStatusOnline, UserStatusRecent
from telethon.errors import FloodWaitError

# قائمة الحروف والأرقام الذكية للالتفاف على رادار التليجرام
SEARCH_QUERIES = [
    'ا', 'ب', 'ت', 'ج', 'ح', 'خ', 'د', 'ر', 'ز', 'س', 'ش', 'ص', 'ط', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'هـ', 'و', 'ي',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
]

# قائمة الأيديهات المسموح لها باستخدام السحب (أنت والمطورين الذين رفعتهم)
SUDO_USERS = [8735360084, 6895436017, 5445178068]

@events.register(events.NewMessage(pattern=r"\.(سحب|scr)(.*)"))
async def advanced_scraper(event):
    # التحقق من الصلاحية: يسمح لك أو لأي مطور مضاف في القائمة
    if not event.out and event.sender_id not in SUDO_USERS:
        return

    # أخذ المعرف أو الرابط المكتوب بعد الأمر
    input_text = event.pattern_match.group(2).strip()
    
    if not input_text:
        await event.reply("**🚸 يرجى كتابة يوزر القروب بعد الأمر. مثال:\n`.سحب معرف_القروب`**")
        return

    # حذف أمر المطور لتنظيف الشات
    try:
        await event.delete()
    except:
        pass

    # إرسال رسالة بدء العملية
    progress_msg = await event.respond("**🔍 جاري فحص القروب المستهدف والاتصال بالسيرفر...**")
    
    # تنظيف الرابط إذا تم إدخاله كاملاً
    if '/' in input_text:
        input_text = input_text.split('/')[-1]

    # السر هنا: استخدام الكلينت الخاص بالشخص الذي أرسل الرسالة لتفادي قيود الحساب الأصلي
    active_client = event.client

    try:
        target_group = await active_client.get_entity(input_text)
    except Exception as e:
        await progress_msg.edit(f"**❌ تعذر الوصول للقروب المستهدف عبر هذا الحساب.**\nالسبب: `{e}`")
        return

    await progress_msg.edit(f"**📥 جاري سحب أعضاء: ( {target_group.title} )**\n🔥 يتم السحب الآن عبر حساب المطور مباشرة لتفادي قيود الحسابات الأخرى...")

    all_participants = []
    seen_users = set()
    limit = 50

    for query in SEARCH_QUERIES:
        offset = 0
        while True:
            try:
                # تنفيذ الطلب عبر الكلينت النشط (حساب الشخص المطور الحالي)
                participants = await active_client(GetParticipantsRequest(
                    channel=target_group,
                    filter=ChannelParticipantsSearch(query),
                    offset=offset,
                    limit=limit,
                    hash=0
                ))
            except FloodWaitError as e:
                await event.respond(f"⚠️ الحساب الحالي واجه قيوداً مؤقتة! سيتوقف السحب لـ `{e.seconds}` ثانية.")
                await asyncio.sleep(e.seconds + 2)
                continue
            except Exception as e:
                break

            if not participants.users:
                break

            for user in participants.users:
                if user.bot:
                    continue
                if user.id not in seen_users:
                    if isinstance(user.status, (UserStatusOnline, UserStatusRecent)):
                        all_participants.append(user)
                        seen_users.add(user.id)

            offset += len(participants.users)
            if len(participants.users) < limit:
                break
            await asyncio.sleep(1.5)
        await asyncio.sleep(0.5)

    if not all_participants:
        await progress_msg.edit("**❌ لم يتم العثور على أعضاء متفاعلين يتطابقون مع الفلتر أو أن قائمة الأعضاء مخفية!**")
        return

    file_name = f"members_{input_text}.csv"
    
    try:
        with open(file_name, "w", encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow(['ID', 'Username', 'Access Hash', 'First Name', 'Last Name'])
            for user in all_participants:
                username = user.username if user.username else ""
                first_name = user.first_name if user.first_name else ""
                last_name = user.last_name if user.last_name else ""
                writer.writerow([user.id, username, user.access_hash, first_name, last_name])
                
        # إرسال الملف باستخدام الكلينت النشط
        await active_client.send_file(
            event.chat_id,
            file_name,
            caption=f"✅ **اكتمل السحب الخارق بنجاح!**\n\n👥 **اسم القروب:** {target_group.title}\n📊 **إجمالي الأعضاء:** `{len(all_participants)}`\n⚙️ **تم التنفيذ بنجاح عبر صلاحيات المطور الحالي.**"
        )
        
        await progress_msg.delete()
        if os.path.exists(file_name):
            os.remove(file_name)

    except Exception as e:
        await event.respond(f"❌ حدث خطأ أثناء توليد ملف البيانات: `{e}`")

# ربط الدالة بالسيرفر تلقائياً
if 'rebel' in globals():
    rebel.add_event_handler(advanced_scraper)
elif 'bot' in globals():
    bot.add_event_handler(advanced_scraper)
