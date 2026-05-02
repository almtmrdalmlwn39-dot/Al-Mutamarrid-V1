import os
import glob
import importlib.util
from telethon import TelegramClient
from telethon.sessions import StringSession
from config import API_ID, API_HASH, SESSION
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Al-Mutamarrid is Active!')

def run_health_check():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# تشغيل الخادم في الخلفية لإرضاء Render
threading.Thread(target=run_health_check, daemon=True).start()

# تشغيل العميل باستخدام الجلسة المستخرجة
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

def load_plugins():
    # البحث عن كل ملفات الموديولات داخل مجلد plugins
    path = "plugins/*.py"
    files = glob.glob(path)
    for name in files:
        try:
            # تحويل مسار الملف لاسم موديول
            module_spec = importlib.util.spec_from_file_location("plugin", name)
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
            print(f"✅ تم تحميل الموديول: {os.path.basename(name)}")
        except Exception as e:
            print(f"❌ فشل تحميل {os.path.basename(name)} بسبب: {e}")

async def main():
    print("🚀 جاري تشغيل سورس المتمرد التقني...")
    load_plugins()
    # التحقق من الاتصال
    await client.start()
    print("🛡️ السورس شغال الآن! اذهب لتليجرام واكتب .اوامري")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())

