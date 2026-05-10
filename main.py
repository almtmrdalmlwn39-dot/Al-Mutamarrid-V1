import asyncio, os, pytz, glob, re, json, threading, random, importlib.util, sys
from config import SUDO_USERS, API_ID, API_HASH, SESSION
from datetime import datetime
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession

# منع استنساخ البوت وربط الإضافات بالمحرك الحقيقي
sys.modules['main'] = sys.modules['__main__']

# --- [ AL-MUTAMARRID TECH GLOBAL IDENTITY ] ---
REBEL_NAME = "𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗧𝗘𝗖𝗛"
WAR_IDENTITY = f"**🛡️ {REBEL_NAME} 𝗦𝗢𝗨𝗥𝗖𝗘 🦅**"
CH_LINK = "https://t.me/bedmoddinnow"
DEV1 = "https://t.me/Vi_ti0"

# 1. التعريفات الأساسية
CMD_HELP = {}
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# 2. قائمة الأقسام الرئيسية (.الاوامر)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.الاوامر"))
async def rebel_super_menu(event):
    # ترتيب الأقسام أبجدياً لضمان الدقة
    plugins = sorted(CMD_HELP.keys())
    if not plugins:
        return await event.edit("**⚠️ مابش أي أقسام محملة حالياً.**")
        
    msg = f"ᯓ **{REBEL_NAME} - قـائمة الأقـسام** 𓆪\n"
    msg += "⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
    for i, plugin in enumerate(plugins, 1):
        msg += f" **.م{i}** ➪ **أوامـر {plugin}**\n"
    msg += "⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
    msg += f"**📢 الـقـناة ⇐ [اضـغط هـنا]({CH_LINK})**\n"
    msg += f"{WAR_IDENTITY}"
    await event.edit(msg, link_preview=False)

# 3. محرك الأوامر الفرعية (.م1، .م2...)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.م(\d+)"))
async def rebel_sub_menu(event):
    try:
        index = int(event.pattern_match.group(1)) - 1
        plugins = sorted(CMD_HELP.keys())
        if 0 <= index < len(plugins):
            p_name = plugins[index]
            h_text = "\n".join(CMD_HELP[p_name]) if isinstance(CMD_HELP[p_name], list) else CMD_HELP[p_name]
            msg = f"ᯓ **أوامـر {p_name}** 𓆪\n\n{h_text}\n\n{WAR_IDENTITY}"
            await event.edit(msg, link_preview=False)
    except: pass

# 4. محرك التحميل الذكي (المعدل للتنظيف)
async def load_plugins():
    # أهم خطوة: مسح المساعدة القديمة لضمان عدم ظهور "تسريع وتشكيلة"
    CMD_HELP.clear() 
    path = "plugins/*.py"
    files = glob.glob(path)
    for name in files:
        module_name = os.path.basename(name).replace(".py", "")
        try:
            spec = importlib.util.spec_from_file_location(module_name, name)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            # الربط الإجباري لعرض الأوامر في القائمة
            if hasattr(mod, 'CMD_HELP'):
                CMD_HELP.update(mod.CMD_HELP)
            print(f"✅ Loaded: {module_name}")
        except Exception as e:
            print(f"❌ Error in {module_name}: {e}")

async def start_rebel():
    await client.start()
    await load_plugins() # تحميل الإضافات وتسجيلها في القائمة
    print(f"🛡️ {REBEL_NAME} IS READY")
    await client.run_until_disconnected()

# سيرفر Flask للإبقاء على البوت حياً
def run_flask():
    app = Flask(__name__)
    @app.route('/')
    def index(): return "ONLINE"
    try:
        port = int(os.environ.get("PORT", 10000))
        app.run(host='0.0.0.0', port=port)
    except: pass

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    client.loop.run_until_complete(start_rebel())
