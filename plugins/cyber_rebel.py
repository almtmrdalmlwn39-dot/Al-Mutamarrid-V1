import asyncio, random
from telethon import events
# تم تغيير الاستيراد لضمان الربط الصحيح بالمحرك الرئيسي
from main import client, CMD_HELP

# هوية المتمرد التقني السيبرانية
CYBER_IDENTITY = "**- الـنـظام تـحت الـسيطرة.. الـمتمرد الـتقني 🏴‍☠️**"

# إضافة القسم لقائمة الأوامر العامة بستايل زدثون
CMD_HELP.update({
    "الترسانة السيبرانية": [
        "قرصنة", "تشفير_آلي", "مصفوفة", "تحذير"
    ]
})

# 1. أمر الاختراق السيبراني (تم تحسين التوقيت للواقعية)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.قرصنة"))
async def cyber_attack(event):
    frames = [
        "**[📡] جـاري فـحص الـثغرات...**",
        "**[🔓] تـم اسـتغلال ثـغرة SQL Injection...**",
        "**[💉] جـاري حـقن الـأكواد الـخبيثة...**",
        "**[💾] تـم الـوصول لـقواعد الـبيانات...**",
        "**[📸] تـم فـتح الـكاميرا والـميكروفون...**",
        "**[💀] الـجهاز الآن تـحت سـيطرة الـمتمرد!**"
    ]
    for frame in frames:
        await event.edit(frame)
        await asyncio.sleep(1.2)

# 2. أمر "التشفير الآلي" (تم إصلاح خطأ النص الفارغ)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تشفير_آلي"))
async def binary_convert(event):
    if " " not in event.text:
        return await event.edit("**⚠️ يرجى كتابة نص بعد الأمر.. مثال: `.تشفير_آلي المتمرد`**")
    
    input_text = event.text.split(" ", 1)[1]
    binary_text = ''.join(format(ord(i), '08b') for i in input_text)
    # تقليص النص لضمان عدم تجاوز حدود رسائل تليجرام
    await event.edit(f"**🔐 الـرسالة الـمشفرة :**\n`{binary_text[:200]}...` \n\n**{CYBER_IDENTITY}**")

# 3. أمر "المصفوفة" (تم إضافة رموز تقنية جديدة للفخامة)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.مصفوفة"))
async def matrix_effect(event):
    matrix_chars = ["0", "1", "α", "β", "X", "Y", "7", "Z"]
    for i in range(12):
        line = "".join(random.choice(matrix_chars) for _ in range(20))
        await event.edit(f"**`{line}`\n`{line[::-1]}`\n`{line}`**")
        await asyncio.sleep(0.2)
    await event.edit("**- تـم اخـتراق الـواقع بنـجاح 🕶️ | AL-MUTAMARRID**")

# 4. أمر "تحذير أمني" (تغيير الآي-بي لجعله يبدو خارجياً ومرعباً أكثر)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تحذير"))
async def security_alert(event):
    alert_msg = (
        "**⚠️ تـنبيه أمـني عـالي الـخطورة !**\n"
        "**— — — — — — — — — —**\n"
        "**🔴 تـم رصـد مـحاولة دخـول غـير مـصرح لـحسابك.**\n"
        "**🌐 الآيـدي الـمهاجم: `152.12.0.94`**\n"
        "**📍 الـموقع: سـيرفرات الـمتمرد الـتقني.**\n"
        "**— — — — — — — — — —**\n"
        "**تـم حـجب الـهجوم بـنجاح بواسطة المتمرد 🛡️**"
    )
    await event.edit(alert_msg)
