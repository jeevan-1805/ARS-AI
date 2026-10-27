import streamlit as st

def show_landing():
    st.title("ARS AI - Autonomous Resume Screening AI")
    st.write("Screen candidates using structured and semantic AI analysis.")
    st.header("Create Screening Session")
    job_title = st.text_input("Job Title", placeholder="eg. Machine Learning Engineer")

    st.subheader("Job Description")
    job_description = st.text_area("Job Description", placeholder="Place your job descriptin here...", height=250, label_visibility="collapsed")
    st.header("Screening Requirements")
    st.subheader("Specify your general requirements for a candidate")
    col1, col2 = st.columns(2)
    with col1:
        job_type = st.selectbox("Job Type", ['Administrative / Clerical', 'Sales'])
        st.subheader("Role Characteristics")
        manager = st.checkbox("Managerial Responsibilities")
        supervisor = st.checkbox("Supervisory responsibilities")
        secretary = st.checkbox("Secretarial duties")
        offsupport = st.checkbox("Office / administrative support")
        salesrep = st.checkbox("Sales representative duties")
        retailsales = st.checkbox("Retail Sales duties")
    with col2:
        schoolreq = st.selectbox("Minimum Education Requirement", ["No formal education requirement", "High school diploma", "Some college", "College degree or higher"])
        expreq = st.selectbox("Experience Requirement", [ "No experience required", "Experience required"])

        if expreq == "Experience required":
            experience_type = st.radio("Minimum Experience Requirement", ["Some experience required", "Specific years of experience required"])
            if experience_type == "Specific years of experience required":
                experience_years = st.number_input("Required Experience (years)", min_value=0.0, step=0.5)
            else:
                experience_years = 0
        else:
            experience_type = 0
            experience_years = 0

        st.subheader("Required Skills")

        comreq = st.checkbox("Strong communication skills required")
        educreq = st.checkbox("Specific education or qualification required")
        compreq = st.checkbox("Computer or technical skills required")
        orgreq = st.checkbox("Organizational skills required")

        requirements = [job_type, manager, supervisor, secretary, offsupport, salesrep, retailsales, schoolreq, expreq, experience_type, experience_years, comreq, educreq, compreq, orgreq]

    uploaded_resumes = st.file_uploader("Upload Resumes", type=['pdf'], accept_multiple_files=True)
    analyze = st.button("Anlanyse Candidates")

    return (job_title, job_description, requirements, uploaded_resumes, analyze)
