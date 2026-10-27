# ARS AI --- Autonomous Resume Screening AI

**AI-powered resume screening with semantic matching and fairness
assessment**

ARS AI is a local Streamlit application built to support the **initial
resume-screening stage**. It analyzes resume information against job
requirements, combines structured and semantic screening signals, and
provides a basic fairness assessment of selection outcomes.

> **Important:** ARS AI is an experimental decision-support project, not
> an automated hiring decision-maker. Its scores are not probabilities
> of being hired, and its fairness check does not prove that a process
> is unbiased. Results require human review and further validation
> before any real-world employment use.

## Features

-   **Resume processing:** Extracts text from uploaded PDF resumes.
-   **Structured screening:** Uses a Random Forest model to assess
    structured candidate features.
-   **Semantic matching:** Uses `sentence-transformers/all-MiniLM-L6-v2`
    embeddings and a Logistic Regression model to compare resume and
    job-description information.
-   **Hybrid screening score:** Combines the structured and semantic
    model outputs into a single screening score.
-   **Information extraction:** Uses `google/flan-t5-base` to help
    extract relevant information from resume text.
-   **Fairness assessment:** Compares selection rates across gender
    groups and flags potential disparities using a selection-rate ratio.
-   **Local execution:** Designed to run locally through Streamlit with
    locally available model artifacts.

## How it works

1.  A user supplies a resume and job-related information.
2.  The application extracts text and prepares the information needed by
    the screening pipelines.
3.  The structured model produces a screening score from structured
    features.
4.  The semantic pipeline represents resume and job-description
    information using MiniLM embeddings and produces a semantic
    screening score.
5.  The application combines the component scores into a hybrid
    screening score and assigns a screening category.
6.  The fairness component can compare selection rates between gender
    groups and flag potential disparities for review.

The screening output is intended to support further human review. It
should not be interpreted as a final hiring recommendation.

## Technology stack

-   Python
-   Streamlit
-   scikit-learn
-   Sentence Transformers
-   Hugging Face Transformers
-   `all-MiniLM-L6-v2`
-   `google/flan-t5-base`
-   PDF text extraction and local model artifacts

## Project structure

The repository may include additional files depending on the version
being published. The main application is organized around these
components:

``` text
ARS-AI/
├── app/       # Streamlit user interface
├── src/       # Resume processing, feature extraction and prediction logic
├── models/    # Saved model and preprocessing artifacts, where distributed
├── data/      # Sample/test data, if included
├── README.md
└── requirements.txt
```

Typical source modules include:

-   `extract_resume.py` --- extracts text from PDF resumes.
-   `extract_features.py` --- prepares structured features for
    screening.
-   `semantic_extract.py` --- prepares information for the semantic
    pipeline.
-   `predict.py` --- runs the structured, semantic and hybrid
    predictions.
-   `reusables.py` --- shared utilities and model-loading functions.

Names and locations may vary slightly between project versions.

## Running locally

The commands below assume that Python is installed and that the
repository contains a `requirements.txt` file. Run commands from the
project root.

1.  Clone or download this repository.

2.  Create and activate a virtual environment:

    **Windows (PowerShell):**

    ``` powershell
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```

3.  Install the project dependencies:

    ``` powershell
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

4.  Confirm that the required model files and saved model artifacts are
    available at the paths expected by the application.

5.  Start the application:

    ``` powershell
    streamlit run app/main.py
    ```

6.  Open the local URL printed by Streamlit in your browser.

### Model files and offline use

The application relies on local model files and saved artifacts. **Do
not assume that cloning the source repository automatically downloads or
includes these files.** If model weights are not distributed with the
repository, they must be obtained separately and placed at the paths
expected by the code before running the app. The first setup may require
internet access unless all required model files are already available
locally.

For a fully offline run, ensure that every required model snapshot,
tokenizer, configuration file, trained model, and preprocessing artifact
is present locally. Verify this in a clean environment before describing
a release as fully offline.

## Dataset and model notes

The structured screening component was developed using the Bertrand and
Mullainathan resume/callback dataset (4,870 observations). The target
label is `call`. The dataset is imbalanced, so accuracy alone is not
sufficient to judge model performance.

The semantic component was developed using a separate synthetic
resume--job-description dataset. Its results should therefore be
interpreted cautiously: the two components were not trained jointly on
one common dataset, and the hybrid score is an engineering combination
rather than a jointly trained or independently calibrated probability.

Protected/audit attributes are not intended to be predictive features.
The final implementation's fairness assessment focuses on gender-group
selection rates; it does **not** provide a complete audit of all
protected attributes or forms of discrimination.

## Fairness and responsible use

The fairness component compares group selection rates and uses a
selection-rate ratio to flag possible disparity. A ratio threshold is a
screening heuristic, not proof of fairness or discrimination.

Before any employment-related deployment, the system would need, at
minimum:

-   Evaluation on representative, job-relevant and appropriately
    licensed data.
-   Independent validation of the structured, semantic and hybrid
    screening approaches.
-   Calibration and error analysis across relevant groups.
-   Broader fairness and impact assessments.
-   Privacy, security, retention and access-control safeguards for
    resumes and candidate data.
-   Human oversight, explainable review criteria and a way to challenge
    or correct inaccurate extracted information.
-   Legal and compliance review appropriate to the deployment location.

Do not use this project as the sole basis for rejecting, ranking or
hiring a person.

## Privacy

Resumes can contain personal and sensitive information. Use only data
you are authorized to process. Avoid committing real resumes, candidate
records, API keys, secrets, local configuration files or private
datasets to GitHub. Review the repository contents before every push.

## Current status

ARS AI was developed as an internship project and local proof of
concept. Its purpose is to demonstrate a modular screening workflow,
semantic matching and an initial fairness assessment. It has not been
established as a validated production hiring system.

## Future improvements

-   Evaluate on larger, representative and job-specific datasets.
-   Improve semantic screening with stronger validation and
    domain-specific data.
-   Add broader fairness metrics and group-wise error analysis.
-   Improve explanations for screening outcomes and extracted fields.
-   Add automated tests, model monitoring and more robust
    data-protection controls.
-   Package the application for convenient Windows installation.

## License

No license is specified yet. Unless a license is added, the repository's
contents are not automatically granted an open-source license. Before
publishing, check the licensing terms of the dataset, pretrained models,
dependencies and any bundled assets. Add a project license only after
deciding how the code may be reused.
