import streamlit as st

FEATURE_LABELS = {
    "education": "Education Level",
    "ofjobs": "Number of Jobs",
    "yearsexp": "Years of Experience",
    "honors": "Honors",
    "volunteer": "Volunteer Experience",
    "military": "Military Experience",
    "empholes": "Employment Gaps",
    "workinschool": "Worked While Studying",
    "email": "Email Provided",
    "computerskills": "Computer Skills",
    "specialskills": "Special Skills"
}

EDUCATION_LABELS = {
    0: "No formal education",
    1: "High school",
    2: "Some college",
    3: "College education",
    4: "College degree or higher"
}


def requirement_satisfaction(candidate_features, requirements):
    satisfied = []
    not_satisfied = []

    required_education = int(requirements["schoolreq"])
    candidate_education = int(float(candidate_features["education"]))

    education_met = candidate_education >= required_education
    education_text = (f"Education requirement: {EDUCATION_LABELS.get(required_education, required_education)}")

    if education_met:
        satisfied.append(education_text)
    else:
        not_satisfied.append(education_text)

    # Experience requirement
    if requirements["expreq"] == 1:

        required_years = float(requirements["required_experience_years"])
        candidate_years = float(candidate_features["yearsexp"])

        experience_type = requirements["experience_requirement_type"]

        if experience_type == "some":
            experience_met = candidate_years > 0
            experience_text = "Some previous experience required"

        else:
            experience_met = candidate_years >= required_years
            experience_text = (f"Minimum {required_years:g} years of experience required")

        if experience_met:
            satisfied.append(experience_text)
        else:
            not_satisfied.append(experience_text)


    if int(requirements["supervisor"]) == 1:
        not_satisfied.append("Supervisory responsibilities cannot be verified from extracted resume features")

    if int(requirements["secretary"]) == 1:
        not_satisfied.append("Secretarial duties cannot be verified from extracted resume features")

    if int(requirements["offsupport"]) == 1:
        not_satisfied.append("Office / administrative support cannot be directly verified from extracted resume features")

    if int(requirements["salesrep"]) == 1:
        not_satisfied.append("Sales representative experience cannot be directly verified from extracted resume features")

    if int(requirements["retailsales"]) == 1:
        not_satisfied.append("Retail sales experience cannot be directly verified from extracted resume features")

    if int(requirements["comreq"]) == 1:
        if int(candidate_features["specialskills"]) == 1:
            satisfied.append("Communication skills")
        else:
            not_satisfied.append("Communication skills")

    if int(requirements["educreq"]) == 1:
        if candidate_education >= 1:
            satisfied.append("Required education / qualification")
        else:
            not_satisfied.append("Required education / qualification")

    if int(requirements["compreq"]) == 1:
        if int(candidate_features["computerskills"]) == 1:
            satisfied.append("Computer / technical skills")
        else:
            not_satisfied.append("Computer / technical skills")

    if int(requirements["orgreq"])== 1:
        if int(candidate_features["specialskills"]) == 1:
            satisfied.append("Organizational skills")
        else:
            not_satisfied.append("Organizational skills")

    return satisfied, not_satisfied


def format_candidate_feature(feature_name, value):

    label = FEATURE_LABELS.get(feature_name, feature_name)

    if feature_name == "education":
        value = EDUCATION_LABELS.get(value, value)

    elif feature_name in {
        "honors",
        "volunteer",
        "military",
        "empholes",
        "workinschool",
        "email",
        "computerskills",
        "specialskills"
    }:
        value = "Yes" if value == 1 else "No"
    return label, value

def show_candidate():

    if "selected_candidate" not in st.session_state:
        st.warning("No candidate selected.")
        return

    filename = st.session_state.selected_candidate
    candidate_details = st.session_state.candidate_details


    if filename not in candidate_details:
        st.error("Candidate details could not be found.")
        return

    candidate = candidate_details[filename]

    probability = candidate["probability"]
    candidate_features = candidate["candidate_features"]
    requirements = candidate["requirements"]
    jd_similarity = candidate["jd_similarity"]
    rank = candidate.get("rank", "-")

    if st.button("← Back to Screening"):
        st.session_state.page = "screening"
        st.rerun()

    st.title("Candidate Analysis")
    st.header(filename)
    st.subheader("Screening Summary")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rank", rank)

    with col2:
        st.metric("Screening Probability", f"{probability:.1%}")

    with col3:
        st.metric("JD Similarity", f"{jd_similarity:.1%}")

    if probability >= 0.46:
        status = "Screening Passed"
    elif probability >= 0.42:
        status = "Potential Candidate"
    else:
        status = "Screening Failed"

    st.write(f"**Status:** {status}")
    st.progress(float(probability))
    st.subheader("Requirements")
    satisfied, not_satisfied = requirement_satisfaction(candidate_features, requirements)

    if satisfied:
        st.write("### ✓ Requirements Satisfied")

        for requirement in satisfied:
            st.success(requirement)

    if not_satisfied:
        st.write("### Requirements Not Satisfied / Not Verifiable")

        for requirement in not_satisfied:
            st.warning(requirement)

    st.subheader("Candidate Details")

    for feature_name, value in candidate_features.items():
        label, formatted_value = format_candidate_feature(feature_name, value)
        st.write(f"**{label}:** {formatted_value}")

    st.subheader("Resume")
    resume_bytes = candidate["resume"]
    st.download_button(label="View Resume", data=resume_bytes, file_name=filename, mime="application/pdf")