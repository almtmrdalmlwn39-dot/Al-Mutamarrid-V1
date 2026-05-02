from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from config import API_ID, API_HASH

print("🔄 جاري الاتصال لاستخراج الجلسة النصية...")
with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    session_string = client.session.save()
    print("\n✅ تم استخراج كود الجلسة بنجاح!\n")
    print("👇 انسخ هذا الكود واحفظه في مكان آمن:")
    print(f"\n{session_string}\n")
    print("⚠️ ملاحظة: لا تشارك هذا الكود مع أحد، لأنه يفتح حسابك.")
