import asyncio, os, pytz, glob, importlib, sys, re
from datetime import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
import config 

# --- واجهة المتمرد السيبرانية (ASCII ART) ---
REBEL_LOGO = """
       .---.        🛡️ THE REBEL CYBER SOURCE 🛡️
      /     \       ---------------------------
      | 0 0 |       [#] STATUS: INVINCIBLE
      |  ^  |       [#] LOGIC: QUANTUM REBEL
      / \_  /       [#] RULE: NO MERCY FOR BUGS
    ./ /   \ \.     ---------------------------
   / /       \ \    "القمة تتسع للمتمرد فقط.."
"""

# --- كود إرضاء منصة ريندر ---
from flask import Flask
import threading

app = Flask(__name__)
@app.route('/')
def health_check():
    return "The Rebel UserBot is Live! 🦅"

def run_flask():
    try:
        app.run(host='0.0.0.0', port=10000)
    except: pass

threading.Thread(target=run_flask, daemon=True).start()

# --- تعريف الكلاينت ---
SESSION_STRING = config.SESSION 
client = TelegramClient(StringSession(SESSION_STRING), config.API_ID, config.API_HASH)

def z_nums(text):
    n = {'0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'}
    return "".join(n.get(c, c) for c in text)

# --- نظام كشف الأوامر المتطور مع الحقوق ---
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.الاوامر"))
async def help_engine(event):
    all_commands = []
    files = ["main.py"] + glob.glob("plugins/*.py")
    
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                found = re.findall(r'pattern=r"\\\.([\w_]+)"', content)
                if found: all_commands.extend(found)
        except: continue

    unique_cmds = sorted(list(set(all_commands)))
    
    # جلب المعرفات وتنظيفها لضمان عمل الروابط
    owner1 = getattr(config, 'OWNER_1', 'Vi_ti0').replace("@", "")
    owner2 = getattr(config, 'OWNER_2', 'A0_O7').replace("@", "")

    msg = "**🛡️ معقل المتمرد: حيث يلتقي التشفير بالذكاء 🦅**\n"
    msg += "— — — — — — — — — — — — —\n"
    msg += "**نحن لا نحمي بياناتك فقط، نحن نمنحك القوة.**\n"
    msg += "— — — — — — — — — — — — —\n"
    
    for i, cmd in enumerate(unique_cmds, 1):
        # استخدام دالة تحويل الأرقام لجعل القائمة فخمة
        msg += f"**{z_nums(str(i))} ⇐** `.{cmd}`\n"
    
    msg += "— — — — — — — — — — — — —\n"
    msg += f"**👤 المطور الأول ⇐ [تواصل هنا](https://t.me/{owner1})**\n"
    msg += f"**👤 المطور الثاني ⇐ [تواصل هنا](https://t.me/{owner2})**\n"
    msg += "— — — — — — — — — — — — —\n"
    msg += f"**📊 الإجمالي: {z_nums(str(len(unique_cmds)))} حزمة برمجية شغّالة**"
    
    await event.edit(msg, link_preview=False)

# --- محرك البروفايل الذكي ---
async def profile_engine():
    while True:
        try:
            me = await client.get_me()
            full_name = me.first_name if me.first_name else "المتمرد"
            if " | " in full_name:
                clean_name = full_name.rsplit(" | ", 1)[0]
            else:
                clean_name = full_name
            tm = z_nums(datetime.now(config.YEMEN_TZ).strftime("%I:%M"))
            await client(UpdateProfileRequest(first_name=f"{clean_name} | {tm}"))
            await asyncio.sleep(300)
        except Exception:
            await asyncio.sleep(300)

def load_plugins():
    if not os.path.exists("plugins"):
        os.makedirs("plugins")
    for name in glob.glob("plugins/*.py"):
        plugin_name = name.replace("/", ".").replace("\\", ".").replace(".py", "")
        if "__init__" in plugin_name: continue
        try:
            importlib.import_module(plugin_name)
        except Exception: pass

async def start_mared():
    # طباعة الشعار في الكونسول عند البداية
    print(REBEL_LOGO)
    print("🚀 [SYSTEM]: جاري فحص أنظمة التشفير...")
    print("🦅 [SUCCESS]: معقل المتمرد تحت السيطرة الكاملة.")
    
    await client.start()
    load_plugins()
    asyncio.create_task(profile_engine())
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        client.loop.run_until_complete(start_mared())
    except (KeyboardInterrupt, SystemExit):
        pass
