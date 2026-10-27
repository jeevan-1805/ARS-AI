import pandas as pd
import joblib
from src.reusables import one_hot_cols, numeric_cols, binary_cols
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

one_hot_encoder = joblib.load("models/one_hot_encoder.pkl")
feature_names = joblib.load("models/X_feature_names.pkl")
model_p2 = joblib.load("models/semantic_model.pkl")
model_p1 = joblib.load("models/rf_model.pkl")

def build_req(job_type, manager, supervisor, secretary, offsupport, salesrep, retailsales, schoolreq, expreq, experience_type, experience_years, comreq, educreq, compreq, orgreq):
    schoolreq_mapping = {
        "No formal education requirement": 0,
        "High school diploma": 1,
        "Some college": 2,
        "College degree or higher": 3
    }

    requirements = {
        "kind": "a" if job_type == "Administrative / Clerical" else "s",
        "manager": int(manager),
        "supervisor": int(supervisor),
        "secretary": int(secretary),
        "offsupport": int(offsupport),
        "salesrep": int(salesrep),
        "retailsales": int(retailsales),

        "schoolreq": schoolreq_mapping[schoolreq],

        "expreq": 0 if expreq == "No experience required" else 1,

        "required_experience_years": experience_years,

        "experience_requirement_type": (
            "years"
            if expreq == "No experience required"
            else (
                "some"
                if experience_type == "Some experience required"
                else "years"
            )
        ),

        "comreq": int(comreq),
        "educreq": int(educreq),
        "compreq": int(compreq),
        "orgreq": int(orgreq)
    }

    return pd.DataFrame([requirements])

def build_test(candidate_features, requirements_df):
    X_test = pd.DataFrame([candidate_features])

    for column in numeric_cols:
        try:
            X_test[column] = pd.to_numeric(X_test[column], errors="raise")
        except ValueError:
            st.error(f"Invalid value for feature '{column}': {X_test[column].iloc[0]}")
            raise

    for column in binary_cols:
        try:
            X_test[column] = pd.to_numeric(X_test[column], errors="raise").astype(int)
        except ValueError:
            st.error(f"Invalid value for feature '{column}': {X_test[column].iloc[0]}")
            raise

    X_test["col"] = (X_test["education"] >= 4).astype(int)
    X_test = pd.concat([X_test, requirements_df], axis=1)
    encoded_array = one_hot_encoder.transform(X_test[one_hot_cols])
    encoded_df = pd.DataFrame(encoded_array, columns=one_hot_encoder.get_feature_names_out(one_hot_cols), index=X_test.index)

    X_test = X_test.drop(columns=one_hot_cols)
    X_test = X_test.join(encoded_df)
    X_test = X_test[feature_names]

    return X_test

def build_p2_X(resume_text, jd_text, embedding_model):
    resume_embeds = embedding_model.encode(resume_text, convert_to_numpy=True)
    jd_embeds = embedding_model.encode(jd_text, convert_to_numpy=True)
    resume_embeds = resume_embeds.reshape(1, -1)  
    jd_embeds = jd_embeds.reshape(1, -1)
    similarity_mat = cosine_similarity(resume_embeds, jd_embeds)
    cs = similarity_mat.diagonal().reshape(-1, 1)
    return pd.DataFrame(cs, columns=['similarity'])

FINAL_THRESHOLD = 0.46

p1_recall = 0.5301
p1_f1 = 0.2310

p2_recall = 0.3360
p2_f1 = 0.4179

p1_score = 0.6 * p1_recall + 0.4 * p1_f1
p2_score = 0.6 * p2_recall + 0.4 * p2_f1

total_score = p1_score + p2_score

P1_WEIGHT = p1_score / total_score
P2_WEIGHT = p2_score / total_score

def predict_final(p1_test, p2_test):
    P1 = model_p1.predict_proba(p1_test)[:,1]
    P2 = model_p2.predict_proba(p2_test)[:,1]
    P_f = (P1_WEIGHT * P1) + (P2_WEIGHT * P2)
    if P_f >= FINAL_THRESHOLD:
        prediction = 1
    else:
        prediction = 0

    return P_f, prediction

