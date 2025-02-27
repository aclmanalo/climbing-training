import streamlit as st
import sqlite3
import pandas as pd

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect("training_log.db", check_same_thread=False)
cursor = conn.cursor()

# Create a table if it doesn’t exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercise TEXT,
        reps INTEGER,
        sets INTEGER,
        rpe INTEGER
    )
''')
conn.commit()

# Title
st.title("🏋️‍♂️ Training Log with SQLite")

# User input for a new workout entry
st.write("### Add New Workout Entry")
col1, col2, col3, col4 = st.columns(4)

with col1:
    exercise = st.text_input("Exercise")

with col2:
    reps = st.number_input("Reps", min_value=1, step=1)

with col3:
    sets = st.number_input("Sets", min_value=1, step=1)

with col4:
    rpe = st.number_input("RPE", min_value=1, max_value=10, step=1)

# Add entry button
if st.button("Add Entry"):
    if exercise:
        cursor.execute("INSERT INTO workouts (exercise, reps, sets, rpe) VALUES (?, ?, ?, ?)", 
                       (exercise, reps, sets, rpe))
        conn.commit()
        st.success("Workout entry added!")

# Display all workouts
st.write("### Training Log")
df = pd.read_sql("SELECT * FROM workouts", conn)
st.data_editor(df.drop(columns=["id"]), key="training_table", hide_index=True)

# Option to clear all logs
if st.button("Clear Log"):
    cursor.execute("DELETE FROM workouts")
    conn.commit()
    st.warning("Training log cleared!")

# Connect to SQLite database
conn = sqlite3.connect("training_log.db", check_same_thread=False)
cursor = conn.cursor()

# Title
st.title("🏋️‍♂️ Training Log with SQLite")

# Fetch data from database
df = pd.read_sql("SELECT * FROM workouts", conn)

# Filter options
st.write("### View Past Workouts")

# Search by exercise name
search_term = st.text_input("🔍 Search Exercise", "").strip().lower()
if search_term:
    df = df[df["exercise"].str.lower().str.contains(search_term, na=False)]

# Sorting options
sort_by = st.selectbox("Sort by", ["Newest First", "Oldest First"])
if sort_by == "Newest First":
    df = df.sort_values(by="id", ascending=False)
else:
    df = df.sort_values(by="id", ascending=True)

# Display filtered data
st.data_editor(df.drop(columns=["id"]), key="training_table", hide_index=True)

# Option to clear all logs
if st.button("Clear Log"):
    cursor.execute("DELETE FROM workouts")
    conn.commit()
    st.warning("Training log cleared!")
