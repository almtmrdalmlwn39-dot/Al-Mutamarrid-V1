import json
import os
import asyncio
from telethon import events, functions, types
from __main__ import client

# --- إعدادات المملكة وتخزين البيانات ---
DB_FILE = "rebel_security.json"
LOG_GROUP_ID = -1002446700860

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: pass
    return {"status": True, "counts": {}, "allowed": []}

def save_data(data):
    with open(DB_FILE, "w") as f: json.dump(data, f)

@client.on(events.NewMessage(incoming=True))
async def almtmrd_guard(event):
    data = load_data()
    if not event.is_private or event.out: return
    
    user_id = str(event.sender_id)
    if int(user_id) in data["allowed"] or not data["status"]: return
    
    user = await event.get_sender()
    if user and user.bot: return

    # [1] تحديث العداد
    counts = data["counts"]
    count = counts.get(user_id, 0) + 1
    counts[user_id] = count
    save_data(data)

    # [2] صيد الميديا المخفية
    if event.media and hasattr(event.media, 'ttl_seconds') and event.media.ttl_seconds:
        try:
            file = await event.download_media()
            cap = f"**⚠️ تم صيد ميديا مخفية!**\n**👤 من:** {user.first_name}\n**🆔 الآيدي:** `{user_id}`"
            await client.send_file(LOG_GROUP_ID, file, caption=cap)
            if os.path.exists(file): os.remove(file)
        except: pass

    # [3] الرد التلقائي والتحذير بالعبارة الجديدة
    if count == 1:
        photos = await client.get_profile_photos("me", limit=1)
        msg = f"""
**- أهـلاً بـك فـي مـعقل الـمتمرد الـتقني 🛡️🦅**
— — — — — — — — — — —
◈ الـاسم ⇐ {user.first_name}
◈ الآيـدي ⇐ `{user_id}`
— — — — — — — — — — —
**⚠️ تـحذير أمـني فـوري (1/5) :**
**- جـاري فـحص بـياناتك والـتأكد مـن هـويتك الآن..**
**- يـمنع إرسـال أكـثر مـن 5 رسـائل لـتجنب الـحظر الـتلقائي.**
— — — — — — — — — — —
**معقل المتمرد: #حيث_يلتقي_التشفير_بالذكاء، والتمرد بالواقع. سورس وُجد ليكون الأول، والبقية مجرد محاولات. نحن لا نحمي بياناتك فقط، نحن نمنحك القوة لتكون السيد في عالم لا يعترف إلا بالأقوياء. المتمرد.. أمانٌ لا يُخترق، وهيبةٌ لا تُهزم.**
"""
        try:
            if photos:
                await client.send_file(event.chat_id, photos[0], caption=msg, reply_to=event.id)
            else:
                await event.reply(msg)
        except: pass

    elif count == 3:
        await event.reply(f"**🚫 تـحذير (3/5):** بدأت تـتجاوز الـحد، تـبقت لـك فرصتان!")

    elif count == 4:
        await event.reply(f"**🚨 الـفرصة الأخـيرة (4/5):** الـرسالة الـقادمة هـي الـحظر!")

    elif count >= 5:
        await event.reply("**❌ تـم حـظرك نـهائياً لـتجاهلك الـتحذيرات.**")
        await client(functions.contacts.BlockRequest(id=int(user_id)))
        counts.pop(user_id)
        save_data(data)
        return

    # [4] تسجيل الرسالة في مجموعة اللوج
    try:
        log_text = f"**📥 رسـالة مـن:** [{user.first_name}](tg://user?id={user_id})\n**🆔 الآيـدي:** `{user_id}`\n**💬 الـنص:** {event.text or 'وسائط'}"
        await client.send_message(LOG_GROUP_ID, log_text)
    except: pass

# [5] أوامر التحكم
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.(تفعيل|تعطيل) الحماية|^\.(سماح|رفض|فحص)"))
async def admin_control(event):
    data = load_data()
    cmd = event.text
    
    if ".تفعيل الحماية" in cmd:
        data["status"] = True
        await event.edit("**✅ تـم تـفعيل نـظام الـحماية والـرد الـتلقائي.**")
    elif ".تعطيل الحماية" in cmd:
        data["status"] = False
        await event.edit("**⚠️ تـم تـعطيل نـظام الـحماية.**")
    elif ".سماح" in cmd:
        target = event.chat_id
        if target not in data["allowed"]: data["allowed"].append(target)
        await event.edit("**✅ تـم الـسماح لـهذا الـمستخدم.**")
    elif ".رفض" in cmd:
        target = event.chat_id
        if target in data["allowed"]: data["allowed"].remove(target)
        await event.edit("**❌ تـم إلـغاء الـسماح.**")
    elif ".فحص" in cmd:
        status = "شـغال ✅" if data["status"] else "مـعطل ⚠️"
        await event.edit(f"**🚀 نـظام الـمتمرد: {status}**")
    
    save_data(data)
