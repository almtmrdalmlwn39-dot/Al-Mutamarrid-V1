import os

# --- [ إعدادات سورس 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗧𝗘𝗖𝗛 ] ---

# سحب البيانات إجبارياً من منصة الاستضافة (Render/Heroku)
# الآن لا توجد أي أرقام أو بيانات حقيقية هنا، الخصوصية 100%
API_ID = int(os.environ.get("API_ID", 0)) 
API_HASH = os.environ.get("API_HASH", None)
SESSION = os.environ.get("SESSION", None)

# سحب ايديك وايدي المطورين من المنصة فقط
SUDO_STR = os.environ.get("SUDO_USERS", "")
SUDO_USERS = list(map(int, SUDO_STR.split())) if SUDO_STR else []

# إعدادات الوقت
YEMEN_TZ = "Asia/Aden"

# اسم السورس الرسمي
BOT_NAME = "𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗧𝗘𝗖𝗛"
