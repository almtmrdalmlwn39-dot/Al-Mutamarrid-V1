from telethon import events, functions, types
import json, os, re

# إعدادات المتمرد الأساسية
DB_FILE = "rebel_security.json"
SUDO_USERS = [6467728995] 

# قائمة الكلمات والروابط المشبوهة (يمكنك زيادتها)
SPAM_PATTERNS = [
    r"(تليجرام|بوت|اختراق|هكر|فلوس|مجانا|ثغرة)", 
    r"(t\.me/|http|https|www\.)", # منع الروابط نهائياً
    r"(\.apk|\.exe|\.zip|\.py)" # منع الملفات الملغمة
]

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: pass
    return {"allowed": []}

# --- [محرك الحماية العظمى للمتمرد] ---
@events.register(events.NewMessage(incoming=True))
async def global_security_guard(event):
    if not event.is_group: return
    data = load_data()
    
    # استثناء المالك والمطورين من الفلترة
    if event.sender_id in SUDO_USERS or event.sender_id in data.get("allowed", []):
        return

    # 1. فلترة الرسائل والروابط المشبوهة
    for pattern in SPAM_PATTERNS:
        if re.search(pattern, event.text, re.IGNORECASE):
            try:
                await event.delete()
                await event.reply(f"**🛡️ نظام المتمرد كشف رسالة مشبوهة وتم حذفها.**")
                return # توقف هنا بعد الحذف
            except: pass

    # 2. منع المقاطع والملفات (لغير الموثوقين)
    if event.media:
        if isinstance(event.media, (types.MessageMediaDocument, types.MessageMediaWebPage)):
             try:
                await event.delete()
                await event.reply("**🛡️ يمنع إرسال الملفات والروابط في معقل المتمرد.**")
             except: pass

# --- [حماية القروب من التفليش والتغيير] ---
@events.register(events.ChatAction)
async def anti_destruction(event):
    data = load_data()
    if event.user_id in SUDO_USERS or event.user_id in data.get("allowed", []):
        return

    # حظر أي شخص يحاول طرد الأعضاء أو تغيير الإعدادات
    if event.user_kicked or event.new_title or event.new_photo or event.new_pin:
        try:
            await event.client(functions.channels.EditBannedRequest(
                event.chat_id, event.user_id, 
                types.ChatBannedRights(until_date=None, view_messages=True)
            ))
            await event.reply(f"**⚠️ تم رصد محاولة تخريب من `{event.user_id}` وتم حظره نهائياً.**")
        except: pass
