from main import client, CMD_HELP
from telethon import events
import platform
from datetime import datetime

# --- [ AL-MUTAMARRID GLOBAL IDENTITY ] ---
# البصمة الملكية الموحدة بالخط الإنجليزي العريض
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"

# إضافة القسم لقائمة أوامر المتمرد العامة
CMD_HELP.update({
    "فحص المتمرد": [
        "فحص", "البوت"
    ]
})

@client.on(events.NewMessage(outgoing=True, pattern=r"\.فحص"))
async def check(event):
    start = datetime.now()
    await event.edit("**𓄂 جاري فحص استجابة المتمرد...**")
    end = datetime.now()
    ms = (end - start).microseconds / 1000

    # نص الفحص الفخم مع اسم الإصدار بالإنجليزية
    rebel_msg = f"""
**{WAR_IDENTITY} - 𝗦𝗧𝗔𝗧𝗨𝗦** ⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
⌔ **المتمرد يعمل بنجاح يا ملك** ✅
⌔ **الاستجابة:** `{ms}ms`
⌔ **النظام:** `{platform.system()}`
⌔ **الإصدار:** `𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗩𝟭.𝟬`
⌔ **الوقت:** `{datetime.now().strftime('%I:%M %p')}`
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
"""
    await event.edit(rebel_msg)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.البوت"))
async def bot_info(event):
    # إثبات الحقوق مع اسم السورس والإصدار بالإنجليزية
    await event.edit(f"**{WAR_IDENTITY}**\n\n**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗧𝗘𝗖𝗛𝗡𝗜𝗖𝗔𝗟 - 𝗩𝟭.𝟬 🛡️**")
