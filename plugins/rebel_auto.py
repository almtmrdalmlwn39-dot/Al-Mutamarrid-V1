import asyncio, os, pytz, glob, re, json, threading
from datetime import datetime
from flask import Flask
from telethon import TelegramClient, events, functions
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
import config 

# --- [1] إعدادات المعقل ---
LOG_GROUP_ID = -1003586994898 
DB_FILE = "rebel_security.json"
YEMEN_TZ = pytz.timezone('Asia/Aden')
SUDO_USERS = [6467728995] # آيديك الخاص لضمان استثنائك من الحظر

# --- [2] محرك الويب لريندر ---
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

# --- [3] محرك الأوامر (العدد الجديد 56 حزمة) ---
@client.on(events.NewMessage(outgoing=True))
async def rebel_cmds(event):
    text = event.text
    data = load_data()

    # فحص الهوية مع عبارتك الخاصة
    if text.startswith((".ايدي", ".فحص", ".هويتي")):
        msg = f"""
**💳 نتيجة الفحص العميق :**
— — — — — — — — — — —
**- الاسم: فـرانـكـو || 𐇮 ᒪOᖇ𐇮f𝑒 **
**- الآيـدي: `{event.sender_id}`**
**- البايو: نبذة تعريفيه شخص مغرم بنفسه ولايتنازل لـ خلق الله أبداً**
— — — — — — — — — — —
**معقل المتمرد: #حيث_يلتقي_التشفير_بالذكاء، والتمرد بالواقع. سورس وُجد ليكون الأول، والبقية مجرد محاولات. نحن لا نحمي بياناتك فقط، نحن نمنحك القوة لتكون السيد في عالم لا يعترف إلا بالأقوياء. المتمرد.. أمانٌ لا يُخترق، وهيبةٌ لا تُهزم.**
"""
        await event.edit(msg)
        return

    # عرض القائمة كاملة (الـ 45 الأساسية + الـ 11 الجديدة)
    if text == ".الاوامر":
        # أوامر التحكم الـ 11 التي سنضيفها الآن
        new_cmds = [
            "تفعيل_الحماية", "تعطيل_الحماية", "انشاء_تخزين", 
            "تفعيل_القروب", "سماح", "رفض", "حظر", "تدمير", 
            "ايدي", "فحص", "هويتي"
        ]
        
        # جلب الـ 45 أمر الحالية من ملفات الإضافات
        plugin_cmds = []
        files = ["main.py"] + glob.glob("plugins/*.py")
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    found = re.findall(r'pattern=r"\\\.([\w_]+)"', f.read())
                    if found: plugin_cmds.extend(found)
            except: continue
        
        # دمج كل الأوامر وترتيبها
        all_list = sorted(list(set(new_cmds + plugin_cmds)))
        total_count = len(all_list) # هنا سيظهر الرقم 56 تلقائياً
        
        header = f"**🛡️ معقل المتمرد: حيث يلتقي التشفير بالذكاء 🦅**\n"
        header += f"**— — — — — — — — — — —**\n"
        header += f"**نحن لا نحمي بياناتك فقط، نحن نمنحك القوة.**\n"
        header += f"**— — — — — — — — — — —**\n"
        
        body = ""
        for i, cmd in enumerate(all_list, 1):
            body += f"**{z_nums(str(i))} ⇐** `.{cmd.replace('_', ' ')}`\n"
            
        footer = f"**— — — — — — — — — — —**\n"
        footer += f"**👤 المطور الأول ⇐ [تواصل هنا](https://t.me/bedmoddinnow)**\n"
        footer += f"**📊 الإجمالي: {z_nums(str(total_count))} حزمة برمجية شغالة**"
        
        await event.edit(header + body + footer)
        return

    # أوامر التحكم في الحماية والتخزين
    if text in [".تفعيل الحماية", ".تفعيل_الحماية"]:
        data["status"] = True
        save_data(data)
        await event.edit("**🛡️ تم تفعيل نظام حماية المتمرد بنجاح.**")
    elif text in [".انشاء تخزين", ".انشاء_تخزين"]:
        data["storage"] = True
        save_data(data)
        await event.edit(f"**✅ تم تفعيل التخزين في القروب: `{LOG_GROUP_ID}`**")

# --- [4] نظام الحماية والتخزين (تحذير 1/5) ---
@client.on(events.NewMessage(incoming=True))
async def security_and_storage(event):
    data = load_data()
    if event.chat_id == LOG_GROUP_ID or not event.is_private: return
    user_id = event.sender_id
    if user_id in SUDO_USERS or user_id in data.get("allowed", []): return

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
        await event.reply("**⚠️ تحذير (1/5): يمنع السبام في معقل المتمرد.**")
    elif count >= 5:
        await client(functions.contacts.BlockRequest(id=user_id))

# --- [5] الإقلاع ---
async def start_rebel():
    await client.start()
    async def time_updater():
        while True:
            try:
                tm = z_nums(datetime.now(YEMEN_TZ).strftime("%I:%M"))
                me = await client.get_me()
                clean_name = me.first_name.split(" | ")[0]
                await client(UpdateProfileRequest(first_name=f"{clean_name} | {tm}"))
            except: pass
            await asyncio.sleep(300)
    asyncio.create_task(time_updater())
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(start_rebel())
