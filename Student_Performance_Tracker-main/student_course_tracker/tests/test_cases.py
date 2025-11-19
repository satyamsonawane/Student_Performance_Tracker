# new file -- add or edit as needed

import re
import pytest

# 1) TC-06 - ID generation uniqueness (unit)
def test_generate_student_id_uniqueness():
    id_mod = pytest.importorskip("app.utils.id_generator")
    gen = getattr(id_mod, "generate_student_id", None)
    if gen is None:
        pytest.skip("generate_student_id() not found in app.utils.id_generator - adapt test to your function name")

    N = 1000
    ids = [gen() for _ in range(N)]
    assert len(ids) == N
    assert len(set(ids)) == N, "Duplicate IDs produced"
    # example pattern: adjust according to your implementation
    pattern = re.compile(r"^S-\d+$")
    assert all(pattern.match(i) for i in ids), "IDs do not match expected pattern S-<digits>"

# 2) TC-01 - Signup (valid) (integration/flow skeleton)
def test_signup_valid_flow(monkeypatch, capsys):
    """
    Skeleton:
    - adapt to the actual module and function that runs signup (e.g. app.CLI.login.signup_flow)
    - monkeypatch builtins.input to supply name/email/password
    - monkeypatch the DB/create-user function used by signup to avoid touching real DB
    - assert expected output or that the mocked DB function was called with expected args
    """
    login_mod = pytest.importorskip("app.CLI.login")
    signup_fn = getattr(login_mod, "signup_flow", None)
    if signup_fn is None:
        pytest.skip("signup_flow() not found in app.CLI.login - adapt to your CLI signup entry")

    # example inputs
    inputs = iter(["Alice Example", "alice@example.com", "Password123"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    called = {}
    # find DB call used by signup and patch it. adjust names as needed:
    for attr_name in ("create_user", "register_user", "signup_user"):
        if hasattr(login_mod, attr_name):
            monkeypatch.setattr(login_mod, attr_name, lambda *a, **k: {"id": "S-1001"})
            called["patched"] = attr_name
            break
    if "patched" not in called:
        # If signup_flow calls a DB helper in another module, patch that instead.
        pytest.skip("No known create_user helper found to patch in app.CLI.login; adapt test to patch DB helper used by signup")

    # run signup flow
    signup_fn()

    # capture output and assert some success message (adjust to your CLI text)
    out, err = capsys.readouterr()
    assert "success" in out.lower() or "created" in out.lower() or "id" in out.lower()

# 3) TC-02 - Signup duplicate email (integration/validation skeleton)
def test_signup_duplicate_email(monkeypatch):
    """
    Skeleton:
    - Simulate DB rejecting duplicate email (e.g., raise IntegrityError)
    - Patch DB helper used by signup to raise that error and assert CLI handles it
    """
    login_mod = pytest.importorskip("app.CLI.login")
    signup_fn = getattr(login_mod, "signup_flow", None)
    if signup_fn is None:
        pytest.skip("signup_flow() not found in app.CLI.login - adapt to your CLI signup entry")

    inputs = iter(["Bob Example", "duplicate@example.com", "Password123"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    # try to import psycopg2 IntegrityError for realistic exception, fall back to Exception
    try:
        from psycopg2 import IntegrityError  # type: ignore
    except Exception:
        IntegrityError = Exception  # fallback for skeleton

    # patch create_user to raise IntegrityError
    for attr_name in ("create_user", "register_user", "signup_user"):
        if hasattr(login_mod, attr_name):
            def _bad_create(*a, **k):
                raise IntegrityError("duplicate key value violates unique constraint")
            monkeypatch.setattr(login_mod, attr_name, _bad_create)
            break
    else:
        pytest.skip("No known create_user helper found to patch in app.CLI.login; adapt test to patch DB helper used by signup")

    # When signup_fn runs it should handle/print an error instead of crashing
    with pytest.raises(Exception):
        # If your CLI catches DB errors and prints them instead of raising,
        # replace this with a call and assert printed text.
        signup_fn()

# 4) TC-05 - Score add bounds (validation skeleton)
def test_add_score_bounds(monkeypatch, capsys):
    """
    Skeleton:
    - Patch CLI inputs for adding scores
    - Patch DB helper that inserts scores so we don't touch real DB
    - Verify negative and >100 rejected; valid score accepted
    """
    score_mod = pytest.importorskip("app.CLI.scores")  # adjust module path
    add_score_fn = getattr(score_mod, "add_score_flow", None)
    if add_score_fn is None:
        pytest.skip("add_score_flow() not found in app.CLI.scores - adapt to your function name")

    # Test invalid negative score
    inputs_neg = iter(["S-1001", "Math", "-5"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs_neg))
    # patch DB insert if exists
    if hasattr(score_mod, "insert_score"):
        monkeypatch.setattr(score_mod, "insert_score", lambda *a, **k: True)
    # run and capture output
    add_score_fn()
    out, _ = capsys.readouterr()
    assert "invalid" in out.lower() or "range" in out.lower() or "0" in out.lower()

    # Test invalid >100
    inputs_hi = iter(["S-1001", "Math", "105"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs_hi))
    add_score_fn()
    out, _ = capsys.readouterr()
    assert "invalid" in out.lower() or "range" in out.lower()

    # Test valid 85
    recorded = {}
    def _record_insert(student_id, subject, score):
        recorded.update({"student_id": student_id, "subject": subject, "score": score})
        return True
    if hasattr(score_mod, "insert_score"):
        monkeypatch.setattr(score_mod, "insert_score", _record_insert)
    inputs_ok = iter(["S-1001", "Math", "85"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs_ok))
    add_score_fn()
    assert recorded.get("score") == 85 or recorded.get("score") == "85"

# 5) TC-09 - Report generation / average calc (unit skeleton)
def test_average_calculation():
    """
    Skeleton:
    - If you have a report or util function that computes averages, import it and test.
    - Example expects a function compute_average(list_of_numbers) -> float
    """
    reports_mod = pytest.importorskip("app.utils.reports")
    compute_avg = getattr(reports_mod, "compute_average", None)
    if compute_avg is None:
        pytest.skip("compute_average() not found in app.utils.reports - adapt to your function name")

    scores = [70, 80, 90]
    avg = compute_avg(scores)
    assert pytest.approx(avg, rel=1e-6) == 80.0