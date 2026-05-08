import asyncio, os, pytz, glob, re, json, threading, random, importlib
from datetime import datetime
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
import google.generativeai as genai
import config 

# --- [ AL-MUTAMARRID GLOBAL BRAND ] ---
# الهوية الموحدة التي ستظهر في كل الملفات
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"

# --- [ إعدادات المعقل والعقل ] ---
LOG_GROUP_ID = -1003586994898 
DB_FILE = "rebel_security.json"
YEMEN_TZ = pytz.timezone('Asia/Aden')
SUDO_USERS = [6467728995] 
REBEL_IMG = "https://telegra.ph/file/058204663f73359d997f0.jpg"

# بصمة المتمرد (REBEL_SIG) المحدثة بالهوية الجديدة
REBEL_SIG = (
    "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗬𝗦𝗧𝗘𝗠 🦅**\n"
    "**— — — — — — — — — — — —**\n"
    "**حيث يلتقي التشفير بالذكاء، والتمرد بالواقع.**\n"
    "**سورس وُجد ليكون الأول، والبقية مجرد محاولات.**\n"
    "**أمانٌ لا يُخترق، وهيبةٌ لا تُهزم.**\n"
    "**— — — — — — — — — — — —**"
)

CMD_HELP = {} # قاموس تخزين الأوامر المسحوبة من plugins

# إعداد الذكاء الاصطناعي (Gemini)
genai.configure(api_key="AIzaSyDwzx1U-IGgw-Kybz2RVt2N-xtkWrIt7aU")
model = genai.GenerativeModel('gemini-pro')

# استضافة سريعة لضمان بقاء السورس حياً (Health Check)
app = Flask(__name__)
@app.route('/')
def health_check(): return "🛡️ Rebel Source is Live"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()

# إقلاع العميل (Telegram Client)
client = TelegramClient(StringSession(config.SESSION), config.API_ID, config.API_HASH)

# --- [ محرك سحب الملفات الذكي ] ---
async def load_plugins():
    path = "plugins/*.py"
    files = glob.glob(path)
    for name in files:
        # تحويل المسار إلى صيغة موديول بايثون
        module_name = name.replace(".py", "").replace("/", ".").replace("\\", ".")
        try:
            importlib.import_module(module_name)
            print(f"✅ 𝗟𝗢𝗔𝗗𝗘𝗗: {os.path.basename(name)}")
        except Exception as e:
            print(f"❌ 𝗘𝗥𝗥𝗢𝗥 𝗜𝗡 {name}: {e}")

# دالة تحويل الأرقام إلى خط عريض فخم
def z_nums(text):
    n = {'0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'}
    return "".join(n.get(c, c) for c in text)

# --- [ تحديث أمر الأوامر الشامل ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.الاوامر"))
async def rebel_cmds(event):
    header = f"**🛡️ 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗖𝗠𝗗𝗦 🦅**\n**— — — — — — — — — — — —**\n"
    body = ""
    # سحب الأوامر من الملفات التي تم تحميلها (plugins)
    for plugin, cmds in CMD_HELP.items():
        body += f"📦 **حزمة: {plugin}**\n"
        for cmd in cmds:
            body += f" ⇐ `.{cmd}`\n"
        body += "— — —\n"
    
    if not body: 
        body = "**⚠️ لم يتم العثور على حزم إضافية.**\n"
    
    total_pkgs = z_nums(str(len(CMD_HELP)))
    footer = f"**— — — — — — — — — — — —**\n**📊 الإجمالي: {total_pkgs} حـزم مسحوبة**"
    await event.edit(f"{header}{body}{footer}\n\n{REBEL_SIG}")

# --- [ إقلاع السورس والمهام التلقائية ] ---
async def start_rebel():
    await client.start()
    await load_plugins() # تشغيل محرك السحب عند الإقلاع
    
    # تحديث اسم الحساب بالوقت تلقائياً (بتوقيت اليمن)
    async def time_updater():
        while True:
            try:
                # جلب معلومات المستخدم
                me = await client.get_me()
                current_name = me.first_name.split('|')[0].strip()
                # جلب الوقت الحالي بتوقيت اليمن السعيد
                tm = z_nums(datetime.now(YEMEN_TZ).strftime("%I:%M"))
                await client(UpdateProfileRequest(first_name=f"{current_name} | {tm}"))
            except: pass
            await asyncio.sleep(300) # التحديث كل 5 دقائق
            
    asyncio.create_task(time_updater())
    print("🦅 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗜𝗦 𝗢𝗡𝗟𝗜𝗡𝗘!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(start_rebel())
