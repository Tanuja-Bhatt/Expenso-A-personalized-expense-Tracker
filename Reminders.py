import streamlit as st
from datetime import date, datetime
import pandas as pd
import sqlite3
from streamlit_push_notifications import send_push

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to continue :)")
    st.stop()

st.header("🎗Reminders")

# --- Reminder input section ---
title = st.text_input("Reminder Title (e.g., Pay Electricity Bill)")
amount = st.number_input("Amount", min_value=0.0)
due_date = st.date_input("Due Date", min_value=date.today())
rem_type = st.selectbox("Type", ["Bill", "Budget"])

# --- Save Reminder ---
if st.button("Save Reminder"):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("INSERT INTO reminders (title, amount, due_date, type) VALUES (?, ?, ?, ?)",
              (title, amount, str(due_date), rem_type))
    conn.commit()
    conn.close()
    st.success("Reminder saved successfully!")


# --- Display today's due reminders ---
def show_due_reminders():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    today = str(date.today())
    c.execute("SELECT title, amount FROM reminders WHERE due_date = ?", (today,))
    due_today = c.fetchall()
    conn.close()
    if due_today:
        for task in due_today:
            st.warning(f"Reminder: {task[0]} is due today! Amount: ₹{task[1]}")
            # send_push(title="Upcoming Bill Alert", body=f"{task[0]} of ₹{task[1]} is due today!", icon_path="icons/alert.png")

show_due_reminders()

# --- Get all reminders as DataFrame ---
def get_all_reminders():
    conn = sqlite3.connect('expenses.db')
    df = pd.read_sql("SELECT * FROM reminders", conn)
    conn.close()
    return df

# --- Delete reminder section ---
reminders_df = get_all_reminders()
if not reminders_df.empty:
    st.subheader("Delete a Reminder")
    reminders_df['display'] = reminders_df['id'].astype(str) + ": " + reminders_df['title']
    selected = st.selectbox("Select a Reminder to Delete", reminders_df['display'].tolist())
    if st.button("Delete Reminder"):
        reminder_id = int(selected.split(":")[0])
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute("DELETE FROM reminders WHERE id=?", (reminder_id,))
        conn.commit()
        conn.close()
        st.success("Reminder deleted successfully! Please refresh to update the list.")
else:
    st.info("No reminders set yet.")
