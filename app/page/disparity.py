import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR.parent / "assets"

def load_asset(filename):
    with open(ASSETS_DIR / filename, "r", encoding="utf-8") as file:
        return file.read()

def show_disparity(results):
    st.markdown(f"<style>{load_asset('disparity.css')}</style>", unsafe_allow_html=True)
    html = load_asset("disparity.html")
    total_candidates = results["male_total"] + results["female_total"]
    total_males = results["male_total"]
    total_females = results["female_total"]
    male_selected = results["male_selected"]
    female_selected = results["female_selected"]
    male_candidate_ratio = (total_males / total_candidates if total_candidates > 0 else 0)
    female_candidate_ratio = (total_females / total_candidates if total_candidates > 0 else 0)

    male_selected_ratio = (male_selected / total_candidates if total_candidates > 0 else 0)
    female_selected_ratio = (female_selected / total_candidates if total_candidates > 0 else 0)

    disparity_ratio = results["disparity_ratio"]
    no_bias = disparity_ratio is not None and disparity_ratio >= 0.80

    if no_bias:
        result_class = "result-safe"
        result_icon = "✓"
        result_title = "No Bias Detected"
        result_text = "The observed female-to-male selection-rate ratio is within the 80% threshold."
    else:
        result_class = "result-warning"
        result_icon = "!"
        result_title = "Potential Disparity Detected"
        result_text = "The observed selection-rate ratio falls below the 80% threshold."

    html = (
        html.replace("{TOTAL_CANDIDATES}", str(total_candidates))
        .replace("{TOTAL_MALES}", str(total_males))
        .replace("{TOTAL_FEMALES}", str(total_females))
        .replace("{RESULT_CLASS}", result_class)
        .replace("{RESULT_ICON}", result_icon)
        .replace("{RESULT_TITLE}", result_title)
        .replace("{RESULT_TEXT}", result_text)
    )

    st.html(html)

    st.markdown("### Selection Overview")

    female_col, male_col = st.columns(2)

    with female_col:
        st.markdown('<div class="metric-heading">Female Candidates</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="progress-label"><span>Total Female Candidates</span><span>{total_females} / {total_candidates}</span></div>',unsafe_allow_html=True)
        st.progress(female_candidate_ratio)

        st.markdown(f'<div class="progress-label"><span>Selected Females</span><span>{female_selected} / {total_candidates}</span></div>', unsafe_allow_html=True)
        st.progress(female_selected_ratio)

        st.markdown(f'<div class="rate-display">Female Selection Rate <strong>{results["female_selection_rate"] * 100:.1f}%</strong></div>', unsafe_allow_html=True)

    with male_col:
        st.markdown('<div class="metric-heading">Male Candidates</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="progress-label"><span>Total Male Candidates</span><span>{total_males} / {total_candidates}</span></div>', unsafe_allow_html=True)
        st.progress(male_candidate_ratio)

        st.markdown(f'<div class="progress-label"><span>Selected Males</span><span>{male_selected} / {total_candidates}</span></div>', unsafe_allow_html=True)
        st.progress(male_selected_ratio)

        st.markdown(f'<div class="rate-display">Male Selection Rate <strong>{results["male_selection_rate"] * 100:.1f}%</strong></div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="disparity-result {result_class}">
            <div class="result-icon">{result_icon}</div>
            <div class="result-content">
                <div class="result-title">{result_title}</div>
                <div class="result-text">{result_text}</div>
                <div class="result-ratio">
                    Disparity Ratio:
                    <strong>{f"{disparity_ratio:.2f}" if disparity_ratio is not None else "N/A"}</strong>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("← Back to Screening", key="back_to_screening"):
        st.session_state.page = "screening"
        st.rerun()