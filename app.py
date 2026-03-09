import streamlit as st
import pandas as pd

from src.resume_parser import extract_text_from_pdf
from src.skill_extractor import extract_skills
from src.skill_matcher import match_skills


st.title("Resume Screening & Skill Gap Analyzer")

# load dataset
data = pd.read_csv("data/job_skills.csv")

# job role selection
job_role = st.selectbox("Select Job Role", data["job_role"].unique())

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

if uploaded_file is not None:

    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    resume_text = extract_text_from_pdf("temp_resume.pdf")

    job_skills = data[data["job_role"] == job_role]["skills"].values[0].split(",")

    resume_skills = extract_skills(resume_text, job_skills)

    matched, missing, score = match_skills(resume_skills, job_skills)

    st.subheader("Analysis Result")

    st.write("Matched Skills:", matched)

    st.write("Missing Skills:", missing)

    st.write("Skill Match Score:", round(score, 2), "%")