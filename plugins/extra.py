import random
from telethon import events, functions
from telethon.tl.functions.users import GetFullUserRequest
from main import client, CMD_HELP

# --- [ AL-MUTAMARRID GLOBAL IDENTITY ] ---
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"

# إضافة القسم للقائمة
CMD_HELP.update({
    "الإضافات والترفيه": [
        "حب", "كذب", "غادر", "الرابط", "ايدي"
    ]
})

# --- [ 1. أوامر التسلية والترفيه ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.نسبة الحب"))
async def love(event):
    score = random.randint(0, 100)
    await event.edit(f"**❤️ نسبة الحب هي : {score}%**\n\n{WAR_IDENTITY}")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.كشف الكذب"))
async def lie(event):
    results = ["كاذب ❌", "صادق ✅", "نصاب كبير 🤡", "ماشاء الله صادق 🙏"]
    res = random.choice(results)
    await event.edit(f"**⚖️ النتيجة هي : {res}**\n\n{WAR_IDENTITY}")

# --- [ 2. أوامر المجموعات الإضافية ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.غادر"))
async def leave(event):
    me = await client.get_me()
    name = me.first_name
    await event.edit(f"**🦅 {name} يغادر المكان.. وداعاً**\n\n{WAR_IDENTITY}")
    await client(functions.channels.LeaveChannelRequest(event.chat_id))

@client.on(events.NewMessage(outgoing=True, pattern=r"\.الرابط"))
async def get_link(event):
    try:
        res = await client(functions.messages.ExportChatInviteRequest(event.chat_id))
        await event.edit(f"**🔗 رابط المجموعة : {res.link}**\n\n{WAR_IDENTITY}")
    except:
        await event.edit("**❌ لا أملك صلاحيات لاستخراج الرابط!**")

# --- [ 3. أوامر المعلومات المتطورة ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.ايدي"))
async def get_id(event):
    await event.edit("**🔍 جاري جلب بيانات الهوية...**")
    
    # تحديد المستخدم (صاحب الرد أو الشخص نفسه)
    if event.is_reply:
        reply = await event.get_reply_message()
        user_id = reply.sender_id
    else:
        user_id = "me"
        
    try:
        # جلب معلومات المستخدم بالكامل بما فيها البايو
        full_user = await client(GetFullUserRequest(user_id))
        user = full_user.users[0]
        photo = await client.download_profile_photo(user.id)
        
        info_text = (
            f"**🧬 𝗨𝗦𝗘𝗥 𝗜𝗡𝗙𝗢𝗥𝗠𝗔𝗧𝗜𝗢𝗡 :**\n"
            f"**— — — — — — — — — —**\n"
            f"**👤 الـاسم:** {user.first_name}\n"
            f"**🆔 الآيـدي:** `{user.id}`\n"
            f"**🔗 الـمعرف:** @{user.username if user.username else 'لا يوجد'}\n"
            f"**📖 الـبايو:** `{full_user.full_user.about if full_user.full_user.about else 'خالي'}`\n"
            f"**— — — — — — — — — —**\n"
            f"{WAR_IDENTITY}"
        )
        
        # إذا كان لديه صورة بروفايل يرسلها مع النص، وإلا يكتفي بالنص
        if photo:
            await client.send_file(event.chat_id, photo, caption=info_text, reply_to=event.reply_to_msg_id)
            await event.delete()
        else:
            await event.edit(info_text)
            
    except Exception as e:
        await event.edit(f"**❌ حدث خطأ أثناء جلب البيانات!**")

