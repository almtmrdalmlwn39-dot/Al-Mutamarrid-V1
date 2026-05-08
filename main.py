import asyncio, os, pytz, glob, re, json, threading, random, importlib.util
from datetime import datetime
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
import config 

# --- [ AL-MUTAMARRID TECH GLOBAL IDENTITY ] ---
# الهوية الإنجليزية الفخمة للسورس
REBEL_NAME = "𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗧𝗘𝗖𝗛"
WAR_IDENTITY = f"**𓄂 {REBEL_NAME} 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"

# 1. التعريفات الأساسية (إصلاح NameError)
CMD_HELP = {}
client = TelegramClient(StringSession(config.SESSION), config.API_ID, config.API_HASH)

# 2. قائمة الأوامر الرئيسية (باسم المتمرد التقني)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.الاوامر"))
async def rebel_super_menu(event):
    msg = f"ᯓ **{REBEL_NAME} - قـائمة الأوامـر الـعـامـة** 𓆪\n"
    msg += "⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
    plugins = sorted(CMD_HELP.keys())
    if not plugins:
        msg += "⚠️ يرجى التأكد من رفع ملفات الـ plugins بشكل صحيح."
    for i, plugin in enumerate(plugins, 1):
        msg += f" **.م{i}** ➪ **أوامـر {plugin}**\n"
    msg += "\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
    msg += f"{WAR_IDENTITY}"
    await event.edit(msg)

# 3. محرك تحميل الإضافات (Plugins Loader)
async def load_plugins():
    path = "plugins/*.py"
    files = glob.glob(path)
    for name in files:
        module_name = os.path.basename(name).replace(".py", "")
        try:
            spec = importlib.util.spec_from_file_location(module_name, name)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            # ربط أوامر الملفات (مثل ملف الخصوصية والحماية)
            if hasattr(mod, 'CMD_HELP'):
                CMD_HELP.update(mod.CMD_HELP)
        except Exception as e:
            print(f"❌ Error loading {module_name}: {e}")

# 4. دالة الإقلاع (باسم المتمرد إنجليزي) 🚀
async def start_rebel():
    # طباعة بدء التشغيل بالاسم الإنجليزي الفخم
    print(f"🛡️ {REBEL_NAME} IS STARTING...") 
    
    await client.start()
    await load_plugins()
    
    me = await client.get_me()
    # طباعة الجاهزية في سجلات السيرفر
    print(f"✅ {REBEL_NAME} IS READY | Account: {me.first_name}") 
    
    await client.run_until_disconnected()

if __name__ == '__main__':
    # إنشاء سيرفر Flask وهمي لتخطي إغلاق الاستضافات (Render)
    app = Flask(__name__)
    @app.route('/')
    def index(): return f"{REBEL_NAME} ONLINE 🛡️"
    
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()
    
    # تشغيل الدورة البرمجية للسورس
    client.loop.run_until_complete(start_rebel())
