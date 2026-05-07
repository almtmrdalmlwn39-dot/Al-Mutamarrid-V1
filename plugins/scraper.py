from main import client, CMD_HELP # استيراد المحرك والقاموس لضمان الاتصال
from telethon import events, functions, errors
import asyncio

# تسجيل الحزمة لكي تظهر في قائمة .الاوامر تلقائياً
CMD_HELP["السحب والاضافة"] = ["سحب"]

@client.on(events.NewMessage(outgoing=True, pattern=r"\.سحب (.*)"))
async def scrap_members(event):
    target = event.pattern_match.group(1).strip()
    if not target:
        return await event.edit("**⚠️ حدد معرف القروب**")
    
    await event.edit("**🛡️ جاري محاولة الوصول للمصدر..**")
    
    try:
        source_chat = await client.get_entity(target)
        # جلب الأعضاء (حددت لك ليميت 100 لتجنب الحظر السريع)
        users_list = await client.get_participants(source_chat, limit=100)
        
        count = 0
        await event.edit(f"**🚀 بدأت الإضافة إلى المجموعة الحالية..**")
        
        for user in users_list:
            if user.bot or user.deleted: continue
            try:
                # محاولة الإضافة المباشرة
                await client(functions.channels.InviteToChannelRequest(event.chat_id, [user.id]))
                count += 1
                # تأخير 2 ثانية ضروري جداً لكي لا ينحظر حسابك
                await asyncio.sleep(2) 
            except errors.FloodWaitError as e:
                # إذا طلب التليجرام الانتظار، يتوقف البوت تلقائياً
                await event.respond(f"**⚠️ توقف السحب مؤقتاً بسبب قيود التليجرام: انتظر {e.seconds} ثانية.**")
                break
            except: 
                continue
        
        await event.respond(f"**✅ انتهى السحب.**\n**- تم إضافة: `{count}` عضو بنجاح.**\n`المتمرد التقني مر من هنا 🦅`")
        
    except Exception as e:
        # معالجة خطأ "Entity" إذا كان المعرف غلط
        await event.edit(f"**❌ خطأ: لم يتم العثور على القروب أو أنك لست عضواً فيه.**")
