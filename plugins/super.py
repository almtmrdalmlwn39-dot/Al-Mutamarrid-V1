import asyncio, os, pytz, re, random
from datetime import datetime
from telethon import events, functions, types
from telethon.tl.functions.messages import EditChatAboutRequest 
from telethon.tl.functions.channels import EditBannedRequest, EditTitleRequest
from telethon.tl.types import ChatBannedRights
from __main__ import client  

# --- [ إعدادات الهوية والوقت ] ---
YEMEN_TZ = pytz.timezone('Asia/Aden')
approved_users = set()
warned_users = set() 
BANNED_RIGHTS = ChatBannedRights(until_date=None, view_messages=True, send_messages=True, send_media=True, send_stickers=True, send_gifs=True, send_games=True, send_inline=True, embed_links=True)

# الهوية السيبرانية
CYBER_IDENTITY = "**- نـحنُ حـماةُ الـخصوصيةِ فـي زمنِ الاختراق، نـبرمجُ الـصمتَ ونـصنعُ الـفرق.. عـقولنا خـلفَ الـشاشاتِ تـبني، وأيـدينا فـي الأنـظمةِ تـحمي. 🦅💻🛡️**"

# --- [ تثبيت النبذة الشخصية القوية ] ---
async def set_fixed_bio():
    try:
        my_bio = "نبذة تعريفية شخص مغرم بنفسه ولايتنازل لـ خلق الله ابدا"
        await client(functions.account.UpdateProfileRequest(about=my_bio))
    except: pass

client.loop.create_task(set_fixed_bio())

# --- [ 1. محرك الترحيب السيبراني بصورتك ] ---
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def pm_protection(event):
    if event.is_bot: return
    sender = await event.get_sender()
    if not sender or event.sender_id in approved_users or event.sender_id in warned_users:
        return
    me = await client.get_me()
    if event.sender_id == me.id: return
    
    time_now = datetime.now(YEMEN_TZ).strftime("%I:%M %p")
    welcome_msg = (
        f"**- مـرحباً بـك يـا {sender.first_name} فـي سـيرفر الـمتمرد 🦅\n"
        f"**- تـوقيت الـيمن الـمحدد: {time_now}**\n"
        "**— — — — — — — — — —**\n"
        "**🛡️ | جـدار الـحماية مـفعل تـلقائياً.**\n"
        f"{CYBER_IDENTITY}"
    )
    
    try:
        photo = await client.download_profile_photo(me.id)
        if photo:
            await client.send_file(event.chat_id, photo, caption=welcome_msg)
        else:
            await event.reply(welcome_msg)
        warned_users.add(event.sender_id)
    except: pass

# --- [ 2. المحرك الرئيسي للأوامر ] ---
@client.on(events.NewMessage(outgoing=True))
async def mutamarrid_engine(event):
    cmd = event.text
    chat = event.chat_id

    if cmd == ".سماح":
        approved_users.add(event.chat_id)
        await event.edit("**✅ تـم الـسماح.**")
    
    elif cmd == ".حظر_خاص":
        await event.edit("**🚫 جـاري الـحظر..**")
        await client(functions.contacts.BlockRequest(id=event.chat_id))

    elif cmd in [".تدمير", ".تفليش"]:
        await event.edit("**- الـتطهير بـدأ 🧨**")
        try:
            await client(EditTitleRequest(chat, "تـم الاخـتراق بـواسطة الـمتمرد 🦅"))
        except: pass
        count = 0
        async for user in client.iter_participants(chat):
            if user.is_self or user.admin_rights: continue 
            try:
                await client(EditBannedRequest(chat, user.id, BANNED_RIGHTS))
                count += 1
            except: continue
        await event.respond(f"**- تـم سـحق {count} عـنصر بـنجاح ✅**")

    elif cmd == ".بينج":
        start = datetime.now()
        await event.edit("**- جـاري الـفحص...**")
        ms = (datetime.now() - start).microseconds / 1000
        await event.edit(f"**- الـسرعة : `{ms}`ms ⚡**")

    elif cmd in [".الاوامر", ".اوامر"]:
        await event.edit(f"**- أوامـر الـمتمرد 🦅 :**\n\n**🛡️ .سماح | .حظر_خاص**\n**🧨 .تدمير | .تفليش | .تكرار**\n\n{CYBER_IDENTITY}")
