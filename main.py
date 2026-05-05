import asyncio, os, pytz, re, random, time
from datetime import datetime
from telethon import TelegramClient, events, functions
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest

# --- [ إعدادات الربط ] ---
API_ID = 20585941
API_HASH = "4c8b6debbee47ab644c82305487f34b2"
SESSION = os.environ.get("TERMUX_SESSION") or ""

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# --- [ الهوية الشخصية ] ---
YEMEN_TZ = pytz.timezone('Asia/Aden')
FIXED_NAME = "فــرانــكَـَۄ|| 𝗟َِ𝗢َِ𝗿َِ𝗶َِ𝗙َِ𝒆َِل↜͟͞💸⁩"
MY_BIO = "نبذة تعريفية: شخص مغرم بنفسه ولايتنازل لـ خلق الله ابدا"

def custom_nums(text):
    nums = {'0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵'}
    return "".join(nums.get(c, c) for c in text)

async def update_profile_loop():
    while True:
        try:
            z_time = custom_nums(datetime.now(YEMEN_TZ).strftime("%I:%M"))
            await client(UpdateProfileRequest(first_name=f"{FIXED_NAME} | {z_time}", about=f"{MY_BIO} | {z_time}"))
        except: pass
        await asyncio.sleep(60)

async def main():
    await client.start()
    print("🦅 الـمتمرد نـشط الآن..")
    asyncio.create_task(update_profile_loop())
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
