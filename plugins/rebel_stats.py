import asyncio
from telethon import events, functions, types
from main import client, CMD_HELP

# --- [ AL-MUTAMARRID STATS BRAND ] ---
# استخدام الهوية الموحدة لضمان الفخامة البصرية
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"
STATS_BRAND = "**📊 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗔𝗡𝗔𝗟𝗬𝗧𝗜𝗖𝗦**"

# تسجيل القسم في قائمة المساعدة
CMD_HELP.update({
    "البيانات والإحصائيات": [
        "احصائياتي", "كشف_الجروب", "هويتي", "اوامر_الاحصائيات"
    ]
})

# 1. أمر إحصائيات الحساب الشاملة
@client.on(events.NewMessage(outgoing=True, pattern=r"\.احصائياتي"))
async def account_stats(event):
    await event.edit("**🔄 جـاري تـحـلـيـل قـاعـدة بـيـانـات الـحـساب...**")
    try:
        # طلب قائمة الحوارات وتحليلها
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
            f"**📊 تـقـريـر الـتـحـلـيـل الـمـلكـي :**\n"
            f"**— — — — — — — — — — —**\n"
            f"**👤 الـحـسابـات الـخاصـة :** `{private}`\n"
            f"**👥 الـمـجـمـوعـات :** `{groups}`\n"
            f"**📢 الـقـنـوات الـعـامـة :** `{channels}`\n"
            f"**🤖 الـبـوتات الـنـشـطة :** `{bots}`\n"
            f"**— — — — — — — — — — —**\n"
            f"{WAR_IDENTITY}"
        )
        await event.edit(res_text)
    except Exception as e:
        await event.edit(f"**⚠️ حـصل خـطأ أثـناء الـتحليل:** `{e}`")

# 2. أمر "كشف الجروب" (تحليل المجموعة)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.كشف_الجروب"))
async def chat_info(event):
    if event.is_private: 
        return await event.edit("**⚠️ هـذا الأمـر يـعمل داخـل الـمجموعات فـقط!**")
    
    await event.edit("**🔍 جـاري تـشـريـح الـمـجـموعة تـقـنـيـاً...**")
    try:
        chat = await event.get_chat()
        full_chat = await client(functions.channels.GetFullChannelRequest(chat))
        
        info = (
            f"**🏢 تـفـاصـيـل الـمـنـظـومـة :**\n"
            f"**— — — — — — — — — — —**\n"
            f"**🆔 آيـدي الـمجموعة :** `{chat.id}`\n"
            f"**👥 عـدد الـمـتواجـديـن :** `{full_chat.full_chat.participants_count}`\n"
            f"**— — — — — — — — — — —**\n"
            f"{WAR_IDENTITY}"
        )
        await event.edit(info)
    except Exception:
        await event.edit("**🚫 لا أمـلك الـصلاحيات الـكافـية لـتفكيك بـيانات الـمجموعة.**")

# 3. أمر "هويتي" (البطاقة التعريفية)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.هويتي"))
async def my_id(event):
    me = await client.get_me()
    my_info = (
        f"**🪪 بـطـاقـة تـعـريـف الـمـتـمـرد :**\n"
        f"**— — — — — — — — — — —**\n"
        f"**👤 الـاسـم :** `{me.first_name}`\n"
        f"**🆔 الآيـدي :** `{me.id}`\n"
        f"**🔗 الـيـوزر :** @{me.username if me.username else 'لا يـوجد'}\n"
        f"**— — — — — — — — — — —**\n"
        f"{WAR_IDENTITY}"
    )
    await event.edit(my_info)

# 4. قائمة أوامر الإحصائيات
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اوامر_الاحصائيات"))
async def stats_help(event):
    help_text = (
        f"**{STATS_BRAND}**\n"
        "**— — — — — — — — — — —**\n"
        "**📈 | `.احصائياتي` :** تـحليل شـامل لـحسابك.\n"
        "**🔍 | `.كشف_الجروب` :** مـعـلومات الـمجموعة الـحالية.\n"
        "**🪪 | `.هويتي` :** بـيـانـاتك الـشخصية الـمـسجلة.\n"
        "**— — — — — — — — — — —**\n"
        f"{WAR_IDENTITY}"
    )
    await event.edit(help_text)
