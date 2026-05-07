import asyncio, os, pytz, glob, importlib, sys, re, json, threading
from datetime import datetime
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import GetFullChannelRequest, JoinChannelRequest
import config 

# --- [1] الهوية والإعدادات ---
REBEL_SIG_TEXT = "نحن لا نحمي بياناتك فقط، نحن نمنحك القوة لتكون السيد في عالم لا يعترف إلا بالأقوياء. المتمرد.. أمانٌ لا يُخترق، وهيبةٌ لا تُهزم."
REBEL_IMG = "https://telegra.ph/file/058204663f73359d997f0.jpg"

app = Flask(__name__)
@app.route('/')
def health_check(): return "🛡️ Rebel Source is Live"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()

client = TelegramClient(StringSession(config.SESSION), config.API_ID, config.API_HASH)

def z_nums(text):
    n = {'0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'}
    return "".join(n.get(c, c) for c in text)

# --- [2] محرك السحب الذكي (عام + خاص) ---
@client.on(events.NewMessage(outgoing=True, pattern=r'\.سحب (.*)'))
async def advanced_scraper(event):
    link = event.pattern_match.group(1).strip()
    await event.edit(f"**⏳ جاري محاولة اختراق حماية {link}...**")
    
    try:
        if "t.me/+" in link or "joinchat/" in link:
            # التعامل مع الروابط الخاصة
            hash_code = link.split('/')[-1].replace('+', '')
            try:
                await client(ImportChatInviteRequest(hash_code))
                await event.edit("**✅ تم الانضمام للجروب الخاص.. جاري السحب الآن.**")
            except: pass # إذا كان الحساب موجوداً بالفعل
            target = link
        else:
            target = link # الجروبات العامة

        # السحب الحقيقي للأعضاء
        all_participants = []
        async for user in client.iter_participants(target, limit=5000):
            if not user.bot:
                all_participants.append(user)
        
        count = len(all_participants)
        await event.edit(f"**✅ تم سحب `{z_nums(str(count))}` عضو حقيقي بنجاح.**\n\n🛡️ ملاحظة: إذا كان العدد أقل من الكلي، فالجروب يخفي بقية الأعضاء.")
        
    except Exception as e:
        await event.edit(f"**❌ فشل السحب.**\nالسبب: {str(e)}")

# --- [3] بقية الأوامر (فحص، اوامر، حماية) ---
@client.on(events.NewMessage(outgoing=True))
async def main_logic(event):
    if event.raw_text == ".فحص":
        await event.edit(f"**🛡️ سورس المتمرد يعمل بنجاح.**\n\n{REBEL_SIG_TEXT}")
    
    elif event.raw_text == ".الاوامر":
        all_list = [".سحب", ".ايدي", ".فحص", ".تفعيل الحماية"]
        msg = f"🛡️ **قائمة أوامر المتمرد**\n— — —\n{REBEL_SIG_TEXT}\n— — —\n"
        for i, cmd in enumerate(all_list, 1):
            msg += f"{z_nums(str(i))} ⇐ {cmd}\n"
        await event.edit(msg)

async def start():
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(start())
