import asyncio, os, pytz, glob, re, json, threading, random, importlib
from datetime import datetime
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
import google.generativeai as genai
import config 

# --- [1] إعدادات المعقل والعقل ---
LOG_GROUP_ID = -1003586994898 
DB_FILE = "rebel_security.json"
YEMEN_TZ = pytz.timezone('Asia/Aden')
SUDO_USERS = [6467728995] 
REBEL_IMG = "https://telegra.ph/file/058204663f73359d997f0.jpg"
REBEL_SIG = "معقل المتمرد: #حيث_يلتقي_التشفير_بالذكاء، والتمرد بالواقع. سورس وُجد ليكون الأول، والبقية مجرد محاولات. نحن لا نحمي بياناتك فقط، نحن نمنحك القوة لتكون السيد في عالم لا يعترف إلا بالأقوياء. المتمرد.. أمانٌ لا يُخترق، وهيبةٌ لا تُهزم."
CMD_HELP = {} # قاموس تخزين الأوامر المسحوبة

genai.configure(api_key="AIzaSyDwzx1U-IGgw-Kybz2RVt2N-xtkWrIt7aU")
model = genai.GenerativeModel('gemini-pro')

app = Flask(__name__)
@app.route('/')
def health_check(): return "🛡️ Rebel Source is Live"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()

client = TelegramClient(StringSession(config.SESSION), config.API_ID, config.API_HASH)

# --- [ نظام سحب الملفات الذكي ] ---
async def load_plugins():
    path = "plugins/*.py"
    files = glob.glob(path)
    for name in files:
        module_name = name.replace(".py", "").replace("/", ".").replace("\\", ".")
        try:
            importlib.import_module(module_name)
            print(f"✅ تم سحب ملف: {os.path.basename(name)}")
        except Exception as e:
            print(f"❌ خطأ في سحب {name}: {e}")

def z_nums(text):
    n = {'0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'}
    return "".join(n.get(c, c) for c in text)

# (احتفظ بدوال load_data و save_data و get_franco_reply كما هي في كودك)

# --- [ تحديث أمر الأوامر ليقرأ من المجلدات ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.الاوامر"))
async def rebel_cmds(event):
    header = f"**🛡️ معقل المتمرد: القائمة الشاملة 🦅**\n— — — — — — — — — — —\n"
    body = ""
    # سحب الأوامر من الملفات التي تم تحميلها
    for plugin, cmds in CMD_HELP.items():
        body += f"📦 **حزمة: {plugin}**\n"
        for cmd in cmds:
            body += f" ⇐ `.{cmd}`\n"
        body += "— — —\n"
    
    if not body: body = "**⚠️ لم يتم العثور على حزم إضافية في المجلدات.**\n"
    
    footer = f"— — — — — — — — — — —\n**📊 الإجمالي: {z_nums(str(len(CMD_HELP)))} حزم مسحوبة**"
    await event.edit(header + body + footer + f"\n\n`{REBEL_SIG}`")

# --- [ إقلاع السورس ] ---
async def start_rebel():
    await client.start()
    await load_plugins() # تشغيل محرك السحب عند الإقلاع
    
    # تحديث الوقت تلقائياً
    async def time_updater():
        while True:
            try:
                tm = z_nums(datetime.now(YEMEN_TZ).strftime("%I:%M"))
                await client(UpdateProfileRequest(first_name=f"المتمرد | {tm}"))
            except: pass
            await asyncio.sleep(300)
            
    asyncio.create_task(time_updater())
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(start_rebel())
