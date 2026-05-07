from main import client, CMD_HELP, SUDO_USERS, DB_FILE # استيراد الإعدادات من الملف الرئيسي
from telethon import events, functions, types
import json, os, re

# تسجيل الحماية في القائمة الشاملة
CMD_HELP["الحماية القصوى"] = ["تفعيل_الحماية", "منع_الروابط", "حماية_التفليش"]

# قائمة الأنماط المشبوهة
SPAM_PATTERNS = [
    r"(تليجرام|بوت|اختراق|هكر|فلوس|مجانا|ثغرة)", 
    r"(t\.me/|http|https|www\.)", 
    r"(\.apk|\.exe|\.zip|\.py)" 
]

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: pass
    return {"allowed": []}

# --- [محرك الحماية العظمى] ---
@client.on(events.NewMessage(incoming=True))
async def global_security_guard(event):
    if not event.is_group: return
    data = load_data()
    
    if event.sender_id in SUDO_USERS or event.sender_id in data.get("allowed", []):
        return

    # فلترة النصوص والروابط
    for pattern in SPAM_PATTERNS:
        if re.search(pattern, event.text, re.IGNORECASE):
            try:
                await event.delete()
                return 
            except: pass

    # منع الوسائط المشبوهة
    if event.media:
        if isinstance(event.media, (types.MessageMediaDocument, types.MessageMediaWebPage)):
             try:
                await event.delete()
             except: pass

# --- [حماية القروب من التفليش] ---
@client.on(events.ChatAction)
async def anti_destruction(event):
    data = load_data()
    if event.user_id in SUDO_USERS or event.user_id in data.get("allowed", []):
        return

    # حظر المخربين فوراً عند محاولة التغيير
    if event.user_kicked or event.new_title or event.new_photo or event.new_pin:
        try:
            await client(functions.channels.EditBannedRequest(
                event.chat_id, event.user_id, 
                types.ChatBannedRights(until_date=None, view_messages=True)
            ))
            await event.reply(f"**🛡️ المتمرد بالمرصاد.. تم حظر المخرب `{event.user_id}` فوراً.**")
        except: pass
