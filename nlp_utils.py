# nlp_utils.py
import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

DEPT_SYNONYMS = {
    "dentistry": ["dentist", "dental", "dental clinic", "tooth doctor"],
    "dermatology": ["dermatologist", "skin doctor", "skin clinic", "derma"],
    "ophthalmology": ["ophthalmologist", "eye doctor", "eye clinic", "optometrist"],
    "cardiology": ["cardiologist", "heart doctor", "cardio clinic"],
    "general physician": ["gp", "physician", "family doctor", "general doctor"],
}

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
for canonical, synonyms in DEPT_SYNONYMS.items():
    patterns = [nlp.make_doc(canonical)] + [nlp.make_doc(s) for s in synonyms]
    matcher.add(canonical, patterns)

def extract_department_spacy(text: str):
    txt = text.strip().strip('"').strip("'")
    doc = nlp(txt)
    matches = matcher(doc)
    if not matches:
        return None
    canonical = nlp.vocab.strings[matches[0][0]]
    return " ".join([w.capitalize() for w in canonical.split()])

def extract_entities(text: str):
    dept = extract_department_spacy(text)
    return {
        "department": dept,
        "raw_text": text,
    }
