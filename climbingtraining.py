import streamlit as st
import sqlite3
import pandas as pd

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

# Title
st.title("🏋️‍♂️ Training Log with SQLite")

# Fetch data from database
df = pd.read_sql("SELECT * FROM workouts", conn)

# Filter options
st.write("### View Past Workouts")

# Search by exercise name
search_term = st.text_input("🔍 Search Exercise", "").strip().lower()
filtered_df = df.copy()  # Prevent modifying the original dataframe

if search_term:
    filtered_df = filtered_df[filtered_df["exercise"].str.lower().str.contains(search_term, na=False)]

# Sorting options
sort_by = st.selectbox("Sort by", ["Newest First", "Oldest First"])
if sort_by == "Newest First":
    filtered_df = filtered_df.sort_values(by="id", ascending=False)
else:
    filtered_df = filtered_df.sort_values(by="id", ascending=True)

# Display filtered data with a **different key**
st.data_editor(filtered_df.drop(columns=["id"]), key="filtered_training_table", hide_index=True)

# Option to clear all logs
if st.button("Clear Log"):
    cursor.execute("DELETE FROM workouts")
    conn.commit()
    st.warning("Training log cleared!")
