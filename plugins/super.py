import asyncio, os, pytz, re, random
from datetime import datetime
from telethon import events, functions, types
from telethon.tl.functions.channels import EditBannedRequest, EditTitleRequest
from telethon.tl.types import ChatBannedRights
from __main__ import client  

# --- [ إعدادات المتمرد ] ---
approved_users = set()
warned_users = set() # لمنع التكرار
BANNED_RIGHTS = ChatBannedRights(until_date=None, view_messages=True, send_messages=True, send_media=True, send_stickers=True, send_gifs=True, send_games=True, send_inline=True, embed_links=True)

# --- [ 1. محرك الحماية - رد مرة واحدة فقط بصورة بروفايلك ] ---
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def pm_protection(event):
    sender = await event.get_sender()
    if not sender or sender.bot or sender.contact or event.sender_id in approved_users or event.sender_id in warned_users:
        return
    if event.sender_id == (await client.get_me()).id:
        return

    warn_text = f"**- عذراً يا {sender.first_name} 🛡️\n- نظام حماية المتمرد مفعل حالياً.\n- المطور مشغول، سيتم الرد عليك لاحقاً.**"
    
    try:
        me = await client.get_me()
        photo = await client.download_profile_photo(me.id)
        if photo:
            await client.send_file(event.chat_id, photo, caption=warn_text)
        else:
            await event.reply(warn_text)
        warned_users.add(event.sender_id)
    except:
        await event.reply(warn_text)
        warned_users.add(event.sender_id)

# --- [ 2. المحرك الملكي الشامل ] ---
@client.on(events.NewMessage(outgoing=True))
async def mutamarrid_omega_engine(event):
    cmd = event.text
    chat = event.chat_id

    # --- قسم الحماية ---
    if cmd == ".سماح" and event.is_reply:
        reply = await event.get_reply_message()
        approved_users.add(reply.sender_id)
        await event.edit("**- تم السماح له بالمراسلة ✅**")
    
    elif cmd == ".رفض" and event.is_reply:
        reply = await event.get_reply_message()
        from telethon.tl.functions.contacts import BlockRequest
        await client(BlockRequest(id=reply.sender_id))
        await event.edit("**- تم سحق المتطفل وحظره 🚫**")

    # --- قسم التفليش (تمت إضافة الكود القوي هنا) ---
    elif cmd == ".تدمير" or cmd == ".تفليش":
        await event.edit("**- جـاري الاكتساح الشامل.. المتمرد في الميدان 🧨**")
        count = 0
        async for user in client.iter_participants(chat):
            if user.is_self or user.admin_rights: # يتخطى نفسك والمشرفين عشان ما يوقف
                continue
            try:
                await client(EditBannedRequest(chat, user.id, BANNED_RIGHTS))
                count += 1
            except: continue
        await event.respond(f"**- تم تنظيف المجموعة من {count} ضحية ✅\n- المتمرد التقني مر من هنا 🦅**")
    
    elif cmd.startswith(".تكرار"):
        parts = cmd.split(" ", 2)
        if len(parts) == 3:
            count = int(parts[1])
            for i in range(count):
                await client.send_message(chat, parts[2])
                await asyncio.sleep(0.2)

    # --- قسم الإدارة والتسلية ---
    elif cmd == ".حظر" and event.is_reply:
        reply = await event.get_reply_message()
        await client(EditBannedRequest(chat, reply.sender_id, BANNED_RIGHTS))
        await event.edit("**- تم الحظر من المجموعة بنجاح 🚷**")
    
    elif cmd == ".بينج":
        start = datetime.now()
        await event.edit("**جاري فحص السرعة...**")
        end = datetime.now()
        await event.edit(f"**- سرعة المتمرد : `{(end - start).microseconds / 1000}`ms ⚡**")

    # --- قائمة الأوامر ---
    elif cmd == ".الاوامر":
        menu = (
            "**- مـوسوعة أوامـر الـمتمرد الـشاملة 🦅 :**\n"
            "**— — — — — — — — — —**\n"
            "**🛡️ | الـحماية :** (.سماح | .رفض)\n"
            "**🧨 | الـتدمير :** (.تدمير | .تفليش | .تكرار)\n"
            "**⚙️ | الـخدمة :** (.بينج | .اذاعة | .غادر)\n"
            "**🔍 | الـفحص :** (.ايدي | .فحص | .الرابط)\n"
            "**🎮 | الـتسلية :** (.نسبة الحب | .كشف الكذب)\n"
            "**📊 | الإدارة :** (.كتم | .طرد | .حظر)\n"
            "**— — — — — — — — — —**\n"
            "**- نـحن لا نـهزم.. الـمتمرد الـتقني 🇾🇪**"
        )
        await event.edit(menu)
