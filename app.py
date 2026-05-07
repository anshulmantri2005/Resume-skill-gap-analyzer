import streamlit as st
import pandas as pd

from src.resume_parser import extract_text_from_pdf
from src.skill_extractor import extract_skills
from src.skill_matcher import match_skills
from src.skill_matcher import semantic_match
from src.role_recommender import recommend_roles
from src.ats_score import calculate_ats_score
from src.gemini_service import generate_ai_analysis


# PAGE CONFIG
st.set_page_config(
    page_title="AI Resume Intelligence Platform",
    page_icon="🚀",
    layout="wide"
)


# CUSTOM CSS
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1 {
    color: white;
    font-size: 55px !important;
    font-weight: 800 !important;
}

h2, h3 {
    color: white;
}

.stFileUploader {
    border: 2px dashed #6C63FF;
    border-radius: 15px;
    padding: 20px;
    background: #161B22;
}

.metric-card {
    background: linear-gradient(135deg,#1f2937,#111827);
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    border: 1px solid #374151;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}

.skill-box {
    background-color: #1E293B;
    color: white;
    padding: 10px 18px;
    border-radius: 30px;
    display: inline-block;
    margin: 6px;
    font-size: 14px;
    font-weight: 600;
}

.role-card {
    background: #111827;
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 15px;
    border-left: 5px solid #8B5CF6;
}

.ai-box {
    background: linear-gradient(135deg,#111827,#1F2937);
    padding: 25px;
    border-radius: 20px;
    color: white;
    line-height: 1.8;
    border: 1px solid #374151;
}

</style>
""", unsafe_allow_html=True)


# HEADER
st.markdown("""
<h1>🚀 AI Resume Intelligence Platform</h1>
<p style='color:gray;font-size:18px;'>
Upload your resume and get AI-powered ATS analysis,
career guidance, and job role recommendations.
</p>
""", unsafe_allow_html=True)


# FILE UPLOADER
uploaded_file = st.file_uploader(
    "Upload Your Resume",
    type=["pdf"]
)


if uploaded_file is not None:

    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    # EXTRACT TEXT
    resume_text = extract_text_from_pdf(
        "temp_resume.pdf"
    )

    # EXTRACT SKILLS
    resume_skills = extract_skills(
        resume_text
    )

    # RECOMMEND ROLES
    recommended_roles = recommend_roles(
        resume_skills
    )

    top_role = recommended_roles[0]["role"]

    # LOAD DATASET
    data = pd.read_csv(
        "data/job_skills.csv"
    )

    job_skills = data[
        data["job_role"] == top_role
    ]["skills"].values[0].split(",")

    # MATCH SKILLS
    matched, missing, score = match_skills(
        resume_skills,
        job_skills
    )

    # ATS SCORE
    ats_score = calculate_ats_score(
        resume_text,
        matched,
        missing
    )

    # SEMANTIC SCORE
    semantic_score = semantic_match(
        resume_text,
        " ".join(job_skills)
    )

    # GEMINI ANALYSIS
    ai_analysis = generate_ai_analysis(
        resume_text,
        matched,
        missing,
        recommended_roles,
        ats_score
    )

    # DASHBOARD
    st.markdown("---")

    # METRICS
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h2>🎯 ATS Score</h2>
            <h1>{ats_score}%</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h2>🧠 Semantic Match</h2>
            <h1>{semantic_score}%</h1>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h2>💼 Best Role</h2>
            <h3>{top_role}</h3>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # SKILLS SECTION
    st.subheader("🛠 Extracted Skills")

    for skill in resume_skills:
        st.markdown(
            f'<div class="skill-box">{skill}</div>',
            unsafe_allow_html=True
        )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # RECOMMENDED ROLES
    st.subheader("💼 Recommended Job Roles")

    for role in recommended_roles:

        st.markdown(f"""
        <div class="role-card">
            <h3>{role['role']}</h3>
            <p style='color:#A78BFA;font-size:18px;'>
                Match Score: {role['score']}%
            </p>
        </div>
        """, unsafe_allow_html=True)

    # SKILL GAP
    col4, col5 = st.columns(2)

    with col4:

        st.subheader("✅ Matched Skills")

        for skill in matched:
            st.success(skill)

    with col5:

        st.subheader("❌ Missing Skills")

        for skill in missing:
            st.error(skill)

    st.markdown("<br>", unsafe_allow_html=True)

    # AI ANALYSIS
    st.subheader("🤖 AI Career Analysis")

    st.markdown(f"""
    <div class="ai-box">
    {ai_analysis}
    </div>
    """, unsafe_allow_html=True)

    # FOOTER
    st.markdown("---")

    st.markdown("""
    <center>
    <p style='color:gray;'>
    Built with ❤️ using Streamlit + Gemini AI
    </p>
    </center>
    """, unsafe_allow_html=True)
