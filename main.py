from telethon import TelegramClient, events, functions, types
from config import API_ID, API_HASH, BOT_TOKEN
from plugins.welcome import start_welcome, start_callbacks
import asyncio

client = TelegramClient('rebel_session', API_ID, API_HASH)
bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

async def setup_logs():
    try:
        dialogs = await client.get_dialogs()
        log_group = next((d for d in dialogs if d.title == "كروب السجل المتمرد"), None)
        
        if not log_group:
            print("[-] جاري إنشاء كروب السجل...")
            # إنشاء الجروب بطريقة مضمونة
            r = await client(functions.messages.CreateChatRequest(
                users=['@BotFather'], 
                title="كروب السجل المتمرد"
            ))
            # الحصول على الأيدي سواء من الرد المباشر أو من التحديثات
            log_id = r.chats[0].id
            await client.send_message(log_id, "🚀 **تم تشغيل سورس المتمرد بنجاح!**\n\nهذا الجروب مخصص لمراقبة السجلات.")
            print(f"✅ تم إنشاء الجروب بنجاح.")
        else:
            await client.send_message(log_group.id, "🔄 **تم إعادة التشغيل..**")
    except Exception as e:
        print(f"⚠️ ملاحظة: {e}")

@client.on(events.NewMessage(incoming=True))
async def handle_welcome(event):
    await start_welcome(event, client)

@bot.on(events.CallbackQuery)
async def handle_callbacks(event):
    await start_callbacks(event, client, bot)

@client.on(events.NewMessage(pattern='.فحص'))
async def ping(event):
    await event.reply("🚀 **سورس المتمرد يعمل بنظام السجلات والأزرار!**")

async def start_all():
    await client.start()
    await setup_logs()
    print("[-] السورس شغال الآن.. تفقد التيليجرام.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_all())
