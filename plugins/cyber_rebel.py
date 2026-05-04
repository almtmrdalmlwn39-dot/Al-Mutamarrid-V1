import asyncio, random
from telethon import events
from __main__ import client 

# هوية الهكر السيبراني
CYBER_IDENTITY = "**- الـنـظام تـحت الـسيطرة.. الـمتمرد الـتقني 🏴‍☠️**"

# 1. أمر الاختراق السيبراني
@client.on(events.NewMessage(outgoing=True, pattern=r"\.قرصنة"))
async def cyber_attack(event):
    frames = [
        "**[📡] جـاري فـحص الـثغرات...**",
        "**[🔓] تـم اسـتغلال ثـغرة SQL Injection...**",
        "**[💉] جـاري حـحقن الـأكواد الـخبيثة...**",
        "**[💾] تـم الـوصول لـقواعد الـبيانات...**",
        "**[📸] تـم فـتح الـكاميرا والـميكروفون...**",
        "**[💀] الـجهاز الآن تـحت سـيطرة الـمتمرد!**"
    ]
    for frame in frames:
        await event.edit(frame)
        await asyncio.sleep(1)

# 2. أمر "التشفير الآلي"
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تشفير_آلي"))
async def binary_convert(event):
    input_text = event.text.split(" ", 1)[1] if " " in event.text else "The Rebel"
    binary_text = ''.join(format(ord(i), '08b') for i in input_text)
    await event.edit(f"**🔐 الـرسالة الـمشفرة :**\n`{binary_text[:100]}...` \n\n**{CYBER_IDENTITY}**")

# 3. أمر "المصفوفة" (Matrix)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.مصفوفة"))
async def matrix_effect(event):
    matrix = ["0", "1"]
    for i in range(10):
        line = "".join(random.choice(matrix) for _ in range(15))
        await event.edit(f"**`{line}`\n`{line[::-1]}`\n`{line}`**")
        await asyncio.sleep(0.3)
    await event.edit("**- تـم اخـتراق الـواقع بنـجاح 🕶️**")

# 4. أمر "تحذير أمني"
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تحذير"))
async def security_alert(event):
    alert_msg = (
        "**⚠️ تـنبيه أمـني عـالي الـخطورة !**\n"
        "**— — — — — — — — — —**\n"
        "**🔴 تـم رصـد مـحاولة دخـول غـير مـصرح لـحسابك.**\n"
        "**🌐 الآيـدي الـمهاجم: `192.168.1.1`**\n"
        "**📍 الـموقع: سـيرفرات الـمتمرد الـتقني.**\n"
        "**— — — — — — — — — —**\n"
        "**تـم حـجب الـهجوم بـنجاح 🛡️**"
    )
    await event.edit(alert_msg)

# --- [ قسم استعراض أوامر الترسانة السيبرانية ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اوامر_السيبراني"))
async def cyber_help(event):
    help_text = (
        "**🏴‍☠️ قـائمة أدوات الـهيبة والـسيبراني :**\n"
        "**— — — — — — — — — —**\n"
        "**⚡ | `.قرصنة` :** تـمثيل عـملية اخـتراق كـاملة.\n"
        "**🔐 | `.تشفير_آلي` :** تـحويل الـنص لـلغة (0101).\n"
        "**📟 | `.مصفوفة` :** تـأثير أرقـام الـهكر الـمتحركة.\n"
        "**⚠️ | `.تحذير` :** إرسـال تـنبيه أمـني وهـمي مرعب.\n"
        "**— — — — — — — — — —**\n"
        f"{CYBER_IDENTITY}"
    )
    await event.edit(help_text)
