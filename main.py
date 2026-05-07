import asyncio, os, pytz, glob, importlib, sys, re, json, threading
from datetime import datetime
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
import google.generativeai as genai
import config 

# --- [1] الهوية والذكاء الاصطناعي ---
REBEL_LOGO = """
       .---.        🛡️ THE REBEL CYBER SOURCE 🛡️
      /     \       ---------------------------
      | 0 0 |       [#] STATUS: INVINCIBLE
      |  ^  |       [#] LOGIC: QUANTUM REBEL
      / \_  /       [#] RULE: NO MERCY FOR BUGS
    ./ /   \ \.     ---------------------------
   "القمة تتسع للمتمرد فقط.."
"""
# عبارتك الأصلية الفخمة
REBEL_SIG_TEXT = "**نحن لا نحمي بياناتك فقط، نحن نمنحك القوة لتكون السيد في عالم لا يعترف إلا بالأقوياء. المتمرد.. أمانٌ لا يُخترق، وهيبةٌ لا تُهزم.**"
REBEL_IMG = "https://telegra.ph/file/058204663f73359d997f0.jpg"

genai.configure(api_key="AIzaSyDwzx1U-IGgw-Kybz2RVt2N-xtkWrIt7aU")
model = genai.GenerativeModel('gemini-pro')

# --- [2] الإعدادات ---
DB_FILE = "rebel_security.json"
LOG_GROUP_ID = -1003586994898 
SUDO_USERS = [6467728995] 

app = Flask(__name__)
@app.route('/')
def health_check(): return "🛡️ Rebel Source is Live"
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
    prompt = f"أنت مطور يمني ذكي ومتمرد. رد بلهجة يمنية قوية ومختصرة جداً. الرسالة: {user_msg}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except: return "لا تزيد بالهرج فوق راسي."

# --- [3] محرك الأوامر الشامل (يحافظ على الشرطات وحساب العداد) ---
@client.on(events.NewMessage(outgoing=True))
async def rebel_main_engine(event):
    text = event.text
    data = load_data()
    reply = await event.get_reply_message()
    
    # أوامر مدمجة مع الحفاظ على الشرطات السفلية
    new_cmds = ["تفعيل_الحماية", "تعطيل_الحماية", "سماح", "حظر", "فك_حظر", "ايدي", "فحص"]

    if text == ".الاوامر":
        plugin_cmds = []
        files = ["main.py"] + glob.glob("plugins/*.py") + glob.glob("plugins/*/*.py")
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # البحث عن الأوامر بدون استبدال الشرطات السفلية
                    found = re.findall(r'pattern=r"[\\/.]+\.([\w_]+)"', content)
                    if not found:
                        found = re.findall(r'pattern=r"\\\.([\w_]+)"', content)
                    if found:
                        plugin_cmds.extend(found)
            except: continue
        
        all_list = sorted(list(set(new_cmds + plugin_cmds)))
        msg = f"**🛡️ معقل المتمرد: حيث يلتقي التشفير بالذكاء 🦅**\n— — —\n{REBEL_SIG_TEXT}\n— — —\n"
        for i, cmd in enumerate(all_list, 1):
            msg += f"**{z_nums(str(i))} ⇐** `.{cmd}`\n"
        msg += f"— — —\n**📊 الإجمالي: {z_nums(str(len(all_list)))} حزمة برمجية شغّالة**"
        await event.edit(msg, link_preview=False)

# --- [4] نظام الحماية المطور (اسم الشخص + الصورة + العبارة) ---
@client.on(events.NewMessage(incoming=True))
async def security_logic(event):
    if not event.is_private: return
    data = load_data()
    user_id = event.sender_id
    
    # سحب اسم الشخص للترحيب به
    sender = await event.get_sender()
    f_name = sender.first_name if sender.first_name else "عزيزي"

    if user_id in SUDO_USERS or user_id in data.get("allowed", []) or user_id == (await client.get_me()).id: return

    if data.get("storage"):
        try: await client.send_message(LOG_GROUP_ID, f"**📥 من:** `{f_name}` ({user_id})\n**💬 النص:** {event.text}")
        except: pass

    if not data.get("status"): return
    
    u_str = str(user_id)
    counts = data.get("counts", {})
    count = counts.get(u_str, 0) + 1
    counts[u_str] = count
    data["counts"] = counts
    save_data(data)

    # التحذير الأول مع الصورة والاسم
    if count == 1:
        warn_msg = f"**يا {f_name}، مرحباً بك في معقل المتمرد 🛡️**\n\n**⚠️ تحذير (1/5): يمنع التكرار هنا.**\n\n— — —\n{REBEL_SIG_TEXT}"
        try: 
            await client.send_file(event.chat_id, REBEL_IMG, caption=warn_msg, reply_to=event.id)
        except: await event.reply(warn_msg)
    
    # الرد الذكي (عقل فرانكو) مع الصورة والعبارة
    elif count < 5:
        franco_res = await get_franco_reply(event.text)
        reply_with_sig = f"**يا {f_name}.. {franco_res}**\n\n— — —\n{REBEL_SIG_TEXT}"
        try: 
            await client.send_file(event.chat_id, REBEL_IMG, caption=reply_with_sig, reply_to=event.id)
        except: await event.reply(reply_with_sig)
    
    # الحظر النهائي
    elif count >= 5:
        ban_msg = f"**🚫 يا {f_name}، تم حظرك نهائياً.**\n\n— — —\n{REBEL_SIG_TEXT}"
        await event.reply(ban_msg)
        await client(functions.contacts.BlockRequest(id=user_id))

# --- [5] الإقلاع وتحميل الإضافات ---
async def start_rebel():
    print(REBEL_LOGO)
    await client.start()
    
    async def profile_engine():
        while True:
            try:
                tz = pytz.timezone('Asia/Aden')
                tm = z_nums(datetime.now(tz).strftime("%I:%M"))
                me = await client.get_me()
                clean_name = me.first_name.split(" | ")[0]
                await client(UpdateProfileRequest(first_name=f"{clean_name} | {tm}"))
            except: pass
            await asyncio.sleep(300)
    
    asyncio.create_task(profile_engine())

    if os.path.exists("plugins"):
        for name in glob.glob("plugins/*.py") + glob.glob("plugins/*/*.py"):
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
