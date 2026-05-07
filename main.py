import asyncio, os, json, threading
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
from telethon.tl.functions.channels import GetFullChannelRequest, InviteToChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
import config 

# --- [1] إعداد السيرفر (Flask) لضمان العمل 24/7 على Render ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "🛡️ Rebel Source is Live"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

threading.Thread(target=run_flask, daemon=True).start()

# --- [2] تعريف العميل (Client) - تم وضعه هنا لتجنب أخطاء التعريف ---
client = TelegramClient(StringSession(config.SESSION), config.API_ID, config.API_HASH)

# الهوية والرسائل الثابتة
REBEL_SIG = "نحن لا نحمي بياناتك فقط، نحن نمنحك القوة لتكون السيد في عالم لا يعترف إلا بالأقوياء. المتمرد.. هيبةٌ لا تُهزم."
REBEL_IMG = "https://telegra.ph/file/058204663f73359d997f0.jpg"

def z_nums(text):
    n = {'0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'}
    return "".join(n.get(c, c) for c in text)

# --- [3] محرك الأوامر (سحب، نقل، ايدي، فحص) ---

@client.on(events.NewMessage(outgoing=True))
async def rebel_commands(event):
    text = event.raw_text
    
    # 1. أمر الفحص
    if text == ".فحص":
        await event.edit(f"**🛡️ سورس المتمرد يعمل بنجاح ومستقر الآن.**")

    # 2. أمر الأوامر
    elif text == ".الاوامر":
        all_list = [".سحب (المعرف)", ".نقل (من) (إلى)", ".ايدي", ".فحص"]
        msg = f"🛡️ **قائمة أوامر المتمرد المطورة**\n— — —\n"
        for i, cmd in enumerate(all_list, 1):
            msg += f"{z_nums(str(i))} ⇐ `{cmd}`\n"
        msg += f"— — —\n{REBEL_SIG}"
        await event.edit(msg)

    # 3. أمر الآيدي
    elif text == ".ايدي":
        reply = await event.get_reply_message()
        target = reply.sender if reply else await event.get_sender()
        await event.edit(f"🆔 الايدي الخاص بك: `{target.id}`")

    # 4. أمر السحب (لمعرفة العدد الحقيقي)
    elif text.startswith(".سحب"):
        try:
            chat = text.split(" ")[1]
            await event.edit(f"**⏳ جاري سحب بيانات الأعضاء من {chat}...**")
            participants = await client.get_participants(chat, limit=5000)
            await event.edit(f"**✅ تم سحب `{z_nums(str(len(participants)))}` عضو حقيقي بنجاح.**")
        except Exception as e:
            await event.edit(f"**❌ فشل السحب: {str(e)}**")

    # 5. أمر النقل (سحب وإضافة تلقائية) - الميزة الجديدة
    elif text.startswith(".نقل"):
        try:
            parts = text.split(" ")
            if len(parts) < 3:
                return await event.edit("**⚠️ استخدام خاطئ. مثال: `.نقل @from @to`**")
            
            from_chat = parts[1]
            to_chat = parts[2]
            await event.edit(f"**🚀 بدأت عملية نقل الأعضاء إلى {to_chat}...**")
            
            participants = await client.get_participants(from_chat, limit=100)
            done, fail = 0, 0
            
            for user in participants:
                if user.bot: continue
                try:
                    await client(InviteToChannelRequest(to_chat, [user.id]))
                    done += 1
                    await asyncio.sleep(1.5) # لتجنب الحظر
                except:
                    fail += 1
            
            await event.edit(f"**🏁 اكتمل النقل.**\n✅ نجاح: `{z_nums(str(done))}`\n❌ فشل: `{z_nums(str(fail))}`")
        except Exception as e:
            await event.edit(f"**❌ خطأ في النقل: {str(e)}**")

# --- [4] تشغيل السورس ---
async def start_rebel():
    await client.start()
    print("🛡️ REBEL SOURCE IS ONLINE")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(start_rebel())
