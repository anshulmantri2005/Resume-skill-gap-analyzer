import streamlit as st
import pandas as pd

from src.resume_parser import extract_text_from_pdf
from src.skill_extractor import extract_skills
from src.skill_matcher import match_skills
from src.skill_matcher import semantic_match
from src.role_recommender import recommend_roles
from src.ats_score import calculate_ats_score
from src.gemini_service import generate_ai_analysis


# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="AI Resume Intelligence",
    page_icon="🚀",
    layout="wide"
)


# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(
        135deg,
        #050816 0%,
        #0B1023 45%,
        #111827 100%
    );
    color: white;
}

.block-container {
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

.hero-title {
    font-size: 64px;
    font-weight: 900;
    color: white;
    margin-bottom: 10px;
}

.gradient-text {
    background: linear-gradient(90deg, #7c3aed, #ec4899, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #9ca3af;
    font-size: 22px;
    margin-bottom: 40px;
}

.section-title {
    color: white;
    font-size: 38px;
    font-weight: 800;
    margin-top: 50px;
    margin-bottom: 25px;
}

</style>
""", unsafe_allow_html=True)


# =========================================
# HERO SECTION
# =========================================

st.markdown("""
<div class="hero-title">
🚀 AI Resume <span class="gradient-text">Intelligence</span>
</div>

<div class="hero-subtitle">
Next-generation AI-powered ATS analysis,
career intelligence, role prediction,
and hiring optimization platform.
</div>
""", unsafe_allow_html=True)


# =========================================
# FILE UPLOAD
# =========================================

uploaded_file = st.file_uploader(
    "Upload Your Resume",
    type=["pdf"]
)


# =========================================
# MAIN LOGIC
# =========================================

if uploaded_file is not None:

    # SAVE PDF
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

    # RECOMMENDED ROLES
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
    ]["skills"].values[0].split(", ")

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

    # AI ANALYSIS
    ai_analysis = generate_ai_analysis(
        resume_text,
        matched,
        missing,
        recommended_roles,
        ats_score
    )


    # =========================================
    # METRICS
    # =========================================

    st.markdown(
        '<div class="section-title">📊 Resume Intelligence</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="🎯 ATS Score",
            value=f"{ats_score}%"
        )

    with col2:
        st.metric(
            label="🧠 Semantic Match",
            value=f"{semantic_score}%"
        )

    with col3:
        st.metric(
            label="💼 Best Role",
            value=top_role
        )


    # =========================================
    # SKILLS DETECTED
    # =========================================

    st.markdown(
        '<div class="section-title">🛠 Skills Detected</div>',
        unsafe_allow_html=True
    )

    st.success(", ".join(resume_skills))


    # =========================================
    # RECOMMENDED ROLES
    # =========================================

    st.markdown(
        '<div class="section-title">💼 Recommended Roles</div>',
        unsafe_allow_html=True
    )

    for role in recommended_roles:

        st.subheader(role['role'])

        st.progress(
            min(int(role['score']), 100)
        )

        st.caption(
            f"Match Score: {role['score']}%"
        )

        st.divider()


    # =========================================
    # MATCHED SKILLS
    # =========================================

    st.markdown(
        '<div class="section-title">✅ Matched Skills</div>',
        unsafe_allow_html=True
    )

    st.success(", ".join(matched))


    # =========================================
    # MISSING SKILLS
    # =========================================

    st.markdown(
        '<div class="section-title">❌ Missing Skills</div>',
        unsafe_allow_html=True
    )

    st.error(", ".join(missing))


    # =========================================
    # AI ANALYSIS
    # =========================================

    st.markdown(
        '<div class="section-title">🤖 AI Career Analysis</div>',
        unsafe_allow_html=True
    )

    st.info(ai_analysis)
