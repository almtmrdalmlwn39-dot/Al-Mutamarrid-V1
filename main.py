import asyncio, os, json, threading
from telethon import TelegramClient, events, functions
from telethon.sessions import StringSession
from telethon.tl.functions.channels import InviteToChannelRequest
import config 

# تعريف العميل أولاً لضمان عدم حدوث NameError
client = TelegramClient(StringSession(config.SESSION), config.API_ID, config.API_HASH)

def z_nums(text):
    n = {'0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'}
    return "".join(n.get(c, c) for c in text)

@client.on(events.NewMessage(outgoing=True))
async def rebel_core(event):
    text = event.raw_text
    
    # أمر النقل المطور
    if text.startswith(".نقل"):
        try:
            parts = text.split(" ")
            if len(parts) < 3:
                return await event.edit("**⚠️ الطريقة: `.نقل @المصدر @جروبك`**")
            
            from_chat = parts[1]
            to_chat = parts[2]
            await event.edit(f"**⏳ جاري محاولة الوصول إلى {from_chat}...**")
            
            # جلب الكيان (Entity) للتأكد من وجود الجروب
            source = await client.get_entity(from_chat)
            target = await client.get_entity(to_chat)
            
            participants = await client.get_participants(source, limit=100)
            done, fail = 0, 0
            
            await event.edit(f"**🚀 بدأت إضافة {z_nums(str(len(participants)))} عضو إلى {to_chat}...**")
            
            for user in participants:
                if user.bot: continue
                try:
                    await client(InviteToChannelRequest(target, [user.id]))
                    done += 1
                    await asyncio.sleep(2) # تأخير ضروري لتجنب الحظر
                except:
                    fail += 1
            
            await event.edit(f"**🏁 انتهت العملية.**\n✅ تم نقل: `{z_nums(str(done))}`\n❌ فشل: `{z_nums(str(fail))}`")
            
        except Exception as e:
            await event.edit(f"**❌ خطأ في النقل: {str(e)}**")

    # أمر السحب الحقيقي
    elif text.startswith(".سحب"):
        try:
            chat = text.split(" ")[1]
            await event.edit(f"**⏳ جاري فحص أعضاء {chat}...**")
            p = await client.get_participants(chat, limit=5000)
            await event.edit(f"**✅ تم سحب `{z_nums(str(len(p)))}` عضو حقيقي.**")
        except Exception as e:
            await event.edit(f"**❌ لم يتم العثور على الجروب.**")

async def start():
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(start())
