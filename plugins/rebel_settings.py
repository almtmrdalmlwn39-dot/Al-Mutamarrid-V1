import asyncio, os, platform, psutil
from telethon import events, functions, types
from main import client, CMD_HELP

# --- [ AL-MUTAMARRID SETTINGS BRAND ] ---
WAR_IDENTITY = "**𓄂 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗦𝗢𝗨𝗥𝗖𝗘 🛡️**"
SET_BRAND = "**⚙️ 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗖𝗢𝗡𝗧𝗥𝗢𝗟**"

# قائمة تخزين المعرفات للمطورين المرفوعين (للسورس العام)
SUDO_USERS = [] 

# تسجيل الأوامر المدمجة في قائمة المساعدة
CMD_HELP.update({
    "الإعدادات والتحكم": [
        "حالة_السورس", "بايو", "عن_المتمرد", "رفع_مطور", "تنزيل_مطور", "اوامر_الاعدادات"
    ]
})

# 1. نظام إدارة المطورين (للمستخدمين الآخرين)
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.رفع_مطور$"))
async def promote_dev(event):
    if not event.is_reply:
        return await event.edit("**⚠️ رد على الشخص لرفعه مطوراً في السورس.**")
    reply_msg = await event.get_reply_message()
    user_id = reply_msg.sender_id
    if user_id not in SUDO_USERS:
        SUDO_USERS.append(user_id)
        await event.edit(f"**👑 تم منح صلاحيات المطور لـ `{user_id}` بنجاح!**")
    else:
        await event.edit("**⚠️ هذا المستخدم مطور بالفعل.**")

@client.on(events.NewMessage(outgoing=True, pattern=r"^\.تنزيل_مطور$"))
async def demote_dev(event):
    if not event.is_reply:
        return await event.edit("**⚠️ رد على الشخص لتنزيله.**")
    reply_msg = await event.get_reply_message()
    user_id = reply_msg.sender_id
    if user_id in SUDO_USERS:
        SUDO_USERS.remove(user_id)
        await event.edit(f"**✅ تم سحب صلاحيات المطور من `{user_id}`.**")
    else:
        await event.edit("**⚠️ المستخدم ليس مطوراً.**")

# 2. أمر فحص حالة السيرفر (Render Status)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.حالة_السورس"))
async def server_status(event):
    await event.edit("**🔄 جـاري فـحص مـوارد الـسيرفر...**")
    ram = f"{psutil.virtual_memory().percent}%"
    cpu = f"{psutil.cpu_percent()}%"
    status_msg = (
        f"**📊 تـقـريـر أداء الـمـنـظـومـة :**\n"
        f"**— — — — — — — — — — —**\n"
        f"**🛡️ الـحـالـة:** نـشـط ✅\n"
        f"**📉 اسـتهلاك الـرام:** `{ram}`\n"
        f"**🧠 مـعـالـج الـنـظام:** `{cpu}`\n"
        f"**💻 بـيـئة الـعـمـل:** `{platform.system()}`\n"
        f"**— — — — — — — — — — —**\n"
        f"{WAR_IDENTITY}"
    )
    await event.edit(status_msg)

# 3. أمر تغيير البايو (النبذة) فوراً
@client.on(events.NewMessage(outgoing=True, pattern=r"\.بايو (.*)"))
async def change_bio(event):
    new_bio = event.pattern_match.group(1)
    try:
        await client(functions.account.UpdateProfileRequest(about=new_bio))
        await event.edit(f"**✅ تـم تـحـديث الـبـايـو :**\n`{new_bio}`")
    except Exception as e:
        await event.edit(f"**⚠️ فـشل الـتحديث:** `{e}`")

# 4. قائمة أوامر الإعدادات الشاملة
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اوامر_الاعدادات"))
async def settings_help(event):
    help_text = (
        f"**{SET_BRAND}**\n"
        "**— — — — — — — — — — —**\n"
        "**📊 | `.حالة_السورس` :** مراقبة أداء السيرفر.\n"
        "**👑 | `.رفع_مطور` :** منح صلاحيات التحكم (بالرد).\n"
        "**👤 | `.تنزيل_مطور` :** سحب صلاحيات المطور (بالرد).\n"
        "**📝 | `.بايو [النص]` :** تغيير نبذة حسابك.\n"
        "**— — — — — — — — — — —**\n"
        f"{WAR_IDENTITY}"
    )
    await event.edit(help_text)
