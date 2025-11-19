# ==============================
# ADD AND VALIDATE STUDENT SCORE
# ==============================
from app.utils import validators

def add_score_flow():
    student_id = input("Student ID: ").strip()
    subject = input("Subject: ").strip()
    score_raw = input("Score (0-100): ").strip()

    if not validators.is_nonempty(student_id) or not validators.is_nonempty(subject):
        print("student id and subject required"); return
    if not validators.is_valid_score(score_raw):
        print("invalid score — must be number between 0 and 100"); return
    score = float(score_raw)
