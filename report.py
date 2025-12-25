import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv
import cohere
from utils.expenseTracker import Account  
from utils.ETbot import get_budget_insights
import re


load_dotenv()
api_key = os.getenv('COHERE_API_KEY')
co = cohere.Client(api_key)

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in first.")
    st.stop()

user_email = st.session_state.user_email
db_name = f"{user_email}.db"
account = Account(db_name=db_name)

st.set_page_config(page_title="Report Analysis", layout="wide")

st.title("📊 Expense and Income Report Analysis")

# --- File uploader ---
uploaded_file = st.file_uploader("Upload your transactions CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Read CSV file
        df = pd.read_csv(uploaded_file)
        st.success("✅ CSV file uploaded successfully!")

        # Clean column names
        df.columns = df.columns.str.strip().str.lower()

        # Expected columns
        expected_cols = ["date", "description", "amount", "type", "category"]

        # Validate columns
        missing_cols = [col for col in expected_cols if col not in df.columns]
        if missing_cols:
            st.warning(f"⚠️ Missing columns in CSV: {', '.join(missing_cols)}")

        # Convert date column to datetime
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

        # Drop rows without valid amounts
        df = df.dropna(subset=["amount"])

        # Separate Income and Expense based on 'type' column
        if "type" in df.columns:
            income_df = df[df["type"].str.lower().isin(["credit", "income"])]
            expense_df = df[df["type"].str.lower().isin(["debit", "expense"])]
        else:
            income_df = pd.DataFrame()
            expense_df = pd.DataFrame()

        import re

        def format_in_indian_currency(amount):
    # """
    # Convert a number into Indian currency format (lakhs/crores)
    # Example: 12345678.9 -> ₹1,23,45,678.90
    # """
    # Handle negative values gracefully
          sign = '-' if amount < 0 else ''
          amount = abs(amount)

          s = f"{amount:.2f}"
          if '.' in s:
             before, after = s.split('.')
          else:
             before, after = s, "00"

    # Apply Indian numbering format
    # Split the last 3 digits and the rest
          if len(before) > 3:
            last_three = before[-3:]
            remaining = before[:-3]
        # Add commas after every 2 digits in the remaining part
            remaining = re.sub(r'(\d)(?=(\d{2})+$)', r'\1,', remaining)
            formatted = remaining + ',' + last_three
          else:
            formatted = before

          return f"{sign}₹{formatted}.{after}"



        # --- KPI Metrics ---
        total_income = income_df["amount"].sum() if not income_df.empty else 0
        total_expense = expense_df["amount"].sum() if not expense_df.empty else 0
        net_savings = total_income - total_expense

        st.markdown("### 💡 Key Insights")
        col1, col2, col3 = st.columns(3)
        # col1.metric("Total Income", f"₹{total_income:,.2f}")
        # col2.metric("Total Expense", f"₹{total_expense:,.2f}")
        # col3.metric("Net Savings", f"₹{net_savings:,.2f}")
        col1.metric("Total Income", format_in_indian_currency(total_income))
        col2.metric("Total Expense", format_in_indian_currency(total_expense))
        col3.metric("Net Savings", format_in_indian_currency(net_savings))


        st.divider()

        # --- EXPENSE ANALYSIS ---
        st.subheader("💸 Expense Analysis")
        if not expense_df.empty:
            group_col = "category" if "category" in expense_df.columns else "description"

            # Expense by category
            exp_by_cat = expense_df.groupby(group_col, as_index=False)["amount"].sum()
            exp_fig = px.pie(
                exp_by_cat,
                values="amount",
                names=group_col,
                title="🧾 Expense Breakdown by Category",
                hole=0.4
            )
            st.plotly_chart(exp_fig, use_container_width=True)

            # Expense over time
            exp_trend = expense_df.groupby("date", as_index=False)["amount"].sum()
            line_fig_exp = px.line(
                exp_trend,
                x="date",
                y="amount",
                title="📅 Expense Trend Over Time"
            )
            st.plotly_chart(line_fig_exp, use_container_width=True)
        else:
            st.info("No expense data found in CSV.")

        st.divider()

        # --- INCOME ANALYSIS ---
        st.subheader("💰 Income Analysis")
        if not income_df.empty:
            group_col = "category" if "category" in income_df.columns else "description"

            # Income by category
            inc_by_cat = income_df.groupby(group_col, as_index=False)["amount"].sum()
            inc_fig = px.pie(
                inc_by_cat,
                values="amount",
                names=group_col,
                title="💵 Income Breakdown by Category",
                hole=0.4
            )
            st.plotly_chart(inc_fig, use_container_width=True)

            # Income over time
            inc_trend = income_df.groupby("date", as_index=False)["amount"].sum()
            line_fig_inc = px.line(
                inc_trend,
                x="date",
                y="amount",
                title="📅 Income Trend Over Time"
            )
            st.plotly_chart(line_fig_inc, use_container_width=True)
        else:
            st.info("No income data found in CSV.")

        st.divider()

        # --- BALANCE TREND ---
        st.subheader("📈 Overall Balance Trend")

        if not df.empty and "date" in df.columns:
            df_sorted = df.sort_values("date")
            df_sorted["balance"] = df_sorted.apply(
                lambda row: row["amount"] if row["type"].lower() in ["credit", "income"] else -row["amount"],
                axis=1
            ).cumsum()

            bal_fig = px.line(
                df_sorted,
                x="date",
                y="balance",
                title="💹 Net Balance Over Time"
            )
            st.plotly_chart(bal_fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")

else:
    st.info("📤 Please upload a CSV file to view analysis.")

#ETBOT
with st.sidebar:
    st.markdown(
        """
        <style>
        .chatbot-container {
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            margin-bottom: 20px;
        }

        .chatbot-icon {
            background-color: #ff4b87;
            color: white;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            font-size: 20px;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
        }

        .chatbot-name {
            background-color: white;
            color: #333;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
        }
        </style>
        <div class="chatbot-container" onclick="document.getElementById('chat_expander').click();">
            <div class="chatbot-icon">🤖</div>
            <div class="chatbot-name">ETBot - AI Assistant</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Expander for AI Chat (appears when button is clicked)
    with st.expander("💬 Chat with ETBot", expanded=False):
        st.write(f"👋 Hi {st.session_state.user_email.split('@')[0]}! How can I help you today")

        user_query = st.text_input("Enter your question:")

        if st.button("Send ▶"):
            if user_query.strip():
                transactions_text = account.format_transactions_for_ai()
                budget_tip = get_budget_insights(user_query, transactions_text)
                st.write(budget_tip)
            else: 
                st.warning("Please enter a valid question.")
