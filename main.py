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

# --- [2] الإعدادات والبيانات ---
DB_FILE = "rebel_security.json"
SUDO_USERS = [6467728995] 

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

# --- [3] محرك الأوامر (الايدي + المطور + القائمة) ---
@client.on(events.NewMessage(outgoing=True))
async def rebel_main_engine(event):
    text = event.text
    
    # 1. أمر الايدي بالصورة (بيانات صافية بدون العبارة)
    if text.startswith(".ايدي"):
        reply = await event.get_reply_message()
        target = reply.sender if reply else await event.get_sender()
        rank = "المالك" if target.id in SUDO_USERS else "عضو"
        if event.is_group:
            perms = await client.get_permissions(event.chat_id, target)
            if perms.is_admin: rank = "أدمن"

        info = f"**👤 الاسم:** {target.first_name}\n"
        info += f"**🆔 الايدي:** `{target.id}`\n"
        info += f"**🎖️ الرتبة:** {rank}\n"
        info += f"**🦅 السورس:** المتمرد التقني"
        
        try:
            photo = await client.download_profile_photo(target.id)
            if photo:
                await client.send_file(event.chat_id, photo, caption=info, reply_to=reply.id if reply else event.id)
                os.remove(photo)
                await event.delete()
            else: await event.edit(info)
        except: await event.edit(info)

    # 2. أمر القائمة مع الحسابات المدمجة نصياً كما في طلبك
    elif text == ".الاوامر":
        new_cmds = ["تفعيل الحماية", "تعطيل الحماية", "سماح", "حظر", "فك حظر", "ايدي", "مطور", "فحص", "تلفيش"]
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
        msg += f"— — —\n**📊 الإجمالي: {z_nums(str(len(all_list)))} حزمة برمجية شغّالة**\n\n"
        
        # تنسيق الحسابات المدمجة نصياً (شفافة داخل النص)
        msg += f"— — — — — — — — — — — —\n"
        msg += f"👤 المطور الأول ⇐ **[تواصل هنا](https://t.me/Vi_ti0)**\n"
        msg += f"👤 المطور الثاني ⇐ **[تواصل هنا](https://t.me/A0_O7)**\n"
        msg += f"— — — — — — — — — — — —"
        
        try:
            await client.send_file(event.chat_id, REBEL_IMG, caption=msg)
            await event.delete()
        except: await event.edit(msg, link_preview=False)

    # 3. أمر المطور المنفصل بنفس التنسيق
    elif text.startswith(".المطور") or text.startswith(".مطور"):
        dev_msg = f"**🦅 حسابات مطورين سورس المتمرد 🛡️**\n\n"
        dev_msg += f"— — — — — — — — — — — —\n"
        dev_msg += f"👤 المطور الأول ⇐ **[تواصل هنا](https://t.me/Vi_ti0)**\n"
        dev_msg += f"👤 المطور الثاني ⇐ **[تواصل هنا](https://t.me/A0_O7)**\n"
        dev_msg += f"— — — — — — — — — — — —\n**- القمة تتسع للمتمرد فقط..**"
        try:
            await client.send_file(event.chat_id, REBEL_IMG, caption=dev_msg)
            await event.delete()
        except: await event.reply(dev_msg)

# --- [4] نظام الحماية والعد المطور (الترحيب والعبارة في البداية فقط) ---
@client.on(events.NewMessage(incoming=True))
async def security_logic(event):
    if not event.is_private: return
    data = load_data()
    user_id = event.sender_id
    if user_id in SUDO_USERS or user_id == (await client.get_me()).id: return
    if not data.get("status"): return

    sender = await event.get_sender()
    f_name = sender.first_name if sender.first_name else "المستخدم"

    u_str = str(user_id)
    counts = data.get("counts", {})
    count = counts.get(u_str, 0) + 1
    counts[u_str] = count
    data["counts"] = counts
    save_data(data)

    if count == 1:
        # الترحيب الأول يحتوي على العبارة الطويلة
        msg = f"**يا {f_name}، مرحباً بك في معقل المتمرد 🛡️**\n**⚠️ تنبيه ({z_nums(str(count))}/٥): يمنع التكرار.**\n\n{REBEL_SIG_TEXT}"
        await client.send_file(event.chat_id, REBEL_IMG, caption=msg)
    elif count < 5:
        # التنبيهات التالية مختصرة وسريعة
        reply = "أهلاً بك، نرجو الالتزام بحدود الرسائل لضمان عدم الحظر."
        full_msg = f"**يا {f_name}.. {reply}**\n**⚠️ تنبيه ({z_nums(str(count))}/٥)**"
        await client.send_file(event.chat_id, REBEL_IMG, caption=full_msg)
    elif count >= 5:
        # الحظر النهائي
        await event.reply(f"**🚫 تم حظرك لتجاوزك حد التكرار.**")
        await client(functions.contacts.BlockRequest(id=user_id))

# --- [5] التشغيل النهائي ---
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
