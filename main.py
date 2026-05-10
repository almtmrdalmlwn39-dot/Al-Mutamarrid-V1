import asyncio, os, pytz, glob, re, json, threading, random, importlib.util, sys
from config import SUDO_USERS, API_ID, API_HASH, SESSION
from datetime import datetime
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession

# 🌟 السطر السحري الذي يمنع استنساخ البوت ويربط الإضافات بالمحرك الحقيقي 🌟
sys.modules['main'] = sys.modules['__main__']

# --- [ 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗧𝗘𝗖𝗛 𝗚𝗟𝗢𝗕𝗔𝗟 𝗜𝗗𝗘𝗡𝗧𝗜𝗧𝗬 ] ---
REBEL_NAME = "𝗔𝗟-𝗠𝗨𝗧𝗔ﻣ𝗔𝗥𝗥𝗜𝗗 𝗧𝗘𝗖𝗛"
WAR_IDENTITY = f"**🛡️ {REBEL_NAME} 𝗦𝗢𝗨𝗥𝗖𝗘 🦅**"

# روابط الحقوق (تم التصحيح والربط المباشر)
CH_LINK = "https://t.me/bedmoddinnow"
DEV1 = "https://t.me/Vi_ti0"
DEV2 = "https://t.me/A0_O7" # تم حذف الشرطة الزائدة ليعمل الرابط فوراً

# 1. التعريفات الأساسية
CMD_HELP = {}
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# 2. قائمة الأوامر الرئيسية (تم إضافة الحقوق والروابط هنا)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.الاوامر"))
async def rebel_super_menu(event):
    msg = f"ᯓ **{REBEL_NAME} - قـائمة الأقـسام الـعـامة** 𓆪\n"
    msg += "⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
    plugins = sorted(CMD_HELP.keys())
    if not plugins:
        msg += "⚠️ يرجى التأكد من رفع ملفات الـ plugins بشكل صحيح."
    for i, plugin in enumerate(plugins, 1):
        msg += f" **.م{i}** ➪ **أوامـر {plugin}**\n"
    msg += "⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
    msg += f"**📢 الـقـناة ⇐ [اضـغط هـنا]({CH_LINK})**\n"
    msg += f"**👤 الـمطور 1 ⇐ [الـمتمرد]({DEV1})**\n"
    msg += f"**👤 الـمطور 2 ⇐ [الـمتمرد]({DEV2})**\n"
    msg += "⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
    msg += f"{WAR_IDENTITY}"
    await event.edit(msg, link_preview=False)

# 3. محرك تشغيل الأوامر الفرعية
@client.on(events.NewMessage(outgoing=True, pattern=r"\.م(\d+)"))
async def rebel_sub_menu(event):
    plugin_index = int(event.pattern_match.group(1)) - 1
    plugins = sorted(CMD_HELP.keys())
    if 0 <= plugin_index < len(plugins):
        plugin_name = plugins[plugin_index]
        help_text = "\n".join(CMD_HELP[plugin_name]) if isinstance(CMD_HELP[plugin_name], list) else CMD_HELP[plugin_name]
        msg = f"ᯓ **أوامـر {plugin_name}** 𓆪\n\n{help_text}\n\n"
        msg += f"**👤 الـمطور ⇐ [اضـغط هـنا]({DEV1})**\n"
        msg += f"{WAR_IDENTITY}"
        await event.edit(msg, link_preview=False)

# 4. محرك تحميل الإضافات (Plugins Loader)
async def load_plugins():
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
            print(f"✅ تم تحميل الإضافة بنجاح: {module_name}")
        except Exception as e:
            print(f"❌ خطأ في تحميل {module_name}: {e}")

# 5. دالة الإقلاع
async def start_rebel():
    print(f"🛡️ {REBEL_NAME} IS STARTING...") 
    await client.start()
    await load_plugins()
    me = await client.get_me()
    print(f"✅ {REBEL_NAME} READY | Account: {me.first_name}") 
    await client.run_until_disconnected()

# 6. سيرفر ويب (Flask) للإبقاء على السورس حياً
def run_flask():
    app = Flask(__name__)
    @app.route('/')
    def index(): return f"{REBEL_NAME} ONLINE 🛡️"
    try:
        port = int(os.environ.get("PORT", 10000))
        app.run(host='0.0.0.0', port=port)
    except:
        app.run(host='0.0.0.0', port=random.randint(8000, 9000))

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    try:
        client.loop.run_until_complete(start_rebel())
    except Exception as e:
        print(f"🔥 Critical Startup Error: {e}")
