from pyrogram import Client

# بياناتك
API_ID = 22610186
API_HASH = "184e7fd176413cd0d2425494f1796229"
BOT_TOKEN = "8794844755:AAHA6yvFrM2rEm6A2II1LlenrFOl8ZjfGVE"

# إعداد البوت باسم فخم وتنسيق احترافي
app = Client(
    "AL-MUTAMARRID-V2",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

if __name__ == "__main__":
    print("-----------------------------------------")
    print("🛡️  AL-MUTAMARRID SOURCE IS NOW LIVE!  🛡️")
    print("🚀 THE REBEL PROJECT STARTED SUCCESSFULLY")
    print("-----------------------------------------")
    app.run()
