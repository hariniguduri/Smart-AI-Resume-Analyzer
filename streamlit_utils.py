from datetime import datetime

import pandas as pd

from models import ResumeAnalysis, get_session


ALLOWED_EXTENSIONS = {"pdf", "docx"}


def validate_uploaded_resume(uploaded_file):
    if uploaded_file is None:
        return False, "Please upload a resume file."

    file_name = (uploaded_file.name or "").strip()
    if "." not in file_name:
        return False, "Invalid file name."

    extension = file_name.rsplit(".", 1)[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        return False, "Only PDF and DOCX files are allowed."

    if uploaded_file.size == 0:
        return False, "The uploaded file is empty."

    return True, ""


def format_skills_for_storage(skills):
    if not skills:
        return ""

    cleaned_skills = []
    seen = set()
    for skill in skills:
        skill_text = str(skill).strip()
        if skill_text and skill_text.lower() not in seen:
            cleaned_skills.append(skill_text)
            seen.add(skill_text.lower())
    return ", ".join(cleaned_skills)


def save_user_analysis(user_id, filename, extracted_skills, score):
    session = get_session()
    try:
        analysis = ResumeAnalysis(
            user_id=user_id,
            filename=filename,
            extracted_skills=format_skills_for_storage(extracted_skills),
            score=float(score or 0),
            timestamp=datetime.utcnow()
        )
        session.add(analysis)
        session.commit()
        session.refresh(analysis)
        return analysis
    finally:
        session.close()


def get_user_history_dataframe(user_id):
    session = get_session()
    try:
        rows = (
            session.query(ResumeAnalysis)
            .filter(ResumeAnalysis.user_id == user_id)
            .order_by(ResumeAnalysis.timestamp.desc())
            .all()
        )

        if not rows:
            return pd.DataFrame()

        return pd.DataFrame([
            {
                "Analysis ID": row.id,
                "Filename": row.filename,
                "Extracted Skills": row.extracted_skills,
                "Score": row.score,
                "Timestamp": row.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for row in rows
        ])
    finally:
        session.close()


def delete_history_item(user_id, analysis_id):
    session = get_session()
    try:
        row = (
            session.query(ResumeAnalysis)
            .filter(
                ResumeAnalysis.id == analysis_id,
                ResumeAnalysis.user_id == user_id
            )
            .first()
        )
        if not row:
            return False, "History item not found."

        session.delete(row)
        session.commit()
        return True, "History item deleted."
    finally:
        session.close()
