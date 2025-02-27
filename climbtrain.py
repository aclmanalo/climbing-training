import streamlit as st
import pandas as pd

st.title("Climbing Training Log")
st.write("Tracking Climbing Training Progress")

# Title
st.title("🏋️‍♂️ One-Rep Max (1RM) Tracker")

# Define initial 1RM values
if "one_rep_max" not in st.session_state:
    st.session_state.one_rep_max = {
        "Squat": 100,
        "Bench Press": 80,
        "Deadlift": 120,
        "Overhead Press": 60
    }

# Convert to DataFrame
df = pd.DataFrame(list(st.session_state.one_rep_max.items()), columns=["Exercise", "1RM (kg)"])

# Editable table
st.write("### Your 1RM Table")
edited_df = st.data_editor(df, key="editable_table")

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
edited_df = st.data_editor(st.session_state.training_log, key="training_table", hide_index=True)

# Update session state
if st.button("Save Changes"):
    st.session_state.training_log = edited_df
    st.success("Training log updated!")
