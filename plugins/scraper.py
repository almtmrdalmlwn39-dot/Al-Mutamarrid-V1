import csv
import asyncio
import os
from telethon import events
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import ChannelParticipantsSearch, UserStatusOnline, UserStatusRecent
from telethon.errors import FloodWaitError, UserAlreadyParticipantError

# لضمان ربط الدالة بالكلينت الرئيسي المسمى client في main.py
from main import client

# قائمة الحروف والأرقام الذكية للالتفاف على رادار التليجرام
SEARCH_QUERIES = [
    'ا', 'ب', 'ت', 'ج', 'ح', 'خ', 'د', 'ر', 'ز', 'س', 'ش', 'ص', 'ط', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'هـ', 'و', 'ي',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
]

# قائمة الأيديهات المسموح لها باستخدام السحب (المطورين الذين رفعتهم)
SUDO_USERS = [8735360084, 6895436017, 5445178068]

# الهاندلر مضبوط على الكلينت الصحيح ومفتوح لاستقبال رسائل المطورين (incoming=True)
@client.on(events.NewMessage(incoming=True, pattern=r"\.(سحب|scr)(.*)"))
@client.on(events.NewMessage(outgoing=True, pattern=r"\.(سحب|scr)(.*)"))
async def advanced_scraper(event):
    # التحقق من الصلاحية: إذا لم تكن أنت المالك ولم يكن المرسل من المطورين يتجاهل الأمر
    if not event.out and event.sender_id not in SUDO_USERS:
        return

    input_text = event.pattern_match.group(2).strip()
    
    if not input_text:
        await event.reply("**🚸 يرجى كتابة يوزر أو رابط القروب بعد الأمر. مثال:\n`.سحب معرف_القروب`**")
        return

    # محاولة حذف أمر المطور لتنظيف الشات
    try:
        await event.delete()
    except:
        pass

    progress_msg = await event.respond("**🔍 جاري فحص الرابط والاتصال بسيرفرات تليجرام...**")
    
    # استخدام كلينت السورس النشط
    active_client = event.client
    target_group = None

    # معالجة الروابط الخاصة (المحمية) والعامة
    try:
        if 't.me/' in input_text or 'telegram.me/' in input_text:
            link_parts = input_text.split('/')[-1]
            if link_parts.startswith('+'):
                link_parts = link_parts[1:]
                
            try:
                updates = await active_client(ImportChatInviteRequest(link_parts))
                target_group = updates.chats[0]
            except UserAlreadyParticipantError:
                target_group = await active_client.get_entity(input_text)
            except Exception:
                target_group = await active_client.get_entity(input_text)
        else:
            target_group = await active_client.get_entity(input_text)
            
    except Exception as e:
        await progress_msg.edit(f"**❌ تعذر الوصول للقروب المستهدف عبر السيرفر.**\nالسبب: `{e}`\n💡 تأكد أن الحساب منضم للقروب إذا كان خاصاً.")
        return

    if not target_group:
        await progress_msg.edit("**❌ فشل تحديد الكيان البرمجي للقروب.**")
        return

    await progress_msg.edit(f"**📥 جاري سحب أعضاء: ( {target_group.title} )**\n🔥 يتم الآن تشغيل خوارزمية السحب المجهري بالحروف...")

    all_participants = []
    seen_users = set()
    limit = 50

    for query in SEARCH_QUERIES:
        offset = 0
        while True:
            try:
                participants = await active_client(GetParticipantsRequest(
                    channel=target_group,
                    filter=ChannelParticipantsSearch(query),
                    offset=offset,
                    limit=limit,
                    hash=0
                ))
            except FloodWaitError as e:
                await event.respond(f"⚠️ السيرفر واجه قيوداً مؤقتة! سيتوقف السحب تلقائياً لـ `{e.seconds}` ثانية.")
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

    file_name = f"members_{target_group.id}.csv"
    
    try:
        with open(file_name, "w", encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow(['ID', 'Username', 'Access Hash', 'First Name', 'Last Name'])
            for user in all_participants:
                username = user.username if user.username else ""
                first_name = user.first_name if user.first_name else ""
                last_name = user.last_name if user.last_name else ""
                writer.writerow([user.id, username, user.access_hash, first_name, last_name])
                
        await active_client.send_file(
            event.chat_id,
            file_name,
            caption=f"✅ **اكتمل السحب الخارق بنجاح!**\n\n👥 **اسم القروب:** {target_group.title}\n📊 **إجمالي الأعضاء الحقيقيين:** `{len(all_participants)}`\n⚙️ **تمت العملية بنجاح لصالح المطورين.**"
        )
        
        await progress_msg.delete()
        if os.path.exists(file_name):
            os.remove(file_name)

    except Exception as e:
        await event.respond(f"❌ حدث خطأ أثناء توليد ملف البيانات: `{e}`")
