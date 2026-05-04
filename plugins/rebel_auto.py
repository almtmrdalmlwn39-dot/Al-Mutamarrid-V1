import asyncio
from telethon import events
from __main__ import client 

# هوية الرد التلقائي
AUTO_IDENTITY = "**- نـظام الـرد الـآلي | الـمتمرد الـتقني 🤖🦅**"

# 1. أمر الترحيب بالأعضاء الجدد (يعمل تلقائياً عند دخول شخص للكروب)
@client.on(events.ChatAction)
async def welcome_rebel(event):
    if event.user_joined:
        await event.reply(
            "**اهـلاً بـك فـي مـعقل الـمتمرد الـتقني! 🏴‍☠️\n"
            "— — — — — — — — — — —\n"
            "نـتمنى لـك وقـتاً مـمتعاً ومـفيداً فـي الـمجموعة.**\n"
            f"\n{AUTO_IDENTITY}"
        )

# 2. الرد التلقائي عند ذكر اسمك (مثال: لو حد كتب "المتمرد")
@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    if "المتمرد" in event.text and not event.out:
        await event.reply("**لـبيك! سـيد الـمتمرد مـشغول الآن بـتطوير الـعالم.. اتـرك رسـالتك. 🛡️**")

# 3. أمر "الرد السريع" (يحفظ نص مخصص لترسله بسرعة)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.قلك"))
async def quick_statement(event):
    msg = (
        "**- قـال لـك الـمتمرد الـتقني :**\n"
        "**الـعقول الـعظيمة تـبني الـأكواد، والـنفوس الـقوية تـحمي الـعهود. 🦅**"
    )
    await event.edit(msg)

# --- [ قسم استعراض أوامر الرد الآلي ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اوامر_الرد"))
async def auto_help(event):
    help_text = (
        "**🤖 أوامـر الـرد والـترحيب الـآلي :**\n"
        "**— — — — — — — — — —**\n"
        "**✨ | الـترحيب :** يـعمل تـلقائياً عـند دخـول أي عـضو جـديد.\n"
        "**🗣️ | الـمنشن :** يـرد تـلقائياً عـلى كـلمة 'الـمتمرد'.\n"
        "**🦅 | `.قلك` :** إرسـال مـقولة خـاصة بـك بـسرعة.\n"
        "**— — — — — — — — — —**\n"
        f"{AUTO_IDENTITY}"
    )
    await event.edit(help_text)
