import asyncio, os, pytz, glob, re, json, threading, random
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

# العبارة الموحدة (التوقيع الفخم)
REBEL_SIG = "معقل المتمرد: #حيث_يلتقي_التشفير_بالذكاء، والتمرد بالواقع. سورس وُجد ليكون الأول، والبقية مجرد محاولات. نحن لا نحمي بياناتك فقط، نحن نمنحك القوة لتكون السيد في عالم لا يعترف إلا بالأقوياء. المتمرد.. أمانٌ لا يُخترق، وهيبةٌ لا تُهزم."

# --- [ إعداد الذكاء الاصطناعي ] ---
genai.configure(api_key="AIzaSyDwzx1U-IGgw-Kybz2RVt2N-xtkWrIt7aU")
model = genai.GenerativeModel('gemini-pro')

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

async def get_franco_reply(user_msg):
    prompt = f"أنت مطور يمني متمرد. رد بلهجة يمنية قوية. لا تذكر أنك بوت. الرسالة: {user_msg}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except: return "لا تزيد بالهرج فوق راسي."

# --- [3] محرك الأوامر (56 حزمة) ---
@client.on(events.NewMessage(outgoing=True))
async def rebel_cmds(event):
    text = event.text
    reply = await event.get_reply_message()

    if text.startswith((".ايدي", ".فحص", ".هويتي")):
        target_id, target_name = event.sender_id, (await client.get_me()).first_name
        if reply:
            target_id = reply.sender_id
            target_name = (await client.get_entity(target_id)).first_name
        msg = f"**💳 نتيجة الفحص العميق :**\n— — — — — — — — — — —\n**- الاسم: {target_name}**\n**- الآيـدي: `{target_id}`**\n— — — — — — — — — — —\n**{REBEL_SIG}**"
        await event.edit(msg)
        return

    if text == ".طرد":
        if event.is_private:
            user = await event.get_chat()
            await event.edit("**🛡️ جاري التنظيف.. وداعاً.**")
            try:
                await client(functions.contacts.BlockRequest(id=user.id))
                await client(functions.messages.DeleteHistoryRequest(peer=user.id, max_id=0, forget=True, revoke=True))
            except: pass
        elif reply:
            try: await client.kick_participant(event.chat_id, reply.sender_id); await event.edit("**تم طرده.**")
            except: await event.edit("**تأكد من الصلاحيات.**")
        return

    if text == ".الاوامر":
        new_cmds = ["تفعيل_الحماية", "تعطيل_الحماية", "انشاء_تخزين", "طرد", "قصف", "حظر", "تدمير", "ايدي", "فحص", "هويتي", "حالة_السورس", "تنظيف", "سرعة", "تحديث"]
        all_list = sorted(list(set(new_cmds)))
        header = f"**🛡️ معقل المتمرد: حيث يلتقي التشفير بالذكاء 🦅**\n— — — — — — — — — — —\n"
        body = "".join([f"**{z_nums(str(i))} ⇐** `.{cmd}`\n" for i, cmd in enumerate(all_list[:56], 1)])
        footer = f"— — — — — — — — — — —\n**👤 المطور الأول ⇐ [تواصل](https://t.me/Vi_ti0)**\n**👤 المطور الثاني ⇐ [تواصل](https://t.me/A0_O7)**\n**📊 الإجمالي: {z_nums(str(56))} حزمة**"
        await event.edit(header + body + footer)
        return

# --- [4] نظام الرد الذكي والتحذير بالخاص (مع العبارة) ---
@client.on(events.NewMessage(incoming=True))
async def security_and_reply(event):
    data = load_data()
    if event.chat_id == LOG_GROUP_ID or event.sender_id in SUDO_USERS: return

    if data.get("storage") and event.is_private:
        try: await client.send_message(LOG_GROUP_ID, f"**📥 من:** `{event.sender_id}`\n**💬 النص:** {event.text}")
        except: pass

    should_reply = event.is_private or event.mentioned or (event.is_reply and (await event.get_reply_message()).sender_id in SUDO_USERS)
    if should_reply and data.get("status"):
        u_str = str(event.sender_id)
        count = data["counts"].get(u_str, 0) + 1
        data["counts"][u_str] = count
        save_data(data)

        if count < 5:
            franco_response = await get_franco_reply(event.text)
            # الرد بالخاص مع العبارة والصورة
            if event.is_private:
                final_msg = f"**{franco_response}**\n\n— — — — — — — — — — —\n`{REBEL_SIG}`"
                try: await event.reply(final_msg, file=REBEL_IMG)
                except: await event.reply(final_msg)
            else: # الرد في القروب (نص فقط)
                await event.reply(f"**{franco_response}**")
        elif count >= 5:
            if event.is_private:
                # رسالة الحظر مع العبارة
                ban_msg = f"**خلاص قد زدت بالحكي.. حظر يفكك من شرك 🚫**\n\n— — — — — — — — — — —\n`{REBEL_SIG}`"
                await event.reply(ban_msg)
            await client(functions.contacts.BlockRequest(id=event.sender_id))

# --- [5] الإقلاع وتحديث الوقت ---
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
