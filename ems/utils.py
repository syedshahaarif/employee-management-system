import re

EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_RE.match(email.strip()))


def is_valid_phone(phone: str) -> bool:
    """Empty is allowed (optional field); otherwise 10 digits."""
    phone = phone.strip()
    return phone == "" or (phone.isdigit() and len(phone) == 10)


def validate_employee(name: str, email: str, phone: str, salary: float):
    """Return a list of error messages (empty list means valid)."""
    errors = []
    if not name.strip():
        errors.append("Name is required.")
    if not is_valid_email(email):
        errors.append("Enter a valid email address.")
    if not is_valid_phone(phone):
        errors.append("Phone must be 10 digits.")
    if salary < 0:
        errors.append("Salary cannot be negative.")
    return errors
