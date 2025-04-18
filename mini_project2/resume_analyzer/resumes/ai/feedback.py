
def analyze_resume_feedback(parsed_resume: dict, job_description: str = None) -> dict:
    feedback = []

    # Skill gap analysis (примитивно, с mock-данными)
    expected_skills = {"Python", "Django", "REST", "Docker"}
    resume_skills = set(parsed_resume.get("skills", []))
    missing_skills = expected_skills - resume_skills
    if missing_skills:
        feedback.append(f"Рекомендуется изучить: {', '.join(missing_skills)}")

    # Formatting tips
    if not parsed_resume.get("experience"):
        feedback.append("Добавьте опыт работы в резюме.")

    # ATS keywords (пример)
    if job_description:
        keywords = {kw.lower() for kw in job_description.split() if len(kw) > 3}
        matched = [kw for kw in resume_skills if kw.lower() in keywords]
        if len(matched) < 3:
            feedback.append("Добавьте больше ключевых слов из описания вакансии.")

    return {
        "feedback": feedback,
        "match_score": len(resume_skills & expected_skills) / len(expected_skills)
    }
