import asyncio, os, pytz, glob, importlib, sys, re, json, threading
from datetime import datetime
from flask import Flask
from telethon import TelegramClient, events, functions
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
import google.generativeai as genai
import config 

# --- [1] واجهة المتمرد السيبرانية (ASCII ART) ---
REBEL_LOGO = """
       .---.        🛡️ THE REBEL CYBER SOURCE 🛡️
      /     \       ---------------------------
      | 0 0 |       [#] STATUS: INVINCIBLE
      |  ^  |       [#] LOGIC: QUANTUM REBEL
      / \_  /       [#] RULE: NO MERCY FOR BUGS
    ./ /   \ \.     ---------------------------
   "القمة تتسع للمتمرد فقط.."
"""

# إعداد عقل فرانكو (الذكاء الاصطناعي)
genai.configure(api_key="AIzaSyDwzx1U-IGgw-Kybz2RVt2N-xtkWrIt7aU")
model = genai.GenerativeModel('gemini-pro')

# --- [2] إعدادات الحماية والتخزين وريندر ---
DB_FILE = "rebel_security.json"
LOG_GROUP_ID = -1003586994898 
SUDO_USERS = [6467728995] 
REBEL_IMG = "https://telegra.ph/file/058204663f73359d997f0.jpg"

app = Flask(__name__)
@app.route('/')
def health_check(): return "The Rebel UserBot is Live! 🦅"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()

client = TelegramClient(StringSession(config.SESSION), config.API_ID, config.API_HASH)

def z_nums(text):
    n = {'0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'}
    return "".join(n.get(c, c) for c in text)

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: pass
    return {"status": True, "counts": {}, "allowed": [], "storage": True}

def save_data(data):
    with open(DB_FILE, "w") as f: json.dump(data, f)

async def get_franco_reply(user_msg):
    prompt = f"أنت مطور يمني ذكي. رد بلهجة يمنية قوية ومختصرة جداً. الرسالة: {user_msg}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except: return "منعاه لا تزيد بالهرج."

# --- [3] محرك الأوامر (العبارة الفخمة + الحسابات + 56 حزمة) ---
@client.on(events.NewMessage(outgoing=True))
async def rebel_main_engine(event):
    text = event.text
    data = load_data()
    reply = await event.get_reply_message()

    # أوامر التحكم الـ 11 الجديدة
    new_cmds = ["تفعيل الحماية", "تعطيل الحماية", "انشاء تخزين", "ايدي", "فحص", "طرد"]

    if text == ".تفعيل الحماية":
        data["status"] = True
        save_data(data)
        return await event.edit("**🛡️ تم تفعيل نظام حماية المتمرد بنجاح.**")
    
    if text == ".انشاء تخزين":
        data["storage"] = True
        save_data(data)
        return await event.edit(f"**✅ تم ربط التخزين بالقروب: `{LOG_GROUP_ID}`**")

    # أمر الآيدي المطور (لا يحذف)
    if text.startswith((".ايدي", ".فحص")):
        target_id = reply.sender_id if reply else event.sender_id
        await event.edit(f"**💳 الآيـدي: `{target_id}`**")
        return

    # عرض القائمة الشاملة
    if text == ".الاوامر":
        plugin_cmds = []
        files = ["main.py"] + glob.glob("plugins/*.py")
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    found = re.findall(r'pattern=r"\\\.([\w_]+)"', f.read())
                    if found: plugin_cmds.extend([c.replace('_', ' ') for c in found])
            except: continue
        
        all_list = sorted(list(set(new_cmds + plugin_cmds)))
        owner1 = getattr(config, 'OWNER_1', 'Vi_ti0').replace("@", "")
        owner2 = getattr(config, 'OWNER_2', 'A0_O7').replace("@", "")

        msg = "**🛡️ معقل المتمرد: حيث يلتقي التشفير بالذكاء 🦅**\n"
        msg += "— — — — — — — — — — — — —\n"
        msg += "**نحن لا نحمي بياناتك فقط، نحن نمنحك القوة لتكون السيد في عالم لا يعترف إلا بالأقوياء. المتمرد.. أمانٌ لا يُخترق، وهيبةٌ لا تُهزم.**\n"
        msg += "— — — — — — — — — — — — —\n"
        for i, cmd in enumerate(all_list, 1):
            msg += f"**{z_nums(str(i))} ⇐** `.{cmd}`\n"
        msg += "— — — — — — — — — — — — —\n"
        msg += f"**👤 المطور الأول ⇐ [تواصل هنا](https://t.me/{owner1})**\n"
        msg += f"**📊 الإجمالي: {z_nums(str(len(all_list)))} حزمة**"
        await event.edit(msg, link_preview=False)

# --- [4] نظام الحماية والرد الذكي ---
@client.on(events.NewMessage(incoming=True))
async def security_logic(event):
    data = load_data()
    if event.chat_id == LOG_GROUP_ID or not event.is_private: return
    user_id = event.sender_id
    if user_id in SUDO_USERS: return

    if data.get("storage"):
        try: await client.send_message(LOG_GROUP_ID, f"**📥 رسالة من:** `{user_id}`\n**💬 النص:** {event.text}")
        except: pass

    if not data.get("status"): return
    u_str = str(user_id)
    counts = data.get("counts", {})
    count = counts.get(u_str, 0) + 1
    counts[u_str] = count
    data["counts"] = counts
    save_data(data)

    if count == 1:
        await event.reply("**⚠️ تحذير: يمنع التكرار في معقل المتمرد.**", file=REBEL_IMG)
    elif count < 5:
        franco_res = await get_franco_reply(event.text)
        await event.reply(f"**{franco_res}**", file=REBEL_IMG)
    elif count >= 5:
        await client(functions.contacts.BlockRequest(id=user_id))

# --- [5] الإقلاع وتحميل الإضافات ---
async def start_rebel():
    print(REBEL_LOGO)
    await client.start()
    
    async def profile_engine():
        while True:
            try:
                tz = getattr(config, 'YEMEN_TZ', pytz.timezone('Asia/Aden'))
                tm = z_nums(datetime.now(tz).strftime("%I:%M"))
                me = await client.get_me()
                clean_name = me.first_name.split(" | ")[0]
                await client(UpdateProfileRequest(first_name=f"{clean_name} | {tm}"))
            except: pass
            await asyncio.sleep(300)
    
    asyncio.create_task(profile_engine())

    # تحميل الإضافات (مثل ملف السحب) مع تمرير الكلاينت
    if os.path.exists("plugins"):
        for name in glob.glob("plugins/*.py"):
            path = name.replace("/", ".").replace("\\", ".").replace(".py", "")
            try:
                spec = importlib.util.spec_from_file_location(path, name)
                mod = importlib.util.module_from_spec(spec)
                mod.client = client 
                spec.loader.exec_module(mod)
            except: pass
            
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(start_rebel())
