import re
import subprocess
import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

# صفحة HTML بسيطة لتجربة الإدخال مع حماية الـ WAF
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>محاكاة الجدار الناري - Security Project</title>
    <style>
        body { font-family: Tahoma, sans-serif; background-color: #f4f4f9; padding: 50px; text-align: center; }
        .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); display: inline-block; width: 400px; }
        input[type="text"] { width: 90%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; }
        input[type="submit"] { background: #5c6bc0; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
        input[type="submit"]:hover { background: #3f51b5; }
        .result { margin-top: 20px; font-weight: bold; }
        .error { color: #d32f2f; }
        .success { color: #388e3c; }
    </style>
</head>
<body>
    <div class="container">
        <h2>فحص الأمان ومحاكاة WAF</h2>
        <form method="POST">
            <input type="text" name="user_input" placeholder="أدخل النص أو الأمر هنا..." required>
            <br>
            <input type="submit" value="إرسال وفحص">
        </form>
        {% if result %}
            <div class="result success">النتيجة: {{ result }}</div>
        {% endif %}
        {% if error %}
            <div class="result error">{{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None
    if request.method == "POST":
        user_input = request.form.get("user_input", "")
        try:
            # --- جدار الحماية (WAF Simulation / Input Filter) ---
            if not re.match(r"^[a-zA-Z0-9\s_-]+$", user_input):
                raise ValueError("Security Alert: Malicious or invalid characters detected! Blocked by WAF/Input Filter.")
            
            # تنفيذ آمن للأمر
            res = subprocess.run(["echo", user_input], capture_output=True, text=True, check=True)
            result = res.stdout.strip()
        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = "حدث خطأ غير متوقع أثناء المعالجة."
            
    return render_template_string(HTML_TEMPLATE, result=result, error=error)

if __name__ == "__main__":
    # قراءة المنفذ (Port) المخصص من منصة Railway أو استخدام المنفذ 5080 افتراضياً
    port = int(os.environ.get("PORT", 5080))
    app.run(host="0.0.0.0", port=port)
