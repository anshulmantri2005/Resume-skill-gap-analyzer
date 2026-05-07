import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-pro")


def generate_ai_analysis(resume_text, matched_skills, missing_skills, recommended_roles, ats_score):

    prompt = f"""
    Analyze this resume.

    Resume:
    {resume_text}

    Matched Skills:
    {matched_skills}

    Missing Skills:
    {missing_skills}

    Recommended Roles:
    {recommended_roles}

    ATS Score:
    {ats_score}

    Give:
    1. Best suited job role
    2. Missing skills
    3. Resume improvements
    4. Career roadmap
    5. Certifications
    """

    response = model.generate_content(prompt)

    return response.text
