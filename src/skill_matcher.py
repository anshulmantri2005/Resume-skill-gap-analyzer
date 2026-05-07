from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')


def match_skills(resume_skills, job_skills):

    matched = []
    missing = []

    for skill in job_skills:

        if skill in resume_skills:
            matched.append(skill)

        else:
            missing.append(skill)

    score = (len(matched) / len(job_skills)) * 100

    return matched, missing, score

def semantic_match(resume_text, job_text):

    resume_embedding = model.encode([resume_text])
    job_embedding = model.encode([job_text])

    similarity = cosine_similarity(
        resume_embedding,
        job_embedding
    )[0][0]

    return round(similarity * 100, 2)
    
