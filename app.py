import subprocess

def run_command(user_input):
    # الطريقة الآمنة: استخدام subprocess.run مع تمرير الأوامر كقائمة لتجنب ثغرات حقن الأوامر
    # كما يُفضل دائماً التحقق من صحة مدخلات المستخدم (Validation) أو تقييدها بقائمة مسموحة
    safe_input = user_input.strip()
    
    # مثال على التحقق من أن المدخل لا يحتوي على رموز خطرة
    if not safe_input.isalnum():
        raise ValueError("مدخلات غير صالحة!")

    # تشغيل الأمر بطريقة آمنة بدون دمج نصوص مباشر
    subprocess.run(["echo", safe_input], check=True)

if __name__ == "__main__":
    run_command("test")
