import streamlit as st
import pandas as pd

# Title
st.title("🏋️‍♂️ Training Log")

# Define initial data
if "training_log" not in st.session_state:
    st.session_state.training_log = pd.DataFrame({
        "Exercise": ["Squat", "Bench Press", "Deadlift", "Overhead Press"],
        "Reps": [5, 5, 5, 5],
        "Sets": [3, 3, 3, 3],
        "RPE": [7, 7, 7, 7]
    })

# Editable table
st.write("### Training Log")
edited_df = st.data_editor(st.session_state.training_log, key="training_table")

# Update session state
if st.button("Save Changes"):
    st.session_state.training_log = edited_df
    st.success("Training log updated!")
