import os

# --- [ إعدادات سورس 𝗔𝗟-𝗠𝗨𝗧𝗔ﻣ𝗔𝗥𝗥𝗜𝗗 𝗧𝗘𝗖𝗛 ] ---

# جلب البيانات من منصة Render (التي وضعتها أنت في الإعدادات)
API_ID = int(os.environ.get("API_ID", 20585941)) 
API_HASH = os.environ.get("API_HASH", "4c8b6debbee47ab644c82305487f34b2")
SESSION = os.environ.get("SESSION", None)

# تعريف المطور الأساسي (أيدي حسابك)
SUDO_STR = os.environ.get("SUDO_USERS", "6467728995")
SUDO_USERS = list(map(int, SUDO_STR.split())) if SUDO_STR else [6467728995]

# إعدادات الوقت والمنطقة
YEMEN_TZ = "Asia/Aden"
BOT_NAME = "𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 𝗧𝗘𝗖𝗛"

# العبارة التي طلبتها للترحيب أو الأوامر
SOURCE_TEXT = "نحن لا نحمي بياناتك فقط، نحن نمنحك القوة لتكون السيد في عالم لا يعترف إلا بالأقوياء. المتمرد.. أمان لا يُخترق، وهيبة لا تُهزم."
