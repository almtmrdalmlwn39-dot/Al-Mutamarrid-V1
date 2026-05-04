from telethon import events
# ضروري جداً عشان الملف الفرعي يعرف السورس الرئيسي
from __main__ import client 

@client.on(events.NewMessage(pattern=r"\.(اوامري|الاوامر|اوامر)$", outgoing=True))
async def help_menu(event):
    help_text = """
🛡️ **سـورس الـمـتمـرد الـتـقـنـي V1** 🛡️
─── • ⚡️ • ───
🚀 **[ الـفـحـص والـسرعـة ]**
• `.بينج` : قياس سرعة الاستجابة.
• `.وقت` : الوقت والتاريخ في اليمن.

💀 **[ الأوامـر والـحمـايـة ]**
• `.كشف` : معلومات الحساب.
• `.حماية تفعيل/تعطيل` : درع الخاص.

🎮 **[ الـتـسـلـيـة ]**
• `.نكته` | `.لو خيروك`
─── • ⚡️ • ───
👤 **المـطـور:** @Vi_ti0
"""
    try:
        await event.edit(help_text)
    except Exception as e:
        print(f"Error in help menu: {e}")
