
import os

def run_command(user_input):
    # ثغرة أمنية متعمدة: تنفيذ أمر نظام خارجي بناءً على مدخلات المستخدم مباشرة (Command Injection)
    os.system("echo " + user_input)

if __name__ == "__main__":
    run_command("test")
