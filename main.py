import os
import glob
import importlib
import asyncio
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from flask import Flask
from threading import Thread

# --- إعدادات السيرفر لإبقاء البوت حياً على Render ---
app = Flask('')
@app.route('/')
def home(): return "I am alive"

def run(): 
    # Render يطلب بورت 10000 عادةً
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات الحساب والبوت من ملف config ---
from config import API_ID, API_HASH, SESSION

# التوكن الخاص ببوتك المساعد (الذي أرسلته لي سابقاً)
BOT_TOKEN = "8662258332:AAF_B4f_UvP_ZpGD8Bzbu-hu3qpb2COzx3s"

# 1. تشغيل الحساب الشخصي
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# 2. تشغيل البوت المساعد (للأزرار والحماية)
tgbot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# --- دالة تحميل الملحقات (Plugins) ---
def load_plugins():
    path = "plugins/*.py"
    files = glob.glob(path)
    for name in files:
        # إصلاح المسارات لتعمل على ويندوز ولينكس (Render)
        module_name = name.replace(".py", "").replace("/", ".").replace("\\", ".")
        try:
            importlib.import_module(module_name)
            print(f"✅ تم تحميل الموديول: {module_name}")
        except Exception as e:
            print(f"❌ فشل تحميل {module_name}: {e}")

# --- نظام حماية الخاص بالأزرار (البوت المساعد) ---
@tgbot.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    if event.is_private:
        me = await client.get_me()
        text = f"🛡️ **أهلاً بك في نظام حماية المتمرد التقني.**\n\nأنا البوت المساعد للمطور [{me.first_name}](tg://user?id={me.id}).\n\nيرجى اختيار سبب التواصل لكي يتم السماح لك بالدخول:"
        
        buttons = [
            [Button.inline("طلب سورس أو برمجة ⚙️", data="dev")],
            [Button.inline("تواصل شخصي 👤", data="personal")],
            [Button.inline("تبادل أو إعلان 🤝", data="trade")]
        ]
        await event.respond(text, buttons=buttons)

@tgbot.on(events.CallbackQuery)
async def callback(event):
    if event.data == b"dev":
        await event.edit("⚙️ **تم إرسال طلبك للمتمرد.. سيتم الرد عليك فور التفرغ.**")
    elif event.data == b"personal":
        await event.edit("👤 **تم إخطار المتمرد برغبتك في التواصل الشخصي.**")
    elif event.data == b"trade":
        await event.edit("🤝 **أرسل تفاصيل التبادل الآن وسينظر فيها المتمرد.**")

# --- دالة التشغيل الكبرى ---
async def start_bot():
    keep_alive() # تشغيل سيرفر الإبقاء متصلاً
    print("⏳ جاري تشغيل سورس المتمرد والبوت المساعد...")
    
    await client.start()
    await tgbot.start()
    
    load_plugins() # تحميل الأوامر
    
    print("🛡️ النظام المزدوج شغال الآن بنجاح على Render!")
    
    # تشغيل الاثنين معاً وعدم التوقف
    await asyncio.gather(
        client.run_until_disconnected(),
        tgbot.run_until_disconnected()
    )

if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        pass
