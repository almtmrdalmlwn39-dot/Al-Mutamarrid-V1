from telethon import events, Button
from __main__ import client

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    # التأكد أن الرسالة في الخاص فقط لعدم إزعاج المجموعات
    if event.is_private:
        # نص الترحيب الفخم بتنسيق Markdown
        welcome_msg = """
🛡️ **أهلاً بك في سورس المتمرد التقني V1** 🛡️
─── • ⚡️ • ───
أنا بوت المتمرد، صُممت لأخدمك وأحمي خصوصيتك.
استخدم الأزرار أدناه للتحكم بالسورس أو التواصل مع المطور.
─── • ⚡️ • ───
👤 **المطور:** @Vi_ti0
"""
        # إضافة الأزرار الشفافة كما في الصورة
        buttons = [
            [Button.url("📢 قناة السورس", "https://t.me/bedmoddinnow")],
            [Button.url("👨‍💻 مطور السورس", "https://t.me/Vi_ti0")],
            [Button.inline("📜 قائمة الأوامر", data="help_cmd")]
        ]
        
        await event.reply(welcome_msg, buttons=buttons)

# كود إضافي لتشغيل زر "قائمة الأوامر" عند الضغط عليه
@client.on(events.CallbackQuery(data="help_cmd"))
async def help_callback(event):
    await event.answer("يرجى كتابة .اوامري في الشات لرؤية القائمة كاملة!", alert=True)
