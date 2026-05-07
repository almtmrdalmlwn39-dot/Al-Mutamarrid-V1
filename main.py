import asyncio, os, json, threading, re, glob, importlib
from pathlib import Path
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
import config 

# [1] السيرفر لضمان البقاء متصلاً (Live)
app = Flask(__name__)
@app.route('/')
def health_check(): return "🛡️ Rebel is Live"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()

# [2] الهوية والإعدادات
REBEL_TITLE = "┃ الأمن السيبراني 🛡️"
REBEL_IMG = "https://telegra.ph/file/058204663f73359d997f0.jpg"
REBEL_LINK = "👤 **المطور:** [المتمرد](https://t.me/Vi_ti0)"
SUDO_USERS = [6467728995] 

# تعريف الـ client هنا بشكل عالمي ليراه الجميع
client = TelegramClient(StringSession(config.SESSION), config.API_ID, config.API_HASH)

# --- [3] رد الخاص التلقائي (الذي سألت عنه) ---
@client.on(events.NewMessage(incoming=True))
async def private_reply(event):
    if not event.is_private: return
    if event.sender_id in SUDO_USERS: return
    # إرسال الصورة والترحيب فور مراسلتك في الخاص
    await client.send_file(event.chat_id, REBEL_IMG, caption=f"**{REBEL_TITLE}**\n\n- مرحباً بك في معقل المتمرد.. انتظر الرد.\n{REBEL_LINK}")

# --- [4] الآيدي بالصورة وأوامر السيطرة ---
@client.on(events.NewMessage(outgoing=True))
async def control_panel(event):
    text = event.raw_text
    
    if text == ".ايدي":
        reply = await event.get_reply_message()
        target = reply.sender if reply else await event.get_sender()
        # جلب صورة الشخص وإرسالها مع الآيدي
        photo = await client.download_profile_photo(target.id)
        await client.send_file(event.chat_id, photo or REBEL_IMG, caption=f"🆔 الايدي: `{target.id}`")
        await event.delete()

    elif text == ".فحص":
        await event.edit(f"**🛡️ درع المتمرد نشط.. تم فحص النظام والملفات الخارجية بنجاح.**")

    elif text == ".الاوامر":
        msg = f"**{REBEL_TITLE}**\n— — —\n`.فحص` | `.ايدي` | `.الاوامر` \n— — —\n{REBEL_LINK}"
        await client.send_file(event.chat_id, REBEL_IMG, caption=msg)
        await event.delete()

# --- [5] محرك استدعاء أوامر الجروبات (Plugins) ---
def load_plugins():
    path = "plugins/*.py"
    for name in glob.glob(path):
        shortname = Path(name).stem
        try:
            # ربط الملفات الخارجية (مثل rebel_tech) بالسورس
            importlib.import_module(f"plugins.{shortname}")
            print(f"✅ تم تحميل: {shortname}")
        except Exception as e:
            print(f"❌ خطأ في {shortname}: {e}")

async def start_rebel():
    await client.start()
    # تحميل الإضافات بعد الـ start يضمن أن الـ client جاهز للعمل
    load_plugins()
    print("🛡️ REBEL SOURCE LOADED SUCCESSFULLY")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(start_rebel())
