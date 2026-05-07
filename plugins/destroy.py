from main import client, CMD_HELP # استيراد المحرك والقاموس
from telethon import events, functions, types
import asyncio

# تسجيل الأمر لكي يظهر تلقائياً في قائمة .الاوامر
CMD_HELP["التدمير"] = ["تلفيش"]

def z_nums(text):
    n = {'0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'}
    return "".join(n.get(c, c) for c in text)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.تلفيش"))
async def rebel_destruction_engine(event):
    if not event.is_group:
        return await event.edit("**⚠️ هذا الأمر مخصص للمجموعات فقط.**")
        
    chat = await event.get_chat()
    admin_id = (await client.get_me()).id
    count = 0
    
    await event.edit("**🛡️ جاري إحكام السيطرة على المجموعة... ⚠️**")
    await asyncio.sleep(1)
    await event.edit("**🧨 بدأ الانفجار.. لا مكان للضعفاء هنا 🧨**")
    
    # سحب الأعضاء بشكل قسري ومباشر
    async for user in client.iter_participants(chat):
        if user.id == admin_id or user.is_self:
            continue
            
        try:
            # تنفيذ الحظر الشامل لجميع الصلاحيات
            await client(functions.channels.EditBannedRequest(
                channel=chat,
                participant=user.id,
                banned_rights=types.ChatBannedRights(
                    until_date=None,
                    view_messages=True,
                    send_messages=True,
                    send_media=True,
                    send_stickers=True,
                    send_gifs=True,
                    send_games=True,
                    send_inline=True,
                    embed_links=True
                )
            ))
            count += 1
            if count % 5 == 0:
                await event.edit(f"**🔥 جاري الانفجار.. الضحايا: {z_nums(str(count))}**")
            
            # تأخير بسيط جداً لتجنب حظر الحساب من التليجرام (FloodWait)
            await asyncio.sleep(0.3) 
            
        except Exception:
            continue

    msg = f"**✅ انتهت المهمة بنجاح**\n"
    msg += f"**- الأرض أصبحت قاعاً صفصفاً بعد مرور المتمرد.**\n"
    msg += f"**- اجمالي الضحايا: {z_nums(str(count))}**\n"
    msg += f"**- المتمرد التقني مر من هنا 🦅**"
    await event.edit(msg)
