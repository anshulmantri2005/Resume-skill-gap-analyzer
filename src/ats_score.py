def calculate_ats_score(resume_text, matched_skills, missing_skills):

    score = 0

    if len(resume_text) > 1500:
        score += 20

    if len(matched_skills) >= 5:
        score += 30

    if "experience" in resume_text.lower():
        score += 15

    if "education" in resume_text.lower():
        score += 15

    if "project" in resume_text.lower():
        score += 10

    if len(missing_skills) < 3:
        score += 10

    return min(score, 100)
