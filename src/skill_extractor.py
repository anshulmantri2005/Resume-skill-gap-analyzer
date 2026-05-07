import re

GLOBAL_SKILLS = [
    "Python",
    "Java",
    "SQL",
    "React",
    "Node.js",
    "FastAPI",
    "Django",
    "TensorFlow",
    "PyTorch",
    "Machine Learning",
    "Deep Learning",
    "LLM",
    "RAG",
    "LangChain",
    "Docker",
    "Kubernetes",
    "AWS",
    "Power BI",
    "Tableau",
    "Statistics",
    "Pandas",
    "Linux",
    "Terraform",
    "Jenkins"
]


def extract_skills(text):

    text = text.lower()

    extracted_skills = []

    for skill in GLOBAL_SKILLS:

        pattern = r'\b' + re.escape(skill.lower()) + r'\b'

        if re.search(pattern, text):
            extracted_skills.append(skill)

    return list(set(extracted_skills))

   
