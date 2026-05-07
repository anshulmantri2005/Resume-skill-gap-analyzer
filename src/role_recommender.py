import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")


def recommend_roles(resume_skills):

    data = pd.read_csv("data/job_skills.csv")

    recommendations = []

    resume_text = " ".join(resume_skills)

    resume_embedding = model.encode([resume_text])

    for _, row in data.iterrows():

        role = row["job_role"]

        role_skills = row["skills"]

        role_embedding = model.encode([role_skills])

        similarity = cosine_similarity(
            resume_embedding,
            role_embedding
        )[0][0]

        recommendations.append({
            "role": role,
            "score": round(similarity * 100, 2)
        })

    recommendations = sorted(
        recommendations,
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations[:5]
