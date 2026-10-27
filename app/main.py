import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import time
from urllib.parse import quote, unquote


from app.page.landing import show_landing
from app.page.screening import screening_result
from app.page.disparity import show_disparity
from app.page.candidate_details import show_candidate

@st.cache_resource
def load_extract_resume_module():
    from src.extract_resume import extract_resume_text
    return extract_resume_text


@st.cache_resource
def load_extract_features_module():
    from src.extract_features import extract_candidate_feature_blocks
    return extract_candidate_feature_blocks


@st.cache_resource
def load_semantic_extract_module():
    from src.semantic_extract import extract_feature_value
    return extract_feature_value


@st.cache_resource
def load_predict_module():
    from src.predict import build_test, build_req, build_p2_X, predict_final

    return build_test, build_req, build_p2_X, predict_final



@st.cache_resource
def load_reusables_module():
    from src.reusables import load_sentence_transformer, load_nlp_model

    return load_sentence_transformer, load_nlp_model


BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"


def load_asset(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def render_loading_steps(steps, exclude=None):

    if exclude is None:
        exclude = []

    html = ""

    for index, step in enumerate(steps):

        if index in exclude:
            continue

        if step["status"] == "complete":
            icon = '<div class="check">✓</div>'
            class_name = "step-complete"

        elif step["status"] == "loading":
            icon = '<div class="spinner"></div>'
            class_name = ""

        else:
            icon = "○"
            class_name = ""

        html += f"""
        <div class="loading-step {class_name}">
            <div class="step-icon">
                {icon}
            </div>

            <div class="step-text">
                {step["label"]}
            </div>
        </div>
        """

    return html

def show_loading():

    loader_css = load_asset(ASSETS_DIR / "loading.css")

    loader_html = load_asset(ASSETS_DIR / "loading.html")

    st.markdown(f"<style>{loader_css}</style>", unsafe_allow_html=True)

    loading_area = st.empty()
    top_loading_area = st.empty()
    module_progress_area = st.empty()
    bottom_loading_area = st.empty()

    steps = [
        {
            "label": "Application components",
            "status": "complete"
        },
        {
            "label": "Module Imports",
            "status": "loading"
        },
        {
            "label": "Embedding model",
            "status": "pending"
        },
        {
            "label": "Natural language model",
            "status": "pending"
        },
        {
            "label": "Screening engine",
            "status": "pending"
        }
    ]

    loading_area.html(loader_html)

    top_loading_area.html(render_loading_steps(steps[:2]))
    module_progress_area.progress(0, text="Loading application modules...")
    bottom_loading_area.html(render_loading_steps(steps[2:]))

    extract_candidate_feature_blocks = load_extract_features_module()
    module_progress_area.progress(20, text="Loading application modules... 20%")

    extract_feature_value = load_semantic_extract_module()
    module_progress_area.progress(40, text="Loading application modules... 40%")

    
    extract_resume_text = load_extract_resume_module()
    module_progress_area.progress(60, text="Loading application modules... 60%")

    build_test, build_req, build_p2_X, predict_final = load_predict_module()
    module_progress_area.progress(80, text="Loading application modules... 80%")

    load_sentence_transformer, load_nlp_model = load_reusables_module()
    module_progress_area.progress(100,text="Application modules loaded")


    steps[1]["status"] = "complete"
    steps[2]["status"] = "loading"

    top_loading_area.html(render_loading_steps(steps[:2]))
    module_progress_area.empty()
    bottom_loading_area.html(render_loading_steps(steps[2:]))


    embedding_model = load_sentence_transformer()

    steps[2]["status"] = "complete"
    steps[3]["status"] = "loading"

    bottom_loading_area.html(render_loading_steps(steps[2:]))


    tokenizer, nlp_model = load_nlp_model()

    steps[3]["status"] = "complete"
    steps[4]["status"] = "loading"

    bottom_loading_area.html(render_loading_steps(steps[2:]))


    steps[4]["status"] = "complete"

    bottom_loading_area.html(render_loading_steps(steps[2:]))

    time.sleep(0.5)

    loading_area.empty()
    top_loading_area.empty()
    bottom_loading_area.empty()

    return (
        embedding_model,
        tokenizer,
        nlp_model,
        extract_resume_text,
        extract_candidate_feature_blocks,
        extract_feature_value,
        build_test,
        build_req,
        build_p2_X,
        predict_final
    )
def main():
    st.set_page_config(page_title="ARS AI", layout="wide")
    analyze = None
    embed_model, tokenizer, semantic_model, extract_resume_text, extract_candidate_feature_blocks, extract_feature_value, build_test, build_req, build_p2_X, predict_final = show_loading()



    if "page" not in st.session_state:
        inputs = (job_title, job_description, requirements, uploaded_resumes, analyze) = show_landing()
    elif st.session_state.page == "screening":
        screening_result(st.session_state.results)
    elif st.session_state.page == "disparity":
        show_disparity(st.session_state.disparity_results)
    elif st.session_state.page == "candidate":
        show_candidate()

    if analyze:
        if all(inputs):
            st.success("Input received successfully.")
        else:
            st.warning("Please provide all the information: One or more inputs are missing")
        st.session_state.job_title = job_title
        pred_results = []
        file_names = []
        st.session_state.candidate_details = {}
        progress_bars = {}

        for file in uploaded_resumes:
            progress_bars[file.name] = st.empty()
            progress_bars[file.name].progress(0, text=f"Preparing {file.name}...")
            
            block_text, block_embeds = extract_resume_text(file, embed_model)
            progress_bars[file.name].progress(1 / 6, text=f"{file.name}: Resume content extracted")

            retrieved_feats = extract_candidate_feature_blocks(block_text=block_text, block_embeddings=block_embeds, embedding_model=embed_model)
            progress_bars[file.name].progress(2 / 6, text=f"{file.name}: Candidate features retrieved")

            candidate_feats = extract_feature_value(retrieved_feats, tokenizer=tokenizer, semantic_model=semantic_model)
            progress_bars[file.name].progress(3 / 6, text=f"{file.name}: Candidate information extracted")

            requirements_df = build_req(*requirements)
            p1_test = build_test(candidate_feats, requirements_df)
            progress_bars[file.name].progress(4 / 6, text=f"{file.name}: Structured screening analysis complete")

            resume_text = "\n".join(block_text)
            p2_test = build_p2_X(resume_text, job_description, embed_model)
            progress_bars[file.name].progress(5 / 6, text=f"{file.name}: Semantic screening analysis complete")

            f_prob, f_pred = predict_final(p1_test, p2_test)
            pred_results.append({"resume": file.name, "probability": f_prob, "prediction": f_pred})
            file_names.append(file.name)
            st.session_state.candidate_details[file.name] = {
                "probability": float(f_prob[0]),
                "candidate_features": candidate_feats,
                "jd_similarity": p2_test.iloc[0]["similarity"],
                "requirements": requirements_df.iloc[0].to_dict(),
                "resume": file.getvalue()
            }
            progress_bars[file.name].progress(1.0, text=f"{file.name}: Screening complete")
        st.session_state.results = pred_results
        st.session_state.page = "screening"

        st.rerun()
    
if __name__ == "__main__":
    main()