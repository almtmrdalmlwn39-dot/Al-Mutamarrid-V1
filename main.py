import asyncio, os, pytz, glob, re, json, threading, random, importlib.util
from datetime import datetime
from flask import Flask
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
import config 

# 1. التعريفات أولاً (هذا يحل مشكلة NameError)
CMD_HELP = {}
client = TelegramClient(StringSession(config.SESSION), config.API_ID, config.API_HASH)

# 2. الآن نضع الأوامر (بعد تعريف client)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.الاوامر"))
async def rebel_super_menu(event):
    msg = "ᯓ **𝗭𝗧𝗵𝗼𝗻 𝗨𝘀𝗲𝗿𝗯𝗼𝘁 - قائمــة الاوامــر العامــه** 𓆪\n"
    msg += "⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
    plugins = sorted(CMD_HELP.keys())
    for i, plugin in enumerate(plugins, 1):
        msg += f" **.م{i}** ➪ **اوامــر {plugin}**\n"
    msg += "\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆"
    await event.edit(msg)

# دالة سحب الملفات
async def load_plugins():
    path = "plugins/*.py"
    for name in glob.glob(path):
        module_name = os.path.basename(name).replace(".py", "")
        try:
            spec = importlib.util.spec_from_file_location(module_name, name)
            pkg = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(pkg)
            if hasattr(pkg, 'CMD_HELP'): CMD_HELP.update(pkg.CMD_HELP)
        except Exception as e: print(f"❌ Error in {module_name}: {e}")

async def start_rebel():
    await client.start()
    await load_plugins()
    await client.run_until_disconnected()

if __name__ == '__main__':
    threading.Thread(target=lambda: Flask(__name__).run(host='0.0.0.0', port=10000), daemon=True).start()
    client.loop.run_until_complete(start_rebel())
