import streamlit as st
import pandas as pd
import plotly.express as px
from utils.expenseTracker import ExpenseManager, BudgetManager

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to continue :)")
    st.stop()

st.set_page_config(page_title="Budget Planner", layout="wide")

st.title("💰 Monthly Budget Planner")

# Initialize managers
db_name = "expenses.db"
expense_manager = ExpenseManager(db_name=db_name)
budget_manager = BudgetManager(db_name=db_name)

# --- Fetch data from database ---
expenses_df = expense_manager.view_expenses()
budgets_df = budget_manager.get_budgets()

# --- Handle empty data ---
if expenses_df.empty:
    st.warning("⚠️ No expenses found in the database. Please upload or add transactions first.")
    st.stop()

# --- Clean data ---
expenses_df["date"] = pd.to_datetime(expenses_df["date"], errors="coerce")
expenses_df["month"] = expenses_df["date"].dt.strftime("%Y-%m")

# --- Current Month ---
current_month = expenses_df["month"].max()

st.markdown(f"### 📅 Showing Budget Report for **{current_month}**")

# --- Step 1: Add / Update Budget ---
st.divider()
st.markdown("### 🧾 Set or Update Budget Limits")

categories = sorted(expenses_df["category"].dropna().unique())

col1, col2 = st.columns([2, 1])
with col1:
    category = st.selectbox("Select Category", categories)
with col2:
    limit = st.number_input("Set Monthly Limit (₹)", min_value=0.0, step=500.0)

if st.button("💾 Save Budget"):
    budget_manager.set_budget(category, limit)
    st.success(f"✅ Budget for **{category}** set to ₹{limit:,.2f}")

# --- Step 2: Budget Overview ---
st.divider()
st.markdown("### 📊 Budget Overview")

budgets_df = budget_manager.get_budgets()  # refresh data
if budgets_df.empty:
    st.info("No budgets set yet. Please add category limits above.")
    st.stop()

st.dataframe(budgets_df, use_container_width=True)

# --- Step 3: Compare Expenses vs Budget ---
st.divider()
st.markdown("### 📈 Expense vs Budget Analysis")

# Filter current month's expenses
monthly_expense = expenses_df[expenses_df["month"] == current_month]
exp_by_cat = monthly_expense.groupby("category", as_index=False)["amount"].sum()

# Merge with budget limits
merged = pd.merge(exp_by_cat, budgets_df, on="category", how="left")
merged["remaining"] = merged["limit_amount"] - merged["amount"]
merged["status"] = merged["remaining"].apply(lambda x: "Over Budget" if x < 0 else "Within Budget")

# --- Step 4: Alerts ---
st.markdown("### ⚠️ Budget Alerts")
exceeded = merged[merged["remaining"] < 0]
if not exceeded.empty:
    for _, row in exceeded.iterrows():
        st.error(f"🚨 You exceeded your **{row['category']}** budget by ₹{abs(row['remaining']):,.2f}")
else:
    st.success("🎉 All your spending is within set limits this month!")

# --- Step 5: Visual Comparison ---
fig = px.bar(
    merged,
    x="category",
    y=["amount", "limit_amount"],
    barmode="group",
    title=f"Spending vs Budget for {current_month}",
    labels={"value": "Amount (₹)", "variable": "Type"},
    color_discrete_sequence=["#FF6B6B", "#4CAF50"]
)
st.plotly_chart(fig, use_container_width=True)

# --- Step 6: Progress Bar Visualization ---
st.divider()
st.markdown("### 📊 Budget Utilization by Category")

for _, row in merged.iterrows():
    spent = row["amount"]
    limit_amt = row["limit_amount"]
    percent = min((spent / limit_amt) * 100, 100) if limit_amt > 0 else 0
    color = "red" if spent > limit_amt else "green"

    st.markdown(f"**{row['category']}** — Spent ₹{spent:,.2f} / ₹{limit_amt:,.2f}")
    st.progress(percent / 100)

