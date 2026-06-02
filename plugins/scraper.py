import csv
import asyncio
import os
from telethon import events
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch, UserStatusOnline, UserStatusRecent
from telethon.errors import FloodWaitError

# قائمة الحروف والأرقام الذكية للالتفاف على رادار التليجرام (تفادي القيود 100%)
SEARCH_QUERIES = [
    'ا', 'ب', 'ت', 'ج', 'ح', 'خ', 'د', 'ر', 'ز', 'س', 'ش', 'ص', 'ط', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'هـ', 'و', 'ي',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
]

# تفعيل الأمر عند كتابة (.سحب) أو (.scr) في التليجرام
# تنبيه: إذا كان السورس الخاص بك يستخدم اسم كلينت آخر غير (bot) مثل (rebel) قم بتغييره هنا
@bot.on(events.NewMessage(pattern=r"\.(سحب|scr)(.*)"))
async def advanced_scraper(event):
    # التحقق من أنك أنت المالك أو المطور (SUDO)
    if not event.out:
        return

    # أخذ المعرف أو الرابط المكتوب بعد الأمر
    input_text = event.pattern_match.group(2).strip()
    
    if not input_text:
        await event.edit("**🚸 يرجى كتابة يوزر القروب بعد الأمر. مثال:\n`.سحب معرف_القروب`**")
        return

    await event.edit("**🔍 جاري فحص القروب المستهدف والاتصال بالسيرفر...**")
    
    # تنظيف الرابط إذا تم إدخاله كاملاً
    if '/' in input_text:
        input_text = input_text.split('/')[-1]

    try:
        target_group = await event.client.get_entity(input_text)
    except Exception as e:
        await event.edit(f"**❌ تعذر الوصول للقروب المستهدف.**\nالسبب: `{e}`")
        return

    await event.edit(f"**📥 جاري سحب أعضاء: ( {target_group.title} )**\n🔥 تم تفعيل خوارزمية السحب المجهري بالحروف لمنع التقييد الحساب...")

    all_participants = []
    seen_users = set() # لمنع التكرار الناتجة عن البحث بالحروف
    limit = 50  # دفعات صغيرة ومستقرة جداً لتفادي رادار الـ Flood

    # بدء السحب الذكي عبر التناوب على الحروف
    for query in SEARCH_QUERIES:
        offset = 0
        while True:
            try:
                participants = await event.client(GetParticipantsRequest(
                    channel=target_group,
                    filter=ChannelParticipantsSearch(query),
                    offset=offset,
                    limit=limit,
                    hash=0
                ))
            except FloodWaitError as e:
                # حماية الحساب الفائقة في حال ضغط السيرفر
                await event.respond(f"⚠️ تليجرام طلب تهدئة السرعة! سيتوقف السحب تلقائياً لـ `{e.seconds}` ثانية للحفاظ على الحساب.")
                await asyncio.sleep(e.seconds + 2)
                continue
            except Exception as e:
                break

            if not participants.users:
                break

            for user in participants.users:
                if user.bot: # تخطي البوتات تلقائياً
                    continue
                
                # التحقق من عدم تكرار العضو ومن حالته (المتفاعلين فقط)
                if user.id not in seen_users:
                    if isinstance(user.status, (UserStatusOnline, UserStatusRecent)):
                        all_participants.append(user)
                        seen_users.add(user.id)

            offset += len(participants.users)
            
            # إذا كانت الدفعة أقل من الليميت يعني انتهت حسابات هذا الحرف
            if len(participants.users) < limit:
                break
                
            # فاصل زمني آمن جداً بين الدفعات للحرف الواحد
            await asyncio.sleep(1.5)

        # فاصل زمني بسيط عند الانتقال من حرف إلى حرف آخر لراحة الحساب
        await asyncio.sleep(0.5)

    if not all_participants:
        await event.edit("**❌ لم يتم العثور على أعضاء متفاعلين يتطابقون مع الفلتر أو أن قائمة الأعضاء مخفية!**")
        return

    # حفظ اللستة النظيفة في ملف CSV داخل مجلد السورس
    file_name = f"members_{input_text}.csv"
    
    try:
        with open(file_name, "w", encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            # كتابة العناوين وتخزين الـ Access Hash لضمان نجاح الإضافة بدون أخطاء Peer
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
            caption=f"✅ **اكتمل السحب الخارق بنجاح وبدون تقييد!**\n\n👥 **اسم القروب:** {target_group.title}\n📊 **إجمالي الأعضاء الحقيقيين والمتفاعلين:** `{len(all_participants)}`\n⚙️ **اللستة مفلترة وجاهزة تماماً للإضافة.**"
        )
        
        # حذف الملف مؤقتاً من السيرفر بعد إرساله للحفاظ على المساحة
        if os.path.exists(file_name):
            os.remove(file_name)

    except Exception as e:
        await event.respond(f"❌ حدث خطأ أثناء توليد ملف البيانات: `{e}`")
