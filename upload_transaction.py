import streamlit as st
import pandas as pd
import sqlite3
from utils.expenseTracker import ExpenseManager, IncomeManager

# --- Ensure user is logged in ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to continue :)")
    st.stop()

st.title("📤 Upload Bank Statement")
st.write("Upload your bank statement (.csv) to automatically import transactions.")

# --- Initialize managers and DB ---
db_name = "expenses.db"
ExManager = ExpenseManager(db_name=db_name)
InManager = IncomeManager(db_name=db_name)

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        required_cols = {"Id", "Description", "Date", "Amount", "Category", "Type"}
        if not required_cols.issubset(df.columns):
            st.error(f"CSV must contain columns: {required_cols}")
        else:
            st.success("✅ File uploaded successfully")
            st.dataframe(df.head())

            # --- User choice: Replace or Append ---
            st.markdown("#### ⚙️ Import Options")
            import_option = st.radio(
                "How do you want to import this file?",
                ("Replace old data", "Append to existing data"),
                horizontal=True
            )

            if st.button("📥 Import Transactions"):
                conn = sqlite3.connect(db_name)
                cursor = conn.cursor()

                # --- Clear old data if Replace selected ---
                if import_option == "Replace old data":
                    cursor.execute("DELETE FROM expenses")
                    cursor.execute("DELETE FROM income")
                    conn.commit()
                    st.info("🧹 Old data cleared before importing new transactions.")

                # --- Insert new data ---
                inserted_exp = inserted_inc = 0
                for _, row in df.iterrows():
                    desc = str(row["Description"])
                    amount = float(row["Amount"])
                    date = str(row["Date"])
                    category = str(row["Category"])
                    t_type = str(row["Type"]).strip().lower()

                    if t_type == "debit":
                        ExManager.add_expense(desc, amount, date, category)
                        inserted_exp += 1
                    elif t_type == "credit":
                        InManager.add_income(desc, amount, date, category)
                        inserted_inc += 1

                conn.commit()
                conn.close()

                # --- Save dataframe in session for other pages (like Budget Planner) ---
                st.session_state["uploaded_df"] = df

                st.success(f"🎉 Imported successfully! {inserted_exp} expenses and {inserted_inc} incomes added.")
                st.info("✅ You can now view reports, budgets, and summaries using this new data.")

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")

