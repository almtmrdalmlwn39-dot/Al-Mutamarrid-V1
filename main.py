import asyncio, os, pytz, glob, re, json, threading, random, importlib.util
from config import SUDO_USERS, API_ID, API_HASH, SESSION # استدعاء مباشر للبيانات
from datetime import datetime
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession

# --- [ 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗧𝗘𝗖𝗛 𝗚𝗟𝗢𝗕𝗔𝗟 𝗜𝗗𝗘𝗡𝗧𝗜𝗧𝗬 ] ---
REBEL_NAME = "𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗧𝗘𝗖𝗛"
# هذه العبارة ستظهر فقط في قائمة الأوامر كما طلبت
WAR_IDENTITY = f"**𓄂 {REBEL_NAME} 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"

# 1. التعريفات الأساسية وتشغيل الجلسة
CMD_HELP = {}
# تم تصحيح استدعاء الجلسة والـ API ليعمل مع ملف config الجديد
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# 2. قائمة الأوامر الرئيسية (.الاوامر)
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
    msg += f"{WAR_IDENTITY}" # هنا تظهر الحقوق
    await event.edit(msg)

# 3. محرك تشغيل الأوامر الفرعية (.م1، .م2 ..الخ)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.م(\d+)"))
async def rebel_sub_menu(event):
    plugin_index = int(event.pattern_match.group(1)) - 1
    plugins = sorted(CMD_HELP.keys())
    if 0 <= plugin_index < len(plugins):
        plugin_name = plugins[plugin_index]
        help_text = CMD_HELP[plugin_name]
        await event.edit(f"ᯓ **أوامـر {plugin_name}** 𓆪\n\n{help_text}\n\n{WAR_IDENTITY}")

# 4. محرك تحميل الإضافات (Plugins Loader)
async def load_plugins():
    # التأكد من وجود مجلد plugins
    if not os.path.exists("plugins"):
        os.makedirs("plugins")
    path = "plugins/*.py"
    files = glob.glob(path)
    for name in files:
        module_name = os.path.basename(name).replace(".py", "")
        try:
            spec = importlib.util.spec_from_file_location(module_name, name)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, 'CMD_HELP'):
                CMD_HELP.update(mod.CMD_HELP)
        except Exception as e:
            print(f"❌ Error loading {module_name}: {e}")

# 5. دالة الإقلاع وفحص الحساب 🚀
async def start_rebel():
    print(f"🛡️ {REBEL_NAME} IS STARTING...") 
    try:
        await client.start()
        await load_plugins()
        me = await client.get_me()
        print(f"✅ {REBEL_NAME} IS READY | Account: {me.first_name}") 
        # إضافة إشعار بسيط عند التشغيل (اختياري)
        # await client.send_message("me", f"✅ تم تشغيل سورس {REBEL_NAME} بنجاح!")
    except Exception as e:
        print(f"❌ Failed to start: {e}")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # تشغيل Flask لتجنب إغلاق Render للبوت
    app = Flask(__name__)
    @app.route('/')
    def index(): return f"{REBEL_NAME} ONLINE 🛡️"
    
    port = int(os.environ.get("PORT", 10000))
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port), daemon=True).start()
    
    # تشغيل البوت
    client.loop.run_until_complete(start_rebel())
