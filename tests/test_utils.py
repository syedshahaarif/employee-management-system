from ems.utils import is_valid_email, is_valid_phone, validate_employee


def test_valid_email():
    assert is_valid_email("rahul@example.com")


def test_invalid_email():
    assert not is_valid_email("rahul@")
    assert not is_valid_email("not-an-email")


def test_phone_rules():
    assert is_valid_phone("")
    assert is_valid_phone("9876543210")
    assert not is_valid_phone("12345")
    assert not is_valid_phone("98765abcde")


def test_validate_employee_ok():
    assert validate_employee("Rahul", "rahul@example.com", "9876543210", 50000) == []


def test_validate_employee_errors():
    errors = validate_employee("", "bad", "123", -1)
    assert len(errors) == 4
