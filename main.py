import asyncio, os, json, threading
from flask import Flask
from telethon import TelegramClient, events, functions
from telethon.sessions import StringSession
import config 

# --- [1] تعريف السيرفر (Flask) لضمان بقاء السورس حياً ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "🛡️ Rebel Source is Live"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()

# --- [2] تعريف المتغير 'client' أولاً لحل مشكلة NameError ---
client = TelegramClient(StringSession(config.SESSION), config.API_ID, config.API_HASH)

REBEL_SIG = "نحن لا نحمي بياناتك فقط، نحن نمنحك القوة لتكون السيد.. المتمرد."
REBEL_IMG = "https://telegra.ph/file/058204663f73359d997f0.jpg"

def z_nums(text):
    n = {'0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'}
    return "".join(n.get(c, c) for c in text)

# --- [3] محرك الأوامر (سحب حقيقي + فحص + أوامر) ---
@client.on(events.NewMessage(outgoing=True))
async def rebel_handler(event):
    text = event.raw_text
    
    # أمر السحب الحقيقي (يتجاوز الحماية الظاهرية)
    if text.startswith(".سحب"):
        try:
            parts = text.split(" ")
            if len(parts) < 2: return await event.edit("**❌ أرسل المعرف (مثال: .سحب @username)**")
            chat = parts[1]
            await event.edit(f"**⏳ جاري سحب البيانات الحقيقية من {chat}...**")
            
            # جلب الأعضاء الفعليين باستخدام iter_participants لضمان المصداقية
            participants = await client.get_participants(chat, limit=2000) 
            real_count = len(participants)
            
            await event.edit(f"**✅ تم سحب `{z_nums(str(real_count))}` عضو حقيقي بنجاح.**\n\n🛡️ ملاحظة: إذا كان الرقم 0، فالجروب يخفي أعضاءه تماماً عن الحسابات العادية.")
        except Exception as e:
            await event.edit(f"**❌ خطأ: {str(e)}**")

    elif text == ".فحص":
        await event.edit(f"**🛡️ سورس المتمرد يعمل بنجاح (تم إصلاح خطأ client).**")

    elif text == ".الاوامر":
        msg = f"🛡️ **أوامر المتمرد**\n— — —\n1 ⇐ .سحب\n2 ⇐ .ايدي\n3 ⇐ .فحص\n4 ⇐ .تفعيل الحماية\n— — —"
        await event.edit(msg)

# --- [4] بدء التشغيل ---
async def main():
    await client.start()
    print("🛡️ REBEL SOURCE LOADED SUCCESSFULLY")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
