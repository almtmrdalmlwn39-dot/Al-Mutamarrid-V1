from telethon import events
from __main__ import client
import asyncio

# قائمة مؤقتة لضمان عدم تكرار الرد التلقائي في نفس الجلسة
replied_users = set()

# --- ميزة الرد التلقائي الذكي للمتمرد ---
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def rebel_auto_reply(event):
    me = await client.get_me()
    sender = await event.get_sender()

    # شروط عدم الرد: (إذا كنت أنت، أو الشخص مسموح له، أو بوت، أو ردينا عليه مسبقاً)
    if event.out or sender.bot or sender.contact or event.sender_id in replied_users:
        return

    # نص الرد التلقائي الفخم (بدون أزرار وبدون كلمات بوت)
    auto_msg = f"""**‹ مـمـلـكـة الـمـتـمـرد الـتـقـنـيـة V1 🛡️ ›**
**— — — — — — — — — —**

**• أهـلاً بـك يـا {sender.first_name} في مـنـصـة الـمـطـور.**
**• لـقـد وصـلـت رسـالـتـك إلـى أنـظمة الـرصـد والـحـمـايـة.**

**• أنـا بـوت الـمـطـور الـخـاص، أعـمـل عـلـى تـنـظـيـم الـخـاص.**
**• ارسـل سـبـب تـواصـلك بـوضـوح وسـيـتـم الـرد مـن قـبـل الـمـطـور قـريـبـاً.**

**— — — — — — — — — —**
**‹ نـحـن لا نـنـتـظـر الـفـرص.. نـحـن نـصـنـعـهـا ›**"""

    try:
        # إرسال الرسالة وإضافة الشخص للقائمة لكي لا يكرر البوت الرد عليه
        await event.reply(auto_msg)
        replied_users.add(event.sender_id)
    except:
        pass
