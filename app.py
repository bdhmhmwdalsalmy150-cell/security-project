from flask import Flask, render_template_string, request, make_response
import re
import subprocess

app = Flask(__name__)

# 1. إضافة رؤوس الأمان (Security Headers) لكل الطلبات
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

# 2. صفحات الأخطاء المخصصة لمنع تسريب معلومات النظام والحمسارات الحساسة
@app.errorhandler(404)
def page_not_found(e):
    return "<h3>404 - الصفحة غير موجودة أو المسار محظور</h3>", 404

@app.errorhandler(500)
def internal_server_error(e):
    return "<h3>500 - حدث خطأ داخلي في الخادم</h3>", 500

# واجهة تطبيق الويب والفلتر الأمني (WAF Simulation)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>فحص الأمان ومحاكاة WAF</title>
    <style>
        body { font-family: Tahoma, sans-serif; background-color: #f4f7f6; text-align: center; padding-top: 50px; }
        .card { background: white; width: 500px; margin: auto; padding: 30px; border-radius: 8px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); }
        input[type="text"] { width: 80%; padding: 10px; margin: 15px 0; border: 1px solid #ccc; border-radius: 4px; }
        button { background-color: #5c6bc0; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
        button:hover { background-color: #3f51b5; }
        .alert { color: #d32f2f; font-weight: bold; margin-top: 15px; }
        .success { color: #388e3c; font-weight: bold; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>فحص الأمان ومحاكاة WAF</h2>
        <form method="POST">
            <input type="text" name="user_input" placeholder="أدخل النص أو الأمر هنا..." required>
            <br>
            <button type="submit">إرسال وفحص</button>
        </form>
        {% if result %}
            <div class="{{ status }}">
                {{ result }}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    status = None
    if request.method == "POST":
        user_input = request.form.get("user_input", "")
        
        # فلتر الأمان (WAF Rule): السماح فقط بالحروف، الأرقام، المسافات، والشرطات
        if not re.match(f"^[a-zA-Z0-9\\s_\\-]+$", user_input):
            result = "Security Alert: Malicious or invalid characters detected! Request blocked."
            status = "alert"
        else:
            result = f"Input passed WAF securely: {user_input}"
            status = "success"
            
    return render_template_string(HTML_TEMPLATE, result=result, status=status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
