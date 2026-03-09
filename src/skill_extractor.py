import nltk

nltk.download('punkt')

def extract_skills(text, skill_list):

    text = text.lower()

    extracted_skills = []

    for skill in skill_list:

        if skill.lower() in text:
            extracted_skills.append(skill)

    return extracted_skills