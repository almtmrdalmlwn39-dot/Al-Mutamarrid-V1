import asyncio, os, pytz, glob, importlib, sys, re, json, threading
from datetime import datetime
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
import google.generativeai as genai
import config 

# --- [1] الهوية والروابط ---
REBEL_SIG_TEXT = "**نحن لا نحمي بياناتك فقط، نحن نمنحك القوة لتكون السيد في عالم لا يعترف إلا بالأقوياء. المتمرد.. أمانٌ لا يُخترق، وهيبةٌ لا تُهزم.**"
REBEL_DEV_LINKS = (
    "\n— — — — — — — — — — — —\n"
    "👤 المطور الأول ⇐ **[تواصل هنا](https://t.me/Vi_ti0)**\n"
    "👤 المطور الثاني ⇐ **[تواصل هنا](https://t.me/A0_O7)**\n"
    "— — — — — — — — — — — —"
)
REBEL_IMG = "https://telegra.ph/file/058204663f73359d997f0.jpg"

# --- [2] الإعدادات ---
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
    return {"status": False, "counts": {}, "allowed": []}

def save_data(data):
    with open(DB_FILE, "w") as f: json.dump(data, f)

# --- [3] محرك الأوامر ---
@client.on(events.NewMessage(outgoing=True))
async def rebel_main_engine(event):
    text = event.text
    data = load_data()
    
    # أمر تفعيل الحماية (للتأكد أن النظام اشتغل)
    if text == ".تفعيل الحماية":
        data["status"] = True
        save_data(data)
        await event.edit("**✅ تم تفعيل نظام حماية معقل المتمرد بنجاح.. القلعة الآن مؤمنة.**")

    elif text == ".تعطيل الحماية":
        data["status"] = False
        save_data(data)
        await event.edit("**⚠️ تم تعطيل نظام الحماية.. القلعة الآن مفتوحة.**")

    # أمر الايدي
    elif text.startswith(".ايدي"):
        reply = await event.get_reply_message()
        target = reply.sender if reply else await event.get_sender()
        rank = "المالك" if target.id in SUDO_USERS else "عضو"
        info = f"**👤 الاسم:** {target.first_name}\n**🆔 الايدي:** `{target.id}`\n**🎖️ الرتبة:** {rank}\n**🦅 السورس:** المتمرد التقني\n{REBEL_DEV_LINKS}"
        try:
            photo = await client.download_profile_photo(target.id)
            await client.send_file(event.chat_id, photo or REBEL_IMG, caption=info, reply_to=reply.id if reply else event.id)
            if photo: os.remove(photo)
            await event.delete()
        except: await event.edit(info)

    # قائمة الأوامر
    elif text == ".الاوامر":
        all_cmds = ["تفعيل الحماية", "تعطيل الحماية", "ايدي", "مطور", "فحص", "تلفيش"]
        msg = f"**🛡️ معقل المتمرد: حيث يلتقي التشفير بالذكاء 🦅**\n— — —\n{REBEL_SIG_TEXT}\n— — —\n"
        for i, cmd in enumerate(all_cmds, 1):
            msg += f"**{z_nums(str(i))} ⇐** `.{cmd}`\n"
        msg += f"— — —\n{REBEL_DEV_LINKS}"
        await client.send_file(event.chat_id, REBEL_IMG, caption=msg)
        await event.delete()

# --- [4] نظام الحماية والترحيب (الإصلاح النهائي) ---
@client.on(events.NewMessage(incoming=True))
async def security_logic(event):
    if not event.is_private: return
    data = load_data()
    if not data.get("status"): return # التأكد أن الحماية مفعلة
    
    user_id = event.sender_id
    if user_id in SUDO_USERS or user_id == (await client.get_me()).id: return

    u_str = str(user_id)
    counts = data.get("counts", {})
    count = counts.get(u_str, 0) + 1
    counts[u_str] = count
    data["counts"] = counts
    save_data(data)

    sender = await event.get_sender()
    f_name = sender.first_name if sender.first_name else "المستخدم"

    if count == 1:
        # الترحيب الأول مع الحسابات
        msg = f"**يا {f_name}، مرحباً بك في معقل المتمرد 🛡️**\n**⚠️ تنبيه ({z_nums(str(count))}/٥): يمنع التكرار.**\n\n{REBEL_SIG_TEXT}\n{REBEL_DEV_LINKS}"
        await client.send_file(event.chat_id, REBEL_IMG, caption=msg)
    elif count < 5:
        # تنبيه تكرار
        await client.send_file(event.chat_id, REBEL_IMG, caption=f"**يا {f_name}.. لا تزيد بالهرج فوق راسي.**\n**⚠️ تنبيه ({z_nums(str(count))}/٥)**")
    elif count >= 5:
        # حظر نهائي
        await event.reply(f"**🚫 تم حظرك لتجاوزك حد التكرار.**\n{REBEL_DEV_LINKS}")
        await client(functions.contacts.BlockRequest(id=user_id))

# --- [5] التشغيل ---
async def start_rebel():
    await client.start()
    print("🛡️ Rebel Source is Online")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(start_rebel())
