import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# Connect to SQLite database
conn = sqlite3.connect("training_log.db", check_same_thread=False)
cursor = conn.cursor()

# Create table with a date column if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        exercise TEXT,
        reps INTEGER,
        sets INTEGER,
        rpe INTEGER
    )
''')
conn.commit()

# Title
st.title("🏋️‍♂️ Training Log with Dates")

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
        cursor.execute("INSERT INTO workouts (date, exercise, reps, sets, rpe) VALUES (?, ?, ?, ?, ?)", 
                       (workout_date, exercise, reps, sets, rpe))
        conn.commit()
        st.success(f"Workout entry added for {workout_date}!")

# Fetch data from database
df = pd.read_sql("SELECT * FROM workouts", conn)

# Filter options
st.write("### View Past Workouts")

# Search by exercise name
search_term = st.text_input("🔍 Search Exercise", "").strip().lower()
filtered_df = df.copy()

if search_term:
    filtered_df = filtered_df[filtered_df["exercise"].str.lower().str.contains(search_term, na=False)]

# Sort by date (Newest First by default)
filtered_df["date"] = pd.to_datetime(filtered_df["date"])
filtered_df = filtered_df.sort_values(by="date", ascending=False)

# Display the updated log
st.data_editor(filtered_df.drop(columns=["id"]), key="training_table", hide_index=True)

# Option to clear all logs
if st.button("Clear Log"):
    cursor.execute("DELETE FROM workouts")
    conn.commit()
    st.warning("Training log cleared!")

