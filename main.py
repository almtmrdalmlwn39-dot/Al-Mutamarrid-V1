import asyncio, os, pytz, glob, importlib, sys, re, json, threading
from datetime import datetime
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
import google.generativeai as genai
import config 

# --- [1] الهوية والذكاء الاصطناعي ---
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

# --- [3] محرك الأوامر والايدي بالصورة ---
@client.on(events.NewMessage(outgoing=True))
async def rebel_main_engine(event):
    text = event.text
    data = load_data()
    
    # --- أمر الايدي بالصورة ---
    if text.startswith(".ايدي"):
        reply = await event.get_reply_message()
        target = reply.sender if reply else await event.get_sender()
        
        # تحديد الرتبة
        rank = "المالك" if target.id in SUDO_USERS else "عضو"
        if event.is_group:
            permissions = await client.get_permissions(event.chat_id, target)
            if permissions.is_admin: rank = "أدمن"
            if permissions.is_creator: rank = "المالك"

        info = f"**👤 الاسم:** {target.first_name}\n"
        info += f"**🆔 الايدي:** `{target.id}`\n"
        info += f"**🎖️ الرتبة:** {rank}\n"
        info += f"**🦅 السورس:** المتمرد التقني\n\n{REBEL_SIG_TEXT}"
        
        try:
            photo = await client.download_profile_photo(target.id)
            await client.send_file(event.chat_id, photo, caption=info, reply_to=reply.id if reply else event.id)
            if photo: os.remove(photo)
            await event.delete()
        except:
            await event.edit(info)

    # --- عرض الأوامر ---
    elif text == ".الاوامر":
        new_cmds = ["تفعيل الحماية", "تعطيل الحماية", "سماح", "حظر", "فك حظر", "ايدي", "فحص"]
        plugin_cmds = []
        files = ["main.py"] + glob.glob("plugins/*.py") + glob.glob("plugins/*/*.py")
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    found = re.findall(r'pattern=r"[\\/.]+\.([\w_]+)"', content)
                    if not found: found = re.findall(r'pattern=r"\\\.([\w_]+)"', content)
                    if found: plugin_cmds.extend(found)
            except: continue
        
        all_list = sorted(list(set(new_cmds + plugin_cmds)))
        msg = f"**🛡️ معقل المتمرد: حيث يلتقي التشفير بالذكاء 🦅**\n— — —\n{REBEL_SIG_TEXT}\n— — —\n"
        for i, cmd in enumerate(all_list, 1):
            msg += f"**{z_nums(str(i))} ⇐** `.{cmd}`\n"
        msg += f"— — —\n**📊 الإجمالي: {z_nums(str(len(all_list)))} حزمة برمجية شغّالة**"
        await event.edit(msg, link_preview=False)

# --- [4] نظام الحماية والعد الصحيح في الخاص ---
@client.on(events.NewMessage(incoming=True))
async def security_logic(event):
    if not event.is_private: return
    data = load_data()
    user_id = event.sender_id
    
    sender = await event.get_sender()
    f_name = sender.first_name if sender.first_name else "المستخدم"

    if user_id in SUDO_USERS or user_id in data.get("allowed", []) or user_id == (await client.get_me()).id: return
    if not data.get("status"): return
    
    # تحديث العداد وحفظه فوراً
    u_str = str(user_id)
    counts = data.get("counts", {})
    count = counts.get(u_str, 0) + 1
    counts[u_str] = count
    data["counts"] = counts
    save_data(data)

    if count == 1:
        msg = f"**يا {f_name}، مرحباً بك في معقل المتمرد 🛡️**\n**⚠️ تحذير ({z_nums(str(count))}/٥): يمنع التكرار.**\n\n{REBEL_SIG_TEXT}"
        await client.send_file(event.chat_id, REBEL_IMG, caption=msg)
    elif count < 5:
        prompt = f"رد بلهجة يمنية فخمة ترحب بالضيف وتذكره أن التكرار ممنوع. الرسالة: {event.text}"
        try:
            res = model.generate_content(prompt)
            reply = res.text
        except: reply = "أهلاً بك، التكرار ممنوع في معقلنا."
        
        full_msg = f"**يا {f_name}.. {reply}**\n**⚠️ تنبيه ({z_nums(str(count))}/٥)**\n\n{REBEL_SIG_TEXT}"
        await client.send_file(event.chat_id, REBEL_IMG, caption=full_msg)
    elif count >= 5:
        await event.reply(f"**🚫 تم حظرك لتجاوزك حد التكرار.**")
        await client(functions.contacts.BlockRequest(id=user_id))

# --- [5] التشغيل وتحميل الإضافات ---
async def start_rebel():
    await client.start()
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
