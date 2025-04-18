import spacy

nlp = spacy.load("en_core_web_sm")  # предварительно установите модель spaCy


def analyze_resume_text(text):
    doc = nlp(text)
    skills = []
    education = []
    experience = []

    for ent in doc.ents:
        if ent.label_ in ["ORG", "GPE"]:
            education.append(ent.text)
        elif ent.label_ in ["DATE", "TIME"]:
            experience.append(ent.text)
        elif ent.label_ == "PERSON":
            continue
        else:
            skills.append(ent.text)

    return {
        "skills": list(set(skills)),
        "education": list(set(education)),
        "experience": list(set(experience)),
    }
