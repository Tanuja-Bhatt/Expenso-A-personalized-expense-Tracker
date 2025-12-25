import streamlit as st
import pandas as pd
import sqlite3
from utils.expenseTracker import ExpenseManager, IncomeManager

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to continue :)")
    st.stop() 

st.title("📊 View Transactions")

db_name = "expenses.db"
ExManager = ExpenseManager(db_name=db_name)
InManager = IncomeManager(db_name=db_name)


tab1, tab2 = st.tabs(["💸 Expenses", "💰 Income"])

with tab1:
    st.subheader("Expense Transactions")
    expenses = ExManager.view_expenses()
    if not expenses.empty:
        st.dataframe(expenses)
    else:
        st.info("No expense records found.")

with tab2:
    st.subheader("Income Transactions")
    income = InManager.view_income()
    if not income.empty:
        st.dataframe(income)
    else:
        st.info("No income records found.")

