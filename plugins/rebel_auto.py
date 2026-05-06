import asyncio, os, pytz, glob, importlib, sys, re, json, threading
from datetime import datetime
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
import config 

# --- [1] إعدادات المملكة (تم تثبيت الآيدي الصحيح للجروب) ---
LOG_GROUP_ID = -1003586994898
DB_FILE = "rebel_security.json"
YEMEN_TZ = pytz.timezone('Asia/Aden')

# --- [2] محرك الويب (لإرضاء ريندر وضمان بقاء السورس أونلاين) ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "🛡️ Rebel Source is Live & Invincible 🦅"
def run_flask():
    try: app.run(host='0.0.0.0', port=10000)
    except: pass
threading.Thread(target=run_flask, daemon=True).start()

# --- [3] تعريف الكلاينت ودوال المساعدة ---
client = TelegramClient(StringSession(config.SESSION), config.API_ID, config.API_HASH)

def z_nums(text):
    n = {'0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'}
    return "".join(n.get(c, c) for c in text)

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: pass
    return {"status": True, "counts": {}, "allowed": []}

def save_data(data):
    with open(DB_FILE, "w") as f: json.dump(data, f)

# --- [4] نظام "الاوامر" الملكي بالأرقام الفخمة ---
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.الاوامر"))
async def help_engine(event):
    all_commands = ["تفعيل_الحماية", "تعطيل_الحماية", "سماح", "رفض", "ايدي", "فحص", "تدمير"]
    files = ["main.py"] + glob.glob("plugins/*.py")
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                found = re.findall(r'pattern=r"\\\.([\w_]+)"', f.read())
                if found: all_commands.extend(found)
        except: continue
    
    unique_cmds = []
    [unique_cmds.append(x) for x in all_commands if x not in unique_cmds]
    
    msg = f"""
**- مـعقل الـمتمرد الـتقني 🛡️🦅**
— — — — — — — — — — —
**معقل المتمرد: #حيث_يلتقي_التشفير_بالذكاء، والتمرد بالواقع. سورس وُجد ليكون الأول، والبقية مجرد محاولات. نحن لا نحمي بياناتك فقط، نحن نمنحك القوة لتكون السيد في عالم لا يعترف إلا بالأقوياء. المتمرد.. أمانٌ لا يُخترق، وهيبةٌ لا تُهزم.**
— — — — — — — — — — —
"""
    for i, cmd in enumerate(unique_cmds, 1):
        msg += f"**{z_nums(str(i))} ⇐** `.{cmd.replace('_', ' ')}`\n"
    
    msg += "— — — — — — — — — — —\n"
    msg += f"**📊 الإجمالي: {z_nums(str(len(unique_cmds)))} حزمة برمجية**"
    await event.edit(msg)

# --- [5] نظام التخزين في الجروب والحماية (1/5) ---
@client.on(events.NewMessage(incoming=True))
async def security_and_logs(event):
    data = load_data()
    if not event.is_private or event.out: return
    
    user = await event.get_sender()
    if not user or user.bot: return
    user_id = str(event.sender_id)

    # إرسال الرسالة والميديا لجروب التخزين بصيغة آمنة
    try:
        u_mention = f"@{user.username}" if user.username else user.first_name
        log_text = f"<b>📥 رسالة جديدة:</b>\n👤: {u_mention}\n🆔: <code>{user_id}</code>\n💬: {event.text or 'وسائط'}"
        await client.send_message(LOG_GROUP_ID, log_text, parse_mode='html')
        if event.media: await client.send_file(LOG_GROUP_ID, event.media)
    except: pass

    # نظام الحماية
    if int(user_id) in data["allowed"] or not data["status"]: return
    counts = data["counts"]
    count = counts.get(user_id, 0) + 1
    counts[user_id] = count
    save_data(data)

    if count == 1:
        photos = await client.get_profile_photos("me", limit=1)
        cap = f"**- أهلاً بك في معقل المتمرد التقني 🛡️**\n— — —\n**⚠️ تحذير (1/5):** يمنع السبام.\n**#حيث_يلتقي_التشفير_بالذكاء..**"
        if photos: await client.send_file(event.chat_id, photos[0], caption=cap)
        else: await event.reply(cap)
    elif count >= 5:
        await event.reply("**❌ تم حظرك تلقائياً لتجاوز حد المراسلة.**")
        await client(functions.contacts.BlockRequest(id=int(user_id)))

# --- [6] محرك التلفيش (التدمير الحقيقي) ---
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.تدمير (\d+) (.*)"))
async def flood_destroy(event):
    count = int(event.pattern_match.group(1))
    text = event.pattern_match.group(2)
    await event.delete()
    for _ in range(count):
        await client.send_message(event.chat_id, text)
        await asyncio.sleep(0.05)

# --- [7] الإقلاع وتحديث الاسم تلقائياً ---
async def start_rebel():
    await client.start()
    print("🦅 [SUCCESS]: معقل المتمرد في الخدمة الآن.")
    
    # تحديث الوقت في الاسم تلقائياً
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
