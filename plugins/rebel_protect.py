import asyncio, re, os, json
from telethon import events, functions, types
from main import client, CMD_HELP, WAR_IDENTITY

# --- [ نظام السيطرة والدرع التقني ] ---
CONFIG_FILE = "rebel_config.json"
def save_cfg(d): json.dump(d, open(CONFIG_FILE, "w"))
def load_cfg(): return json.load(open(CONFIG_FILE, "r")) if os.path.exists(CONFIG_FILE) else {"protect": False, "replies": False, "anti_hack": False}
REBEL_SETTINGS = load_cfg()

# 1. أوامر التحكم (تشغيل/إيقاف الدرع)
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.(تفعيل|تعطيل) (الحماية|الردود|الدرع)$"))
async def toggle_rebel(event):
    action = event.pattern_match.group(1)
    target = event.pattern_match.group(2)
    state = True if action == "تفعيل" else False
    
    if target == "الحماية": REBEL_SETTINGS["protect"] = state
    elif target == "الدرع": REBEL_SETTINGS["anti_hack"] = state
    else: REBEL_SETTINGS["replies"] = state
    
    save_cfg(REBEL_SETTINGS)
    await event.edit(f"**🛡️ تم {action} {target} بنجاح!**")

# 2. درع الحماية من الهكر والبوتات (Anti-Hack)
@client.on(events.ChatAction)
async def anti_hack(event):
    if not REBEL_SETTINGS["anti_hack"]: return
    
    # منـع إضـافة البوتات (طرد أي بوت يضيفه شخص غير الأدمن)
    if event.user_added:
        added_users = await event.get_users()
        for user in added_users:
            if user.bot:
                try:
                    # طرد البوت المضاف وطرد الشخص الذي أضافه (اختياري)
                    await client.kick_participant(event.chat_id, user.id)
                    await event.respond(f"**🛡️ درع المتمرد: تم طرد البوت المخرب [ {user.first_name} ]**")
                except: pass

# 3. حماية الروابط ومنع التفليش (Flood)
@client.on(events.NewMessage(incoming=True))
async def security_check(event):
    if not REBEL_SETTINGS["protect"] or event.is_private: return
    
    # حذف الروابط والمعرفات فوراً
    if re.search(r"(http|https|t\.me|@)", event.raw_text):
        try:
            perms = await client.get_permissions(event.chat_id, event.sender_id)
            if not perms.is_admin:
                await event.delete()
        except: pass

# 4. أوامر السيطرة (طرد، حظر، كتم)
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.(طرد|حظر|كتم)$"))
async def admin_tools(event):
    if not event.is_reply: return await event.edit("**⚠️ رد على الشخص!**")
    cmd = event.pattern_match.group(1)
    rep = await event.get_reply_message()
    try:
        if cmd == "طرد": await client.kick_participant(event.chat_id, rep.sender_id)
        elif cmd == "حظر": await client(functions.channels.EditBannedRequest(event.chat_id, rep.sender_id, types.ChatBannedRights(until_date=None, view_messages=True)))
        elif cmd == "كتم": await client(functions.channels.EditBannedRequest(event.chat_id, rep.sender_id, types.ChatBannedRights(until_date=None, send_messages=True)))
        await event.edit(f"**🛡️ تم تنفيذ {cmd} الشخص بنجاح.**")
    except: await event.edit("**⚠️ ارفعني أدمن أولاً.**")

# --- [ تحديث القائمة رقم 1 ] ---
CMD_HELP["درع الحماية والسيطرة"] = [
    "**• أوامر الـتـفـعـيـل:**",
    "**-** `.تفعيل الدرع` ⇐ لمنع دخول البوتات المخربة.",
    "**-** `.تفعيل الحماية` ⇐ لمنع الروابط والمعرفات.",
    "**--------------------------**",
    "**• أوامر السيطرة:**",
    "**-** `.طرد` | `.حظر` | `.كتم` (بالرد).",
    "**-** سورس المتمرد يحميك من أي محاولة اختراق للقروب."
]

