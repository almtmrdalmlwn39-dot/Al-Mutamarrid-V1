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
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات الحساب والبوت من ملف config ---
from config import API_ID, API_HASH, SESSION
BOT_TOKEN = "8662258332:AAF_B4f_UvP_ZpGD8Bzbu-hu3qpb2COzx3s"

# تعريف الكلاينت والبوت بدون تشغيل فوري لتجنب خطأ asyncio
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
tgbot = TelegramClient("bot_assistant", API_ID, API_HASH)

# --- دالة تحميل الملحقات (Plugins) ---
def load_plugins():
    path = "plugins/*.py"
    for name in glob.glob(path):
        module_name = name.replace(".py", "").replace("/", ".").replace("\\", ".")
        try:
            importlib.import_module(module_name)
            print(f"✅ تم تحميل: {module_name}")
        except: pass

# --- نظام حماية الخاص (الأزرار) ---
@tgbot.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    if event.is_private:
        me = await client.get_me()
        text = f"🛡️ **أهلاً بك في نظام حماية المتمرد التقني.**\n\nأنا البوت المساعد للمطور [{me.first_name}](tg://user?id={me.id}).\n\nيرجى اختيار سبب التواصل لكي يتم السماح لك بالدخول:"
        buttons = [[Button.inline("طلب سورس أو برمجة ⚙️", data="dev")],
                   [Button.inline("تواصل شخصي 👤", data="personal")],
                   [Button.inline("تبادل أو إعلان 🤝", data="trade")]]
        await event.respond(text, buttons=buttons)

@tgbot.on(events.CallbackQuery)
async def callback(event):
    if event.data == b"dev": await event.edit("⚙️ **تم إخطار المتمرد.. انتظر رده.**")
    elif event.data == b"personal": await event.edit("👤 **تم إرسال تنبيه للمتمرد برغبتك في التواصل.**")
    elif event.data == b"trade": await event.edit("🤝 **أرسل تفاصيل التبادل الآن.**")

# --- دالة التشغيل الصحيحة ---
async def main():
    keep_alive()
    print("⏳ جاري بدء التشغيل الموحد...")
    
    # تشغيل الحساب والبوت باستخدام نفس الدورة البرمجية
    await client.start()
    await tgbot.start(bot_token=BOT_TOKEN)
    
    load_plugins()
    print("🛡️ السورس والبوت الآن Live وبدون أخطاء!")
    
    # الانتظار حتى يتم إيقاف السورس
    await asyncio.wait([client.run_until_disconnected(), tgbot.run_until_disconnected()])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
