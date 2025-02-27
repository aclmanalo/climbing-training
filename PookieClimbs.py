import streamlit as st
import sqlite3
import pandas as pd
from datetime import date


# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect("new_training_log.db")
cursor = conn.cursor()


# Create a table if it doesn’t exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercise TEXT,
        reps INTEGER,
        sets INTEGER,
        rpe INTEGER,
        date TEXT
    )
''')
conn.commit()

# Title
st.title("Input Exercise")

# User input for a new workout entry
st.write("### Add New Workout Entry")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    exercise = st.text_input("Exercise")

with col2:
    reps = st.number_input("Reps", min_value=1, step=1)

with col3:
    sets = st.number_input("Sets", min_value=1, step=1)

with col4:
    rpe = st.number_input("RPE", min_value=1, max_value=10, step=1)

with col5:
    workout_date = st.date_input("Date", date.today())  # Default to today's date

# Add entry button
if st.button("Add Entry"):
    if exercise:
        cursor.execute("INSERT INTO workouts (exercise, reps, sets, rpe, date) VALUES (?, ?, ?, ?, ?)", 
                       (workout_date, exercise, reps, sets, rpe))
        conn.commit()
        st.success(f"Workout entry added for {workout_date}!")




# Add space
st.markdown("<br><br>", unsafe_allow_html=True)  # Adds two line breaks



