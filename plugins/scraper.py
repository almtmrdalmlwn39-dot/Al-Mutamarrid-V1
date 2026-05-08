import asyncio, random
from telethon import events, functions, types
from telethon.errors import FloodWaitError, UserPrivacyRestrictedError
from main import client, WAR_IDENTITY

# أمر سحب الأعضاء المطور (أقوى وأكثر أماناً)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.سحب (.*)"))
async def advanced_scraping(event):
    input_str = event.pattern_match.group(1)
    await event.edit("**🔄 جـاري بـدء عـمـلـية الـسحب الـخارق...**")
    
    try:
        # جلب المجموعة المستهدفة
        target_group = await client.get_entity(input_str)
        async for user in client.iter_participants(target_group):
            if user.bot: continue # تخطي البوتات لضمان جودة السحب
            
            try:
                # محاولة إضافة العضو للمجموعة الحالية
                await client(functions.channels.InviteToChannelRequest(
                    channel=event.chat_id,
                    users=[user]
                ))
                # فاصل زمني ذكي لحماية الحساب من الحظر
                await asyncio.sleep(random.uniform(2.5, 5.0)) 
                
            except FloodWaitError as e:
                # إذا حدث ضغط كبير، البوت ينتظر تلقائياً
                await event.respond(f"**⚠️ تـنبيه: تـم تـقـييد الـحساب مؤقتاً، سأنتظر `{e.seconds}` ثانية.**")
                await asyncio.sleep(e.seconds)
            except UserPrivacyRestrictedError:
                continue # تخطي المستخدمين الذين يغلقون ميزة الإضافة لخصوصيتهم
            except Exception:
                continue

        await event.edit(f"**✅ تـم إنـهـاء عـمـلـية الـسـحب بـنـجاح!\n\n{WAR_IDENTITY}**")
    except Exception as e:
        await event.edit(f"**❌ حـدث خـطأ فـي الـسحب:** `{e}`")
