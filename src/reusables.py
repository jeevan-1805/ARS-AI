from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

resume_features = [
    "education",
    "ofjobs",
    "yearsexp",
    "honors",
    "volunteer",
    "military",
    "empholes",
    "workinschool",
    "email",
    "computerskills",
    "specialskills",
]

jd_features = [
    "kind",
    "manager",
    "supervisor",
    "secretary",
    "offsupport",
    "salesrep",
    "retailsales",
    "schoolreq",
    "expreq",
    "expminreq",
    "comreq",
    "educreq",
    "compreq",
    "orgreq",
]

derived_features = [
    "expminreq_years",
    "experience_gap",
    "experience_meets_requirement",
    "education_meets_requirement",
    "computer_requirement_met",
    "communication_requirement_met",
    "organization_requirement_met",
]

audit_features = [
    "firstname",
    "sex",
    "race",
]

target_col = "call"

include_cols = resume_features + jd_features + derived_features + audit_features + [target_col]

one_hot_cols = [
    "kind",
    "experience_requirement_type"
]

ordinal_cols = [
    "schoolreq"
]

schoolreq_mapping = {
    "0": 0,
    "hsg": 1,
    "somcol": 2,
    "colp": 3
}

numeric_cols = [
    "education",
    "ofjobs",
    "yearsexp",
]

binary_cols = [
    "honors",
    "volunteer",
    "military",
    "empholes",
    "workinschool",
    "email",
    "computerskills",
    "specialskills",
]


section_headings = {
    "summary",
    "objective",
    "education",
    "experience",
    "work experience",
    "professional experience",
    "skills",
    "technical skills",
    "soft skills",
    "projects",
    "relevant projects",
    "relevant project",
    "certifications",
    "certification",
    "courses and certification",
    "courses and certifications",
    "achievements",
    "awards",
    "honors",
    "volunteer",
    "volunteering",
    "military",
    "military service",
    "contact",
    "contact information",
    "personal details",
}

FEATURE_DESCRIPTIONS = {
    "education": """
    Candidate's highest completed formal education or academic
    qualification, including school, college, university, diploma,
    bachelor's degree, master's degree, or other postgraduate study.
    """,

    "ofjobs": """
    Number of distinct previous jobs, employment positions, or
    professional work roles held by the candidate.
    """,

    "yearsexp": """
    Candidate's total professional or practical work experience,
    including employment and internships, expressed in years.
    """,

    "honors": """
    Candidate's honors, awards, academic distinctions, prizes,
    scholarships, achievements, or formal recognitions.
    """,

    "volunteer": """
    Candidate's volunteer work, community service, nonprofit work,
    or other unpaid service activities.
    """,

    "military": """
    Candidate's military service, military training, or military
    work experience.
    """,

    "empholes": """
    Candidate's employment history, including previous employers,
    professional positions, and work experience.
    """,

    "workinschool": """
    Work or employment performed by the candidate while attending
    school, college, or university.
    """,

    "email": """
    Candidate's email address or email contact information with '@' symbol.
    """,

    "computerskills": """
    Candidate's computer and technical skills, including programming
    languages, software, frameworks, databases, operating systems,
    development tools, and other computer technologies.
    """,

    "specialskills": """
    Candidate's additional, specialized, or professional skills
    relevant to their capabilities and work.
    """
}

