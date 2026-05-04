import os, pytz, asyncio, sys
from datetime import datetime
from collections import defaultdict
from telethon import events, functions, types
from telethon.tl.functions.channels import EditBannedRequest, EditTitleRequest
from telethon.tl.types import ChatBannedRights

# --- [ محرك الربط الذكي ] ---
def get_rebel_client():
    # محاولة سحب الكلاينت من الذاكرة لضمان عدم حدوث Error
    main_mod = sys.modules.get('__main__')
    c = getattr(main_mod, 'client', None)
    if not c:
        for mod in sys.modules.values():
            c = getattr(mod, 'client', None)
            if c: break
    return c

client = get_rebel_client()

# --- [ الإعدادات ] ---
YEMEN_TZ = pytz.timezone('Asia/Aden')
BANNED_RIGHTS = ChatBannedRights(until_date=None, view_messages=True, send_messages=True, send_media=True, send_stickers=True, send_gifs=True, send_games=True, send_inline=True, embed_links=True)

CYBER_IDENTITY = "**- نـحنُ حـماةُ الـخصوصيةِ فـي زمنِ الاختراق، نـبرمجُ الـصمتَ ونـصنعُ الـفرق.. عـقولنا خـلفَ الـشاشاتِ تـبني، وأيـدينا فـي الأنـظمةِ تـحمي. 🦅💻🛡️**"

# ذاكرة السورس
welcomed_users = set() 
user_messages = defaultdict(list) 

# دالة زخرفة الأرقام اليمنية
def custom_nums(text):
    n = {'0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'}
    return "".join(n.get(c, c) for c in text)

# --- [ 1. محرك الحماية والترحيب الفوري ] ---
if client:
    @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
    async def fast_security_engine(event):
        if event.is_bot: return
        me = await client.get_me()
        sender_id = event.sender_id
        if sender_id == me.id: return

        if sender_id not in welcomed_users:
            sender = await event.get_sender()
            time_now = datetime.now(YEMEN_TZ).strftime("%I:%M %p")
            welcome_msg = (
                f"**- مـرحباً بـك يـا {sender.first_name} فـي سـيرفر الـمتمرد 🦅\n"
                f"**- تـوقيت الـيمن الـمحدد: {custom_nums(time_now)}**\n"
                "**— — — — — — — — — —**\n"
                "**🛡️ | جـدار الـحماية مـفعل تـلقائياً.**\n"
                "**⏳ | جـاري تـحليل طـلبك، انـتظر الـمطور.**\n\n"
                f"{CYBER_IDENTITY}"
            )
            try:
                await event.reply(welcome_msg)
                welcomed_users.add(sender_id)
            except: pass
        else:
            now = datetime.now().timestamp()
            user_messages[sender_id] = [t for t in user_messages[sender_id] if now - t < 10]
            user_messages[sender_id].append(now)
            
            msg_count = len(user_messages[sender_id])
            if msg_count > 4:
                if msg_count < 7:
                    await event.reply("**⚠️ هوي يا مستخدم! ممنوع التكرار. جدار حماية المتمرد يراقبك! 🚫**")
                else:
                    await event.reply("**🚫 تم حظرك تلقائياً لتجاوزك حدود الأدب!**")
                    await client(functions.contacts.BlockRequest(id=sender_id))

    # --- [ 2. محرك الأوامر ] ---

    @client.on(events.NewMessage(pattern=r'^\.رفض$', outgoing=True))
    async def reject_cmd(event):
        chat_id = event.chat_id
        welcomed_users.discard(chat_id)
        user_messages[chat_id] = []
        await event.edit("**✅ تـم الـرفض. عيرجع يستلم الترحيب من جديد!**")

    @client.on(events.NewMessage(pattern=r'^\.سماح$', outgoing=True))
    async def allow_cmd(event):
        welcomed_users.add(event.chat_id)
        await event.edit("**✅ تـم الـسماح بـفخامة.**")

    @client.on(events.NewMessage(pattern=r'^\.(الاوامر|اوامر)$', outgoing=True))
    async def help_cmd(event):
        await event.edit(
            f"**- أوامـر الـمتمرد الـقوية 🦅 :**\n\n"
            "**🛡️ .سماح | .رفض | .حظر_خاص**\n"
            "**🧨 .تدمير | .تفليش | .بينج**\n\n"
            f"{CYBER_IDENTITY}"
        )

    @client.on(events.NewMessage(pattern=r'^\.بينج$', outgoing=True))
    async def ping_cmd(event):
        start = datetime.now()
        await event.edit("**🚀 جـاري قـياس الـنبض...**")
        end = datetime.now()
        ms = (end - start).microseconds / 1000
        await event.edit(f"**⚡ سـرعة الـمتمرد: `{ms}`ms**")
