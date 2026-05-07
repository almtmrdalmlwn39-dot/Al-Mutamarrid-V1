import asyncio, os, json, threading, re, glob, importlib
from pathlib import Path
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.tl.functions.channels import GetFullChannelRequest, InviteToChannelRequest
from telethon.sessions import StringSession
import config 

# [1] سيرفر ريندر لضمان بقاء البوت Live
app = Flask(__name__)
@app.route('/')
def health_check(): return "🛡️ Rebel Scraping Live"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()

# [2] الإعدادات
REBEL_TITLE = "┃ الأمن السيبراني 🛡️"
REBEL_IMG = "https://telegra.ph/file/058204663f73359d997f0.jpg"
REBEL_LINK = "👤 **المطور:** [المتمرد](https://t.me/Vi_ti0)"
SUDO_USERS = [6467728995] 

client = TelegramClient(StringSession(config.SESSION), config.API_ID, config.API_HASH)

# --- [3] ميزة سحب الأعضاء (التي طلبتها) ---
@client.on(events.NewMessage(outgoing=True, pattern=r'\.سحب (.*)'))
async def get_members(event):
    chat_id = event.pattern_match.group(1)
    await event.edit(f"**⏳ جاري سحب الأعضاء من: {chat_id}...**")
    try:
        full_chat = await client(GetFullChannelRequest(chat_id))
        members = await client.get_participants(full_chat.full_chat.id)
        await event.edit(f"**✅ تم سحب `{len(members)}` عضو بنجاح.**")
    except Exception as e:
        await event.edit(f"**❌ خطأ: {e}**")

# --- [4] رد الخاص التلقائي والآيدي بالصورة ---
@client.on(events.NewMessage(incoming=True))
async def private_guard(event):
    if event.is_private and event.sender_id not in SUDO_USERS:
        await client.send_file(event.chat_id, REBEL_IMG, caption=f"**{REBEL_TITLE}**\n\n- معقل المتمرد التقني.. انتظر الرد.\n{REBEL_LINK}") #

@client.on(events.NewMessage(outgoing=True))
async def control_panel(event):
    if event.raw_text == ".ايدي":
        reply = await event.get_reply_message()
        target = reply.sender if reply else await event.get_sender()
        photo = await client.download_profile_photo(target.id) #
        await client.send_file(event.chat_id, photo or REBEL_IMG, caption=f"🆔 الايدي: `{target.id}`")
        await event.delete()
    
    elif event.raw_text == ".فحص":
        await event.edit("**🛡️ درع المتمرد نشط.. ميزة السحب مفعلة.**") #

# --- [5] استدعاء ملفات الجروبات (Plugins) ---
def load_plugins():
    for name in glob.glob("plugins/*.py"):
        shortname = Path(name).stem
        try:
            importlib.import_module(f"plugins.{shortname}") #
            print(f"✅ تم تحميل: {shortname}")
        except: pass

async def start_rebel():
    await client.start()
    load_plugins() #
    print("🛡️ REBEL SOURCE LOADED WITH SCRAPER")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(start_rebel())
