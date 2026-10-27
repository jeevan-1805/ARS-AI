import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR.parent / "assets"

def load_asset(filename):
    with open(ASSETS_DIR / filename, "r", encoding="utf-8") as file:
        return file.read()

def calculate_disparity(predictions, genders):
    male_selected = 0
    male_total = 0
    female_selected = 0
    female_total = 0

    for prediction, gender in zip(predictions, genders):
        if gender == "Male":
            male_total += 1
            if prediction == 1:
                male_selected += 1
        elif gender == "Female":
            female_total += 1
            if prediction == 1:
                female_selected += 1

    male_selection_rate = (male_selected / male_total if male_total > 0 else 0)
    female_selection_rate = (female_selected / female_total if female_total > 0 else 0)

    if male_selection_rate == 0:
        disparity_ratio = None
    else:
        disparity_ratio = female_selection_rate / male_selection_rate

    return {
        "male_total": male_total,
        "female_total": female_total,
        "male_selected": male_selected,
        "female_selected": female_selected,
        "male_selection_rate": male_selection_rate,
        "female_selection_rate": female_selection_rate,
        "disparity_ratio": disparity_ratio
    }


def get_prediction_status(probability):
    if probability >= 0.46:
        return "pass"
    elif probability >= 0.42:
        return "Potential"
    return "Fail"


def get_status_display(pred_label):
    if pred_label == "pass":
        return {
            "text": "Screening Passed",
            "class_name": "passed",
            "dot_class": "status-passed",
            "progress_class": "progress-passed"
        }

    if pred_label == "Potential":
        return {
            "text": "Potential",
            "class_name": "potential",
            "dot_class": "status-potential",
            "progress_class": "progress-potential"
        }

    return {
        "text": "Screening Failed",
        "class_name": "failed",
        "dot_class": "status-failed",
        "progress_class": "progress-failed"
    }


def screening_result(results):
    results = sorted(results, key=lambda x: x["probability"], reverse=True)

    pred_val = []
    file_names = []

    passed_count = 0
    potential_count = 0
    failed_count = 0

    job_title = st.session_state.get("job_title", "Resume Screening")
    total_candidates = len(results)

    screening_html = load_asset("screening.html")
    screening_css = load_asset("screening.css")

    st.markdown(f"<style>{screening_css}</style>", unsafe_allow_html=True)

    for result in results:
        probability = float(result["probability"][0])
        pred_label = get_prediction_status(probability)

        if pred_label == "pass":
            passed_count += 1
        elif pred_label == "Potential":
            potential_count += 1
        else:
            failed_count += 1

    screening_html = (
        screening_html.replace("{JOB_TITLE}", str(job_title))
        .replace("{TOTAL_CANDIDATES}", str(total_candidates))
        .replace("{PASSED_COUNT}", str(passed_count))
        .replace("{POTENTIAL_COUNT}", str(potential_count))
        .replace("{FAILED_COUNT}", str(failed_count))
    )

    st.html(screening_html)

    for rank, result in enumerate(results, start=1):
        probability = float(result["probability"][0])
        pred_label = get_prediction_status(probability)
        filename = result["resume"]

        file_names.append(filename)
        pred_val.append(1 if pred_label == "pass" else 0)

        st.session_state.candidate_details[filename]["rank"] = rank

        status = get_status_display(pred_label)
        percentage = probability * 100

        card_html = f"""
        <div class="candidate-card candidate-{status["class_name"]}">
            <div class="candidate-top-row">
                <div class="candidate-name">{filename}</div>

                <div class="candidate-status {status["dot_class"]}">
                    <span class="status-dot"></span>
                    <span>{status["text"]}</span>
                </div>
            </div>

            <div class="match-row">
                <div class="match-label">Final Match</div>
                <div class="match-percentage">{percentage:.1f}%</div>
            </div>

            <div class="progress-track">
                <div class="progress-fill {status["progress_class"]}" style="width: {percentage:.1f}%"></div>
            </div>
        </div>
        """

        st.html(card_html)

        st.markdown('<div class="candidate-action">', unsafe_allow_html=True)

        if st.button("View Candidate →", key=f"candidate_{filename}", use_container_width=True):
            st.session_state.selected_candidate = filename
            st.session_state.page = "candidate"
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    st.html(
        """
        <div class="fairness-section">
            <div class="fairness-title">
                Gender Fairness Check
            </div>

            <div class="fairness-subtitle">
                Enter gender details of candidates to detect disparity.
            </div>
        </div>
        """
    )

    genders = []

    for file in file_names:
        genders.append(st.radio(f"{file}:",["Male", "Female"],key=f"gender_{file}"))

    disparity = st.button(f"Calculate Disparity for the group of {len(genders)} Candidates", key="calculate_disparity", type="primary")

    if disparity:
        disparity_results = calculate_disparity(pred_val, genders)
        st.session_state.disparity_results = disparity_results
        st.session_state.page = "disparity"
        st.rerun()