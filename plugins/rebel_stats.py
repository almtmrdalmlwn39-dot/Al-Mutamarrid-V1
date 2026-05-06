import asyncio
from telethon import events, functions, types
# استدعاء القلب النابض للسورس لضمان عدم التضارب
import main 

client = main.client

# هوية الإحصائيات
STATS_IDENTITY = "**- مـركز بـيانات الـمتمرد الـتقني | الـإحصائيات 📊🦅**"

# 1. أمر إحصائيات الحساب الشاملة (كم كروب، كم شخص، كم بوت)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.احصائياتي"))
async def account_stats(event):
    await event.edit("**- جـاري تـحليل بـيانات الـحساب...**")
    try:
        result = await client(functions.messages.GetDialogsRequest(
            offset_date=None, offset_id=0, offset_peer=types.InputPeerEmpty(), limit=999, hash=0
        ))
        private, groups, channels, bots = 0, 0, 0, 0
        for dialog in result.chats:
            if isinstance(dialog, types.User):
                if dialog.bot: bots += 1
                else: private += 1
            elif isinstance(dialog, (types.Chat, types.Channel)):
                if isinstance(dialog, types.Channel) and dialog.broadcast: channels += 1
                else: groups += 1
                
        res_text = (
            f"**📊 تـقرير الـمتمرد لـلحساب :**\n"
            f"**— — — — — — — — — —**\n"
            f"**👤 الـخاص:** `{private}`\n"
            f"**👥 الـمجموعات:** `{groups}`\n"
            f"**📢 الـقنوات:** `{channels}`\n"
            f"**🤖 الـبوتات:** `{bots}`\n"
            f"**— — — — — — — — — —**\n"
            f"{STATS_IDENTITY}"
        )
        await event.edit(res_text)
    except Exception as e:
        await event.edit(f"**❌ حدث خطأ أثناء التحليل: {e}**")

# 2. أمر "كشف الجروب" (معلومات المجموعة الحالية)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.كشف_الجروب"))
async def chat_info(event):
    if event.is_private: return
    await event.edit("**- جـاري تـشريح الـمجموعة بـياناتياً...**")
    try:
        chat = await event.get_chat()
        full_chat = await client(functions.channels.GetFullChannelRequest(chat))
        
        info = (
            f"**🏢 مـعلومات الـمجموعة :**\n"
            f"**— — — — — — — — — —**\n"
            f"**🆔 الآيـدي:** `{chat.id}`\n"
            f"**👥 الـأعضاء:** `{full_chat.full_chat.participants_count}`\n"
            f"**— — — — — — — — — —**\n"
            f"{STATS_IDENTITY}"
        )
        await event.edit(info)
    except Exception:
        await event.edit("**❌ لا أملك صلاحيات كافية للكشف عن هذه المجموعة.**")

# 3. أمر "هويتي" (معلوماتك الشخصية)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.هويتي"))
async def my_id(event):
    me = await client.get_me()
    my_info = (
        f"**🪪 بـطاقة تـعريف الـمتمرد :**\n"
        f"**— — — — — — — — — —**\n"
        f"**- الـاسم:** {me.first_name}\n"
        f"**- الآيـدي:** `{me.id}`\n"
        f"**- الـيوزر:** @{me.username if me.username else 'لا يـوجد'}\n"
        f"**— — — — — — — — — —**\n"
        f"{STATS_IDENTITY}"
    )
    await event.edit(my_info)

# 4. قائمة أوامر الإحصائيات
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اوامر_الاحصائيات"))
async def stats_help(event):
    help_text = (
        "**📊 أوامـر الـبيانات والـإحصائيات :**\n"
        "**— — — — — — — — — —**\n"
        "**📈 | `.احصائياتي` :** تـفاصيل حـسابك كـاملاً.\n"
        "**🔍 | `.كشف_الجروب` :** تـفاصيل الـمجموعة الـحالية.\n"
        "**🪪 | `.هويتي` :** لـعرض مـعلوماتك الـشخصية.\n"
        "**— — — — — — — — — —**\n"
        f"{STATS_IDENTITY}"
    )
    await event.edit(help_text)