FEATURE_VALUE_CODES = {
    "education": """
Give a numeric value as output.

Extract the candidate's highest completed education level.

Use these values:
0 = no formal education or education level cannot be determined
1 = high school or equivalent
2 = high school diploma completed
3 = any college or other undergraduate qualification equalant
4 = Bachelor's degree such as BCA, B.com, B.sc or other equalant
5 = postgraduate degree such as master's degree, MBA, M.Tech, or higher

Return only the numeric value. Strictly no text/strings
""",

    "ofjobs": """
Give a whole number as output.

Count the distinct previous jobs or professional employment positions
held by the candidate.

Count internships as practical positions only when they represent a
distinct work/internship position.

Return only the number. Strictly no text/strings
If there is no previous job or internship, return 0.
""",

    "yearsexp": """
Extract the total number of years of work experience mentioned in the resume.

Return ONLY the numeric value.

Examples of valid answers:
0
1
2
3
5
7.5

If the resume does not mention any work experience, return:
0

Do NOT return:
"numeric"
"years"
"years of experience"
"unknown"
"not mentioned"
"some"

The answer must contain only a number.
""",

    "honors": """
Return only 1 or 0. Strictly no text/strings

1 = the candidate has any explicit honor, award, academic distinction,
prize, scholarship, or formal recognition.

0 = none is explicitly mentioned.
""",

    "volunteer": """
Return only 1 or 0. Strictly no text/strings

1 = the candidate explicitly has volunteer work, community service,
nonprofit work, or unpaid service experience. don't consider internship or project.

0 = none is explicitly mentioned.
""",

    "military": """
Determine whether the resume mentions military service or military experience.

Return ONLY one value:

1 = The candidate has military service or military experience.
0 = The resume contains no evidence of military service or military experience.

Valid outputs are ONLY:
0
1

If there is no military-related information in the provided resume context, return 0.

Do NOT return the resume text.
Do NOT return an explanation.
Do NOT return job titles.
Do NOT return any other words or numbers.
""",

    "empholes": """
Determine whether the resume shows employment gaps or periods of unemployment.

Return ONLY one value:

1 = The resume indicates employment gaps, unemployment periods, or significant gaps between jobs.
0 = The resume does not indicate employment gaps or unemployment periods.

Valid outputs are ONLY:
0
1

If there is not enough evidence in the resume context to identify an employment gap, return 0.

Do NOT return the resume text.
Do NOT return an explanation.
Do NOT return dates.
Do NOT return job titles.
Do NOT return any other words or numbers.
""",

    "workinschool": """
Return only 1 or 0. Strictly no text/strings

1 = the candidate explicitly worked in a job, internship, or other
employment while attending school, college, or university.

0 = this is not explicitly supported by the resume.
""",

    "email": """
Return only 1 or 0. Strictly no text/strings

1 = an email address with '@' is present in the candidate's resume.

0 = no email address is present.
""",

    "computerskills": """
Return only 1 or 0. Strictly no text/strings

1 = the candidate explicitly demonstrates computer or technical skills,
such as programming languages, software, databases, frameworks,
operating systems, development tools, or other computer technologies.

0 = no computer or technical skills are explicitly identified.

Valid outputs are ONLY:
0
1

Do NOT return the resume text.
Do NOT return an explanation.
Do NOT return dates.
Do NOT return job titles.
Do NOT return any other words or numbers.
""",

    "specialskills": """
Return only 1 or 0. Strictly no text/strings

1 = the candidate has explicit additional or special professional skills
that are relevant to their capabilities.

0 = no such skills are explicitly identified.

Valid outputs are ONLY:
0
1

Do NOT return the resume text.
Do NOT return an explanation.
Do NOT return dates.
Do NOT return job titles.
Do NOT return any other words or numbers.
"""
}

req_feats_names = ["kind", "manager", "supervisor", "secretary", "offsupport", "salesrep", "retailsales", "schoolreq", "expreq", "required_experience_years", "experience_requirement_type", "comreq", "educreq", "compreq", "orgreq"]
cand_feats_names = ['education', 'ofjobs', 'yearsexp', 'honors', 'volunteer', 'military', 'empholes', 'workinschool', 'email', 'computerskills', 'specialskills']
from sentence_transformers import SentenceTransformer
import streamlit as st
@st.cache_resource
def load_sentence_transformer():
    MODEL_PATH = PROJECT_ROOT / "models" / "sentence_transformer"
    return SentenceTransformer(str(MODEL_PATH))

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

@st.cache_resource
def load_nlp_model():
    MODEL_PATH = PROJECT_ROOT / "models" / "nlp_model"
    tokenizer = AutoTokenizer.from_pretrained(str(MODEL_PATH), local_files_only=True)
    semantic_model = AutoModelForSeq2SeqLM.from_pretrained(str(MODEL_PATH), local_files_only=True)
    return tokenizer, semantic_model
