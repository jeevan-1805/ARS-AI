from src.reusables import FEATURE_VALUE_CODES, binary_cols, cand_feats_names
import streamlit as st

def generate_answer(prompt, tokenizer, semantic_model, max_new_tokens=5):
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = semantic_model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer.strip()

def extract_feature_value(retrieved_features, tokenizer, semantic_model):
    candidate_features = {}
    for feature_name, retrieved_blocks in zip(cand_feats_names, retrieved_features.values()):
        context = "\n".join(item["block"] for item in retrieved_blocks)

        prompt = f"""
Extract the value of the following resume feature.

Feature:
{feature_name}

Rules:
{FEATURE_VALUE_CODES[feature_name]}

Resume context:
{context}

Return only the value.

"""
        value = generate_answer(prompt,tokenizer=tokenizer, semantic_model=semantic_model)
        if feature_name in binary_cols:
            value = value.strip()

            if value not in {"0", "1"}:
                st.error(f"Invalid value for feature '{feature_name}': {value}")
                raise ValueError(f"Invalid binary value for feature '{feature_name}'")

            value = int(value)
        candidate_features[feature_name] = value

    return candidate_features
