import asyncio, random
from telethon import events
from main import client, CMD_HELP

# --- [ AL-MUTAMARRID CYBER IDENTITY ] ---
# الهوية الإنجليزية العريضة (بصمة المتمرد العالمية)
CYBER_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🏴‍☠️**"

# إضافة القسم للقائمة الملكية
CMD_HELP.update({
    "الترسانة السيبرانية": [
        "قرصنة", "تشفير_آلي", "مصفوفة", "تحذير"
    ]
})

# 1. أمر الاختراق السيبراني (نصوص عربية مع بصمة إنجليزية)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.قرصنة"))
async def cyber_attack(event):
    frames = [
        "**[📡] جـاري فـحص ثـغرات الـشبكة...**",
        "**[🔓] تـم اخـتراق الـقاعدة بـنجاح...**",
        "**[💉] جـاري حـقن الـأكواد الـخبيثة...**",
        "**[💾] تـم الـوصول لـسجلات الـبيانات...**",
        "**[📸] تـم تـفعيل الـكاميرا عـن بـعد...**",
        f"**[💀] الـنظام الآن تـحت سـيطرة الـمتمرد!**\n\n{CYBER_IDENTITY}"
    ]
    for frame in frames:
        await event.edit(frame)
        await asyncio.sleep(1.2)

# 2. أمر "التشفير الآلي"
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تشفير_آلي"))
async def binary_convert(event):
    if " " not in event.text:
        return await event.edit("**⚠️ يرجى كتابة نص لتشفيره.. مثال: `.تشفير_آلي المتمرد`**")
    
    input_text = event.text.split(" ", 1)[1]
    binary_text = ''.join(format(ord(i), '08b') for i in input_text)
    
    await event.edit(f"**🔐 الـرسالة الـمشفرة بنجاح :**\n\n`{binary_text[:200]}...` \n\n{CYBER_IDENTITY}")

# 3. أمر "المصفوفة" (أرقام هكر متحركة)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.مصفوفة"))
async def matrix_effect(event):
    matrix = ["0", "1", "α", "β", "X", "Y"]
    for i in range(12):
        line = "".join(random.choice(matrix) for _ in range(20))
        await event.edit(f"**`{line}`\n`{line[::-1]}`\n`{line}`**")
        await asyncio.sleep(0.2)
    await event.edit(f"**- تـم اخـتراق الـواقع بـنجاح 🕶️**\n\n{CYBER_IDENTITY}")

# 4. أمر "تحذير أمني" 
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تحذير"))
async def security_alert(event):
    alert_msg = (
        "**⚠️ تـنبيه أمـني عـالي الـخطورة !**\n"
        "**— — — — — — — — — —**\n"
        "**🔴 تـم رصـد مـحاولة دخـول غـير مـصرح لـحسابك.**\n"
        "**🌐 الآيـدي الـمهاجم: `152.12.0.94`**\n"
        "**📍 الـموقع: سـيرفرات الـمتمرد الـتقني.**\n"
        "**— — — — — — — — — —**\n"
        f"**تـم حـجب الـهجوم بـنجاح 🛡️**\n\n{CYBER_IDENTITY}"
    )
    await event.edit(alert_msg)
