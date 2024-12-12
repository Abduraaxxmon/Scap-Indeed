from email.policy import default

from job_skills_mapping import job_list_sorted

# Load SpaCy's pre-trained model


# Define the function to extract skills
def extract_skills(text, skills_list=job_list_sorted):
    text_lower = text.lower()
    extracted_skills = [skill for skill in skills_list if skill.lower() in text_lower]
    return ",".join(set(extracted_skills))

