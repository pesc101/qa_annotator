import glob
import os
import ast
import math
import pandas as pd
import streamlit as st

# Wide layout for better visibility
st.set_page_config(layout='wide')
st.title('Question-Answer Annotation Tool')

# Dataset selection from CSV files in data/ folder
dataset_files = glob.glob('data/*.csv')
dataset_files = [os.path.basename(f) for f in dataset_files]
dataset_file = st.selectbox('Select CSV Dataset', dataset_files)

# Annotator info
annotator_name = st.text_input('Annotator Name:')
partition = st.selectbox('Your Partition (1-4)', ['1', '2', '3', '4'])

if dataset_file and annotator_name and partition:
    # Load the dataset
    df = pd.read_csv(os.path.join('data', dataset_file))
    total = len(df)
    part = int(partition) - 1
    per_partition = math.ceil(total / 4)

    # Determine progress by reading existing annotations
    os.makedirs('results', exist_ok=True)
    out_file = os.path.join('results', f'annotations_{annotator_name}_{dataset_file}')
    if os.path.exists(out_file):
        res_df = pd.read_csv(out_file)
        done = len(res_df)
    else:
        done = 0

    # Calculate current index for this partition
    idx = part + done * 4

    # Display progress
    st.progress(done / per_partition)
    st.caption(f'Annotated {done} of {per_partition} samples (partition {partition})')

    # Check completion
    if done >= per_partition or idx >= total:
        st.success('Annotation complete for your partition!')
        st.stop()

    # Fetch current row
    row = df.iloc[idx]
    col1, col2 = st.columns([2, 3])

    # Left: QA display and annotation
    with col1:
        st.subheader('Question')
        st.write(row['question'])
        st.subheader('Answer')
        st.write(row['answer'])
        st.subheader('Final Formula')
        st.code(row['final_formula'])
        with st.expander('Question Reasoning'):
            st.write(row['question_reasoning'])
        with st.expander('Answer Reasoning'):
            st.write(row['answer_reasoning'])

        # Unique session keys to prevent double-writing
        q_key = f"q_invalid_{idx}"
        a_key = f"a_invalid_{idx}"
        written_key = f"written_{idx}"
        st.session_state.setdefault(q_key, False)
        st.session_state.setdefault(a_key, False)
        st.session_state.setdefault(written_key, False)

        # Annotation inputs
        q_invalid = st.checkbox('Question does not make sense', key=q_key)
        a_invalid = st.checkbox('Answer does not make sense or invalid', key=a_key)

        # On-click saves annotation
        def submit_annotation():
            if not st.session_state[written_key]:
                result = pd.DataFrame([{ 
                    'id': row.get('id', idx),
                    'question': row['question'],
                    'q_invalid': st.session_state[q_key],
                    'a_invalid': st.session_state[a_key],
                    'annotator': annotator_name
                }])
                # Append or create
                if os.path.exists(out_file):
                    result.to_csv(out_file, index=False, header=False, mode='a')
                else:
                    result.to_csv(out_file, index=False)
                st.session_state[written_key] = True

        st.button('Submit', key=f'submit_{idx}', on_click=submit_annotation)

    # Right: render the raw table
    with col2:
        st.subheader('Table')
        try:
            outer = ast.literal_eval(row['table'])
            inner = ast.literal_eval(outer.get('raw', outer))
            if isinstance(inner, dict) and all(isinstance(v, dict) for v in inner.values()):
                df_tbl = pd.DataFrame(inner)
            else:
                df_tbl = pd.DataFrame(list(inner.items()), columns=['Field', 'Value'])
            # Cast to string to avoid serialization issues
            df_tbl = df_tbl.astype(str)
            st.table(df_tbl)
        except Exception as e:
            st.error(f'Failed to parse table: {e}')
