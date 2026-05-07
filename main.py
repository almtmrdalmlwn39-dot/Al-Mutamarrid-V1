import asyncio, os, pytz, glob, re, json, threading, random, importlib.util
from datetime import datetime
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
import config 

CMD_HELP = {}

client = TelegramClient(StringSession(config.SESSION), config.API_ID, config.API_HASH)

# دالة سحب الملفات المطورة (تفتيش المجلدات وقراءة القواميس)
async def load_plugins():
    path = "plugins/*.py"
    files = glob.glob(path)
    for name in files:
        # تحويل المسار إلى اسم موديول
        module_name = os.path.basename(name).replace(".py", "")
        try:
            # استيراد الملف كموديول مستقل
            spec = importlib.util.spec_from_file_location(module_name, name)
            pkg = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(pkg)
            
            # فحص إذا كان الملف يحتوي على قاموس CMD_HELP وسحبه
            if hasattr(pkg, 'CMD_HELP'):
                CMD_HELP.update(pkg.CMD_HELP)
                print(f"✅ تم دمج أوامر الملف: {module_name}")
            else:
                print(f"⚠️ الملف {module_name} لا يحتوي على تعريف CMD_HELP")
                
        except Exception as e:
            print(f"❌ خطأ فادح في تحميل {name}: {e}")

# أمر .الاوامر (الذي سيظهر ممتلئاً الآن)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.الاوامر"))
async def show_all_cmds(event):
    if not CMD_HELP:
        return await event.edit("**⚠️ القائمة فارغة.. تأكد من تعريف CMD_HELP داخل ملفات الـ plugins.**")
        
    msg = "**🛡️ قائمة أوامر المتمرد الشاملة 🦅**\n— — — — — — — — —\n"
    for plugin, cmds in CMD_HELP.items():
        msg += f"📦 **حزمة: {plugin}**\n"
        for cmd in cmds:
            msg += f" ⇐ `.{cmd}`\n"
        msg += "— — —\n"
    await event.edit(msg + "\n`تم سحب الأوامر من المجلدات بنجاح.`")

async def start_rebel():
    await client.start()
    await load_plugins()
    print("🛡️ المتمرد جاهز الآن.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # تشغيل سيرفر Flask في خلفية لضمان استقرار ريندر
    threading.Thread(target=lambda: Flask(__name__).run(host='0.0.0.0', port=10000), daemon=True).start()
    client.loop.run_until_complete(start_rebel())
