from flask import Flask, request, render_template_string, abort
import re
import logging
import sys

# إعداد نظام تسجيل السجلات ليظهر مباشرة في سطر الأوامر وسجلات Railway
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - IP: %(ip)s - User-Agent: %(agent)s - Payload: %(payload)s - Message: %(message)s'
)
logger = logging.getLogger('WAF_Logger')

app = Flask(__name__)

# قائمة الأنماط والرموز المحظورة لمحاكاة جدار الحماية (WAF)
MALICIOUS_PATTERNS = [
    r"<script.*?>.*?</script.*?>",  # XSS
    r"union\s+select",              # SQL Injection
    r"or\s+1=1",                    # SQL Injection Bypass
    r"[';--]",                      # رموز SQL وخطوط الحظر
    r"drop\s+table",                # SQL Destruction
    r"exec\s*\(",                   # Code Execution
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>فحص الأمان ومحاكاة WAF</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f4f9; }
        h2 { color: #333; }
        form { margin-top: 20px; }
        input[type="text"] { padding: 10px; width: 300px; border: 1px solid #ccc; border-radius: 4px; }
        button { padding: 10px 20px; background-color: #4F46E5; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background-color: #4338CA; }
        .alert { color: #DC2626; font-weight: bold; margin-top: 20px; font-size: 18px; }
        .success { color: #16A34A; font-weight: bold; margin-top: 20px; font-size: 18px; }
    </style>
</head>
<body>
    <h2>فحص الأمان ومحاكاة WAF</h2>
    <form method="POST">
        <input type="text" name="user_input" placeholder="أدخل النص أو الأمر هنا..." required>
        <br><br>
        <button type="submit">إرسال وفحص</button>
    </form>
    {% if message %}
        <div class="{{ status }}">{{ message }}</div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    message = None
    status = None
    
    if request.method == 'POST':
        user_input = request.form.get('user_input', '')
        
        # استخراج عنوان الـ IP الحقيقي للمهاجم (خصوصاً عند العمل خلف بروكسي مثل Railway)
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        user_agent = request.headers.get('User-Agent', 'Unknown')
        
        # فحص المدخلات عبر مطابقة الأنماط الضارة
        is_malicious = False
        for pattern in MALICIOUS_PATTERNS:
            if re.search(pattern, user_input, re.IGNORECASE):
                is_malicious = True
                break
                
        if is_malicious:
            # تسجيل تفاصيل الهجوم في السجلات
            logger.warning("Blocked malicious input", extra={
                'ip': client_ip,
                'agent': user_agent,
                'payload': user_input,
                'message': 'WAF Blocked Attack'
            })
            
            message = "Security Alert: Malicious or invalid characters detected! Blocked by WAF/Input Filter"
            status = "alert"
        else:
            message = f"Success: Input is safe and accepted! (Value: {user_input})"
            status = "success"
            
    return render_template_string(HTML_TEMPLATE, message=message, status=status)

# تفعيل رؤوس الأمان لحماية التطبيق
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

# معالجة الأخطاء المخصصة لمنع كشف المسارات الداخلية
@app.errorhandler(404)
def page_not_found(e):
    return "<h2 style='text-align:center; margin-top:50px; color:#DC2626;'>404 - الصفحة غير موجودة أو المسار محظور</h2>", 404

@app.errorhandler(500)
def internal_server_error(e):
    return "<h2 style='text-align:center; margin-top:50px; color:#DC2626;'>500 - حدث خطأ داخلي في الخادم</h2>", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
