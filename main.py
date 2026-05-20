import asyncio
from pyrogram import Client

# بيانات AL-MUTAMARRID
API_ID = 22610186
API_HASH = "184e7fd176413cd0d2425494f1796229"
BOT_TOKEN = "8794844755:AAHA6yvFrM2rEm6A2II1LlenrFOl8ZjfGVE"

app = Client(
    "AL-MUTAMARRID-V2",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

async def main():
    await app.start()
    print("-----------------------------------------")
    print("🛡️  AL-MUTAMARRID SOURCE IS NOW LIVE!  🛡️")
    print("-----------------------------------------")
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
