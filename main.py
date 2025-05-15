import glob
import os

import pandas as pd
import streamlit as st

# Wide layout
st.set_page_config(layout="wide")
st.title("Question Annotation Tool")

# Dataset selection
dataset_files = glob.glob("./data/*.xlsx")
dataset_files = [os.path.basename(f) for f in dataset_files]
dataset_file = st.selectbox("Select Dataset", dataset_files)

# Annotator name input
annotator_name = st.text_input("Enter your name:", key="annotator_name")

if dataset_file and annotator_name:
    df = pd.read_excel(f"data/{dataset_file}", engine="openpyxl")
    st.session_state.setdefault("index", 0)
    st.session_state.setdefault("orig_label", None)
    st.session_state.setdefault("gen_label", None)

    total_samples = len(df)
    current_index = st.session_state["index"]

    # Progress bar + count
    st.progress(current_index / total_samples)
    st.caption(f"Annotated: {current_index} / {total_samples}")

    if current_index >= total_samples:
        st.success("All annotations done!")
        st.stop()

    current_row = df.iloc[current_index]

    # Layout: Left = Questions + Buttons | Right = Context
    col_left, col_right = st.columns([2, 3])

    with col_left:
        with st.form(key="annotation_form"):
            st.subheader("Original Question")
            st.text_area("Question", current_row["question"], height=100, disabled=True)

            orig_label = st.radio(
                "Original Question Label",
                ["Context-free", "Unambiguous"],
                key="orig_label_radio",
            )

            st.subheader("Generated Question")
            st.text_area(
                "Generated",
                current_row["generated_question"],
                height=100,
                disabled=True,
            )

            gen_label = st.radio(
                "Generated Question Label",
                ["Context-free", "Unambiguous"],
                key="gen_label_radio",
            )

            submitted = st.form_submit_button("Submit Annotations")

            if submitted:
                result = pd.DataFrame(
                    [
                        {
                            "dataset": dataset_file,
                            "id": current_row["id"],
                            "type": "original",
                            "label": orig_label,
                            "annotator": annotator_name,
                        },
                        {
                            "dataset": dataset_file,
                            "id": current_row["id"],
                            "type": "generated",
                            "label": gen_label,
                            "annotator": annotator_name,
                        },
                    ]
                )
                out_file = f"results/annotations_{annotator_name}_{dataset_file}"

                if os.path.exists(out_file):
                    result.to_csv(out_file, mode="a", header=False, index=False)
                else:
                    result.to_csv(out_file, index=False)

                # Next sample
                st.session_state["index"] += 1

    with col_right:
        st.subheader("Context")
        st.markdown(current_row["context"])
