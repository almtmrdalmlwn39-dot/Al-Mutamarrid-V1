import asyncio, os, pytz, glob, re, json, threading, random, importlib
from datetime import datetime
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
import config 

# قاموس عالمي لتخزين الأوامر من الملفات
CMD_HELP = {}

client = TelegramClient(StringSession(config.SESSION), config.API_ID, config.API_HASH)

# دالة سحب الملفات من مجلد plugins
async def load_plugins():
    path = "plugins/*.py"
    files = glob.glob(path)
    for name in files:
        module_name = name.replace(".py", "").replace("/", ".").replace("\\", ".")
        try:
            importlib.import_module(module_name)
        except Exception as e:
            print(f"❌ خطأ في ملف {name}: {e}")

# أمر .الاوامر الذي يقرأ من كل الملفات تلقائياً
@client.on(events.NewMessage(outgoing=True, pattern=r"\.الاوامر"))
async def show_all_cmds(event):
    msg = "**🛡️ قائمة أوامر المتمرد الشاملة 🦅**\n— — — — — — — — —\n"
    for plugin, cmds in CMD_HELP.items():
        msg += f"📦 **حزمة: {plugin}**\n"
        for cmd in cmds:
            msg += f" ⇐ `.{cmd}`\n"
        msg += "— — —\n"
    await event.edit(msg + "\n`تم سحب الأوامر من المجلدات بنجاح.`")

# تشغيل السورس
async def start_rebel():
    await client.start()
    await load_plugins() # تفعيل السحب التلقائي
    await client.run_until_disconnected()

if __name__ == '__main__':
    threading.Thread(target=lambda: Flask(__name__).run(host='0.0.0.0', port=10000), daemon=True).start()
    client.loop.run_until_complete(start_rebel())
