from main import client, CMD_HELP
from telethon import events
import platform
from datetime import datetime

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

    # نص الفحص الفخم بهوية المتمرد
    rebel_msg = f"""
**ᯓ AL-MUTAMARRID SOURCE - 𝗦𝗧𝗔𝗧𝗨𝗦** 𓆪
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
⌔ **المتمرد يعمل بنجاح يا كنق** ✅
⌔ **الاستجابة:** `{ms}ms`
⌔ **النظام:** `{platform.system()}`
⌔ **الإصدار:** `V1.0`
⌔ **الوقت:** `{datetime.now().strftime('%I:%M %p')}`
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
**[ @almtmrdalmlwn39 ]**
"""
    await event.edit(rebel_msg)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.البوت"))
async def bot_info(event):
    # إثبات الحقوق للمتمرد التقني
    await event.edit("**𓄂 سورس المتمرد التقني | الإصدار الأول 🛡️**\n**المطور: @almtmrdalmlwn39**")
