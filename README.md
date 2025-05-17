# QA Annotator

A tool for annotating question-answer datasets with context-dependence and ambiguity labels.

## Installation

1. **Install dependencies using [uv](https://github.com/astral-sh/uv):**
    ```bash
    uv venv --python 3.12
    source .venv/bin/activate
    uv sync
    ```

2. **Start the Streamlit app:**
    ```bash
    streamlit run main.py
    ```

## Usage

1. **Select a dataset** from the available options in the app.
2. **Enter the dataset name** when prompted.
3. For each question:
    - Decide if the question is **context-dependent**.
    - Decide if the question is **unambiguous**.

Follow the on-screen instructions to complete the annotation process.

## After the annotation
Just push the changes in the result folder to the repo.

## Annotation Progress

| Name    | Dataset    | Done |
|---------|------------|------|
| Jan     | FinQA      |   <p align="center">✅</p>   |
| Jan     | ConvFinQA  |  <p align="center">✅</p>    |
| Max     | VQA        |  <p align="center">✅</p>  |
| Max     | TATDQA     |  <p align="center">✅</p>   |
| Isabell | FinQA      |  <p align="center">✅</p>   |
| Isabell | ConvFinQA  |  <p align="center">✅</p>   |
| Kutay   | VQA        |      |
| Kutay   | TATDQA     |      |
