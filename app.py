import streamlit as st
import pandas as pd

from src.resume_parser import extract_text_from_pdf
from src.skill_extractor import extract_skills
from src.skill_matcher import match_skills
from src.skill_matcher import semantic_match
from src.role_recommender import recommend_roles
from src.ats_score import calculate_ats_score
from src.gemini_service import generate_ai_analysis


st.set_page_config(
    page_title="AI Resume Intelligence Platform",
    layout="wide"
)

st.title("AI Resume Intelligence Platform")

st.write("Upload your resume for AI-powered analysis")

# load dataset

data = pd.read_csv("data/job_skills.csv")


# upload
uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

if uploaded_file is not None:

    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    resume_text = extract_text_from_pdf("temp_resume.pdf")


    # extract skills
    resume_skills = extract_skills(resume_text)


    st.subheader("Extracted Skills")
    st.write(resume_skills)
    # recommend roles
    recommended_roles = recommend_roles(resume_skills)


    top_role = recommended_roles[0]['role']


    job_skills = data[
        data['job_role'] == top_role
    ]['skills'].values[0].split(',')


    matched, missing, score = match_skills(
        resume_skills,
        job_skills
    )


    semantic_score = semantic_match(
        resume_text,
        " ".join(job_skills)
    )

    ats_score = calculate_ats_score(
        resume_text,
        matched,
        missing
    )


    ai_analysis = generate_ai_analysis(
        resume_text,
        matched,
        missing,
        recommended_roles,
        ats_score
    )


    st.subheader("Recommended Job Roles")

    for role in recommended_roles:
        st.write(
            f"{role['role']} → {role['score']}% Match"
        )
    st.subheader("Matched Skills")
    st.success(matched)


    st.subheader("Missing Skills")
    st.error(missing)


    st.subheader("ATS Score")
    st.metric("ATS Score", f"{ats_score}%")


    st.subheader("Semantic Match Score")
    st.metric(
        "Semantic Similarity",
        f"{semantic_score}%"
    )


    st.subheader("AI Career Analysis")
    st.write(ai_analysis)
    
