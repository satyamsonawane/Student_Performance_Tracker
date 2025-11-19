import re
from typing import List

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def is_nonempty(s: str) -> bool:
    return bool(s and s.strip())

def is_valid_email(email: str) -> bool:
    return bool(email and EMAIL_RE.match(email))

def is_valid_password(pw: str) -> bool:
    # minimum length 6 to match CLI prompts (adjust if you prefer stricter rules)
    return bool(pw and len(pw) >= 6)

def is_valid_score(val) -> bool:
    try:
        v = float(val)
        return 0.0 <= v <= 100.0
    except Exception:
        return False


def collect_student_validation(name: str, email: str, password: str) -> list:
    """Return list of validation error messages for a signup attempt."""
    errs = []
    if not is_nonempty(name):
        errs.append("name required")
    if not is_valid_email(email):
        errs.append("invalid email")
    if not is_valid_password(password):
        errs.append("password must be at least 6 characters")
    return errs
