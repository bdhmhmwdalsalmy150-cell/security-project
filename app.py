import subprocess
import re

def run_command(user_input):
    # التحقق من أن المدخلات تحتوي فقط على أحرف وأرقام لضمان الأمان
    if not re.match("^[A-Za-z0-9]+$", user_input):
        raise ValueError("مدخلات غير صالحة!")
    
    # تنفيذ الأمر بشكل آمن
    result = subprocess.run(["echo", user_input], capture_output=True, text=True)
    return result.stdout

if __name__ == "__main__":
    print("تم تشغيل التطبيق بنجاح وبشكل آمن.")
