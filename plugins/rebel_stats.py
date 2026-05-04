import asyncio
from telethon import events, functions, types
from __main__ import client 

# هوية الإحصائيات
STATS_IDENTITY = "**- مـركز بـيانات الـمتمرد الـتقني | الـإحصائيات 📊🦅**"

# 1. أمر إحصائيات الحساب الشاملة (كم كروب، كم شخص، كم بوت)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.احصائياتي"))
async def account_stats(event):
    await event.edit("**- جـاري تـحليل بـيانات الـحساب...**")
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

# 2. أمر "كشف الجروب" (كم عدد المشرفين، البوتات، المحظورين)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.كشف_الجروب"))
async def chat_info(event):
    if event.is_private: return
    await event.edit("**- جـاري تـشريح الـمجموعة بـياناتياً...**")
    chat = await event.get_chat()
    full_chat = await client(functions.channels.GetFullChannelRequest(chat))
    
    info = (
        f"**🏢 مـعلومات الـمجموعة :**\n"
        f"**— — — — — — — — — —**\n"
        f"**🆔 الآيـدي:** `{chat.id}`\n"
        f"**👥 الـأعضاء:** `{full_chat.full_chat.participants_count}`\n"
        f"**🚫 الـمحظورين:** `{full_chat.full_chat.kicked_count if full_chat.full_chat.kicked_count else '0'}`\n"
        f"**👮 الـمشرفين:** `{full_chat.full_chat.admins_count if full_chat.full_chat.admins_count else '1'}`\n"
        f"**— — — — — — — — — —**\n"
        f"{STATS_IDENTITY}"
    )
    await event.edit(info)

# 3. أمر "من أنا؟" (يعرض صورتك ومعلوماتك بشكل فخم للآخرين)
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

# --- [ قسم استعراض أوامر الإحصائيات ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اوامر_الاحصائيات"))
async def stats_help(event):
    help_text = (
        "**📊 أوامـر الـبيانات والـإحصائيات :**\n"
        "**— — — — — — — — — —**\n"
        "**📈 | `.احصائياتي` :** لـمعرفة تـفاصيل حـسابك كـاملاً.\n"
        "**🔍 | `.كشف_الجروب` :** لـمعرفة تـفاصيل الـمجموعة الـحالية.\n"
        "**🪪 | `.هويتي` :** لـعرض مـعلوماتك الـشخصية بـفخامة.\n"
        "**— — — — — — — — — —**\n"
        f"{STATS_IDENTITY}"
    )
    await event.edit(help_text)
