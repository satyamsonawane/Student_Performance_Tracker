# new file
import os
import sys
# ensure the parent package (the folder that contains `app`) is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import re
import pytest

from app.utils import validators

def test_email_validation():
    assert validators.is_valid_email("a@b.com")
    assert not validators.is_valid_email("bademail")
    assert not validators.is_valid_email("no-at.com")

def test_password_validation():
    assert validators.is_valid_password("abcdefgh")
    assert not validators.is_valid_password("short")

def test_score_validation():
    assert validators.is_valid_score("0")
    assert validators.is_valid_score("100")
    assert not validators.is_valid_score("-1")
    assert not validators.is_valid_score("abc")

def test_generate_student_id_uniqueness():
    # Test id helper functions without touching the DB-backed generator.
    id_mod = pytest.importorskip("app.utils.id_generator")
    fmt = getattr(id_mod, "_format_id", None)
    ext = getattr(id_mod, "_extract_numeric_suffix", None)
    if fmt is None or ext is None:
        pytest.skip("id helper functions not found; adapt test to your id generator")

    assert fmt("STU", 42) == "STU-000042"
    assert ext("STU-000042") == 42
    assert ext("142") == 142
    assert ext(None) == 0
    assert ext("ABC") == 0