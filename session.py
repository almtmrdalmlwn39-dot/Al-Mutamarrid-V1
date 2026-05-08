from telethon.sync import TelegramClient
from telethon.sessions import StringSession

print("🛡️ -- [ مـسـتـخـرج جـلـسـات 𝗔𝗟-𝗠𝗨𝗧𝗔𝗠𝗔𝗥𝗥𝗜𝗗 ] -- 🛡️")

# إدخال البيانات يدوياً لضمان العمل في أي بيئة
APP_ID = int(input("1. أدخل الـ API_ID الخاص بك: "))
APP_HASH = input("2. أدخل الـ API_HASH الخاص بك: ")

print("\n🔄 جـاري الاتـصال بـخـوادم تـلـيـجـرام...")

try:
    with TelegramClient(StringSession(), APP_ID, APP_HASH) as client:
        session_string = client.session.save()
        print("\n✅ تـم اسـتـخراج كـود الـجـلـسة بـنـجـاح!")
        print("\n👇 انـسـخ هـذا الـكـود (يـبـدأ بـ 1BV...) واحـفـظـه بـسـرية:")
        print(f"\n{session_string}\n")
        print("⚠️ تـحـذيـر: لا تـشـارك هـذا الـكـود مـع أحـد نـهـائـيـاً.")
except Exception as e:
    print(f"\n❌ حـدث خـطأ: {e}")
