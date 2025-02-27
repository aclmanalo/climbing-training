import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# Connect to SQLite database (creates file if it doesn't exist)
DB_NAME = "climbing_training.db"
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor = conn.cursor()

# Ensure table exists with a "date" column
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
st.title("🏋️‍♂️ Climbing Training Log")

# User input for new workout entry
st.write("### Add a New Workout Entry")
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
    workout_date = st.date_input("Date", date.today())  # Defaults to today

# Button to add entry
if st.button("Add Entry"):
    if exercise:  # Ensure exercise is not empty
        cursor.execute(
            "INSERT INTO workouts (date, exercise, reps, sets, rpe) VALUES (?, ?, ?, ?, ?)", 
            (workout_date.strftime("%Y-%m-%d"), exercise, reps, sets, rpe)
        )
        conn.commit()
        st.success(f"Workout entry for {workout_date} added!")

# Fetch and display past workout logs
df = pd.read_sql("SELECT * FROM workouts", conn)

# Convert date column to proper format
df["date"] = pd.to_datetime(df["date"])

# --- Search and Filter Section ---
st.write("### Search Workouts")

# Search input for exercise name
search_query = st.text_input("Search by Exercise Name", "")

# Date range filter
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", df["date"].min().date() if not df.empty else date.today())
with col2:
    end_date = st.date_input("End Date", df["date"].max().date() if not df.empty else date.today())

# Apply filters
if not df.empty:
    # Filter by exercise name (case insensitive)
    if search_query:
        df = df[df["exercise"].str.contains(search_query, case=False, na=False)]

    # Filter by date range
    df = df[(df["date"] >= pd.to_datetime(start_date)) & (df["date"] <= pd.to_datetime(end_date))]

# Display the filtered table
st.write("### Training Log")
st.data_editor(df.drop(columns=["id"]), key="training_table_history", hide_index=True)

# Option to clear all logs
if st.button("Clear Log"):
    cursor.execute("DELETE FROM workouts")
    conn.commit()
    st.warning("Training log cleared!")
