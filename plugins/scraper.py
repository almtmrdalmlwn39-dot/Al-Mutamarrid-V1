import csv
import asyncio
import os
from telethon import events
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import ChannelParticipantsSearch, UserStatusOnline, UserStatusRecent
from telethon.errors import FloodWaitError, UserAlreadyParticipantError

# استدعاء الكلينت مباشرة من الماين
from main import client

# قائمة الأيديهات الثابتة للمطورين المساعدين (SUDO)
SUDO_USERS = [8735360084, 6895436017, 5445178068]

# الحروف الذكية للالتفاف على رادار التليجرام منعاً للتقييد
SEARCH_QUERIES = [
    'ا', 'ب', 'ت', 'ج', 'ح', 'خ', 'د', 'ر', 'ز', 'س', 'ش', 'ص', 'ط', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'هـ', 'و', 'ي',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
]

# ربط الأمر مباشرة بالكلينت للرسائل الواردة والصادرة
@client.on(events.NewMessage(pattern=r"\.(سحب|scr)(.*)"))
async def advanced_scraper(event):
    # السماح لمالك الحساب الأساسي أو أي مطور مضاف في القائمة
    sender_id = event.sender_id
    if not event.out and sender_id not in SUDO_USERS:
        return

    try:
        input_text = event.pattern_match.group(2).strip()
    except Exception:
        return
    
    if not input_text:
        await event.reply("**🚸 يرجى كتابة يوزر أو رابط القروب بعد الأمر. مثال:\n`.سحب معرف_القروب`**")
        return

    # حذف أمر المطور فوراً لتنظيف الشات
    try:
        await event.delete()
    except:
        pass

    # إرسال رسالة بدء الفحص لتأكيد الاستجابة
    progress_msg = await event.respond("**🔍 [منظومة المتمرد] جاري فحص الرابط والاتصال بالسيرفر...**")
    target_group = None

    try:
        # معالجة الروابط
        if 't.me/' in input_text or 'telegram.me/' in input_text:
            link_parts = input_text.split('/')[-1]
            if link_parts.startswith('+'):
                link_parts = link_parts[1:]
                
            try:
                updates = await client(ImportChatInviteRequest(link_parts))
                target_group = updates.chats[0]
            except UserAlreadyParticipantError:
                target_group = await client.get_entity(input_text)
            except Exception:
                target_group = await client.get_entity(input_text)
        else:
            target_group = await client.get_entity(input_text)
            
    except Exception as e:
        await progress_msg.edit(f"**❌ تعذر الوصول للقروب المستهدف.**\nالسبب: `{e}`")
        return

    if not target_group:
        await progress_msg.edit("**❌ فشل تحديد الكيان البرمجي للقروب.**")
        return

    await progress_msg.edit(f"**📥 جاري سحب أعضاء: ( {target_group.title} )**\n🔥 تم التحقق من الصلاحية وجاري جمع البيانات...")

    all_participants = []
    seen_users = set()
    limit = 50

    for query in SEARCH_QUERIES:
        offset = 0
        while True:
            try:
                participants = await client(GetParticipantsRequest(
                    channel=target_group,
                    filter=ChannelParticipantsSearch(query),
                    offset=offset,
                    limit=limit,
                    hash=0
                ))
            except FloodWaitError as e:
                await event.respond(f"⚠️ طلب التهدئة! سيتوقف السحب لـ `{e.seconds}` ثانية لحماية الحساب.")
                await asyncio.sleep(e.seconds + 2)
                continue
            except Exception:
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
            await asyncio.sleep(1.2)
        await asyncio.sleep(0.3)

    if not all_participants:
        await progress_msg.edit("**❌ قائمة أعضاء هذا القروب مخفية تماماً أو لا يوجد أعضاء متفاعلين!**")
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
                
        await client.send_file(
            event.chat_id,
            file_name,
            caption=f"✅ **اكتمل السحب بنجاح!**\n\n👥 **القروب:** {target_group.title}\n📊 **العدد:** `{len(all_participants)}`"
        )
        
        await progress_msg.delete()
        if os.path.exists(file_name):
            os.remove(file_name)

    except Exception as e:
        await event.respond(f"❌ حدث خطأ أثناء توليد ملف البيانات: `{e}`")
