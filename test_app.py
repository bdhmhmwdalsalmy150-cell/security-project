
import pytest
from app import run_command

def test_run_command_valid_input():
    # مدخلات سليمة يجب أن تمر دون أخطاء
    try:
        run_command("test123")
    except Exception as e:
        pytest.fail(f"فشل الاختبار لمدخل صالح: {e}")

def test_run_command_invalid_input():
    # مدخلات تحتوي على رموز أو مسافات يجب أن تثير استثناء ValueError
    with pytest.raises(ValueError, match="مدخلات غير صالحة!"):
        run_command("test; rm -rf /")
