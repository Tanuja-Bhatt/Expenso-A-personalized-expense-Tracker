# import sqlite3
# import pandas as pd
# import streamlit as st
# from datetime import date
# import schedule, time
# from datetime import datetime

# # ---------- REMINDER MANAGER ----------
# class ReminderManager:
#     def __init__(self, db_name):
#         self.db_name = db_name
#         self.conn = sqlite3.connect(self.db_name)
#         self.cursor = self.conn.cursor()

#         # Create the reminders table if it doesn't exist
#         self.cursor.execute('''CREATE TABLE IF NOT EXISTS reminders (
#                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                                 title TEXT NOT NULL,
#                                 due_date TEXT NOT NULL,
#                                 amount REAL,
#                                 type TEXT CHECK(type IN ('Bill', 'Budget')) NOT NULL,
#                                 status TEXT DEFAULT 'Pending')''')
#         self.conn.commit()

#     def addReminder(self, title, due_date, amount, rem_type):
#         self.cursor.execute('''INSERT INTO reminders (title, due_date, amount, type)
#                                VALUES (?, ?, ?, ?)''',
#                                (title, due_date, amount, rem_type))
#         self.conn.commit()

#     def viewReminders(self):
#         query = "SELECT * FROM reminders"
#         return pd.read_sql(query, self.conn)

#     def markCompleted(self, reminder_id):
#         self.cursor.execute("UPDATE reminders SET status='Completed' WHERE id=?", (reminder_id,))
#         self.conn.commit()

#     def deleteReminder(self, reminder_id):
#         self.cursor.execute("DELETE FROM reminders WHERE id=?", (reminder_id,))
#         self.conn.commit()


# # ---------- EXPENSE MANAGER ----------
# class ExpenseManager:
#     def __init__(self, db_name="expenses.db"):
#         self.conn = sqlite3.connect(db_name)
#         self.create_table()

#     def create_table(self):
#         query = """
#         CREATE TABLE IF NOT EXISTS expenses (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             description TEXT,
#             amount REAL,
#             date DATE,
#             category TEXT
#         )
#         """
#         self.conn.execute(query)
#         self.conn.commit()

#     def add_expense(self, description, amount, date, category="Others"):
#         query = "INSERT INTO expenses (description, amount, date, category) VALUES (?, ?, ?, ?)"
#         self.conn.execute(query, (description, amount, date, category))
#         self.conn.commit()

#     def view_expenses(self):
#         return pd.read_sql("SELECT * FROM expenses", self.conn)





# # ---------- INCOME MANAGER ----------
# class IncomeManager:
#     def __init__(self, db_name="expenses.db"):
#         self.conn = sqlite3.connect(db_name)
#         self.create_table()

#     def create_table(self):
        
#         query = """
#         CREATE TABLE IF NOT EXISTS income (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             description TEXT,
#             amount REAL,
#             date DATE,
#             category TEXT
#         )
#         """
#         self.conn.execute(query)
#         self.conn.commit()

#     def add_income(self, description, amount, date, category="Others"):
#         query = "INSERT INTO income (description, amount, date, category) VALUES (?, ?, ?, ?)"
#         self.conn.execute(query, (description, amount, date, category))
#         self.conn.commit()

#     def view_income(self):
#         return pd.read_sql("SELECT * FROM income", self.conn)




# # ---------- ACCOUNT MANAGER ----------
# class Account:
#     def __init__(self, db_name):
#         self.IncomeManager = IncomeManager(db_name)
#         self.ExpenseManager = ExpenseManager(db_name)
#         self.ReminderManager = ReminderManager(db_name)
#         self.Balance = 0.0

#     def getBalance(self):
#         total_income = self.IncomeManager.viewIncome()["amount"].sum()
#         total_expense = self.ExpenseManager.viewExpenses()["amount"].sum()
#         self.Balance = total_income - total_expense
#         return self.Balance

#     def addExpense(self, date, name, amount, category, description):
#         self.ExpenseManager.addExpense(date, name, amount, category, description)
#         self.Balance -= amount
#         st.success("Expense added successfully!")

#     def addIncome(self, date, name, amount, source, description):
#         self.IncomeManager.addIncome(date, name, amount, source, description)
#         self.Balance += amount
#         st.success("Income added successfully!")

#     def expenseList(self):
#         return self.ExpenseManager.view_expenses()

#     def incomeList(self):
#         return self.IncomeManager.view_income()

#     def deleteExpense(self, expense_id):
#         expenses = self.ExpenseManager.view_expenses()
#         if expenses.empty:
#             st.warning("No expenses to delete.")
#             return
#         if expense_id in expenses["id"].values:
#             amount = expenses.loc[expenses["id"] == expense_id, "amount"].iloc[0]
#             self.ExpenseManager.deleteExpense(expense_id)
#             self.Balance += amount
#             st.success(f"Expense {expense_id} deleted successfully!")
#         else:
#             st.warning(f"Invalid Expense ID: {expense_id}")

#     def deleteIncome(self, income_id):
#         incomes = self.IncomeManager.view_income()
#         if incomes.empty:
#             st.warning("No income records to delete.")
#             return
#         if income_id in incomes["id"].values:
#             amount = incomes.loc[incomes["id"] == income_id, "amount"].iloc[0]
#             self.IncomeManager.deleteIncome(income_id)
#             self.Balance -= amount
#             st.success(f"Income {income_id} deleted successfully!")
#         else:
#             st.warning(f"Invalid Income ID: {income_id}")

#     # ---------- AI TRANSACTION FORMAT ----------
#     def format_transactions_for_ai(self):
#         expenses = self.ExpenseManager.view_expenses()
#         income = self.IncomeManager.view_income()
#         formatted_expenses = expenses[['name', 'date', 'amount', 'category', 'description']].to_dict(orient='records')
#         formatted_income = income[['name', 'date', 'amount', 'source', 'description']].to_dict(orient='records')
#         transactions = {'income': formatted_income, 'expenses': formatted_expenses}
#         return transactions
    


import sqlite3
import pandas as pd
import streamlit as st
from datetime import datetime

# ---------- REMINDER MANAGER ----------
class ReminderManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Create the reminders table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS reminders (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT NOT NULL,
                                due_date TEXT NOT NULL,
                                amount REAL,
                                type TEXT CHECK(type IN ('Bill', 'Budget')) NOT NULL,
                                status TEXT DEFAULT 'Pending')''')
        self.conn.commit()

    def addReminder(self, title, due_date, amount, rem_type):
        self.cursor.execute('''INSERT INTO reminders (title, due_date, amount, type)
                               VALUES (?, ?, ?, ?)''',
                               (title, due_date, amount, rem_type))
        self.conn.commit()

    def viewReminders(self):
        query = "SELECT * FROM reminders"
        return pd.read_sql(query, self.conn)

    def markCompleted(self, reminder_id):
        self.cursor.execute("UPDATE reminders SET status='Completed' WHERE id=?", (reminder_id,))
        self.conn.commit()

    def deleteReminder(self, reminder_id):
        self.cursor.execute("DELETE FROM reminders WHERE id=?", (reminder_id,))
        self.conn.commit()


# ---------- EXPENSE MANAGER ----------
class ExpenseManager:
    def __init__(self, db_name="expenses.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            amount REAL,
            date DATE,
            category TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_expense(self, description, amount, date, category="Others"):
        query = "INSERT INTO expenses (description, amount, date, category) VALUES (?, ?, ?, ?)"
        self.conn.execute(query, (description, amount, date, category))
        self.conn.commit()

    def view_expenses(self):
        return pd.read_sql("SELECT * FROM expenses", self.conn)


# ---------- INCOME MANAGER ----------
class IncomeManager:
    def __init__(self, db_name="expenses.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            amount REAL,
            date DATE,
            category TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_income(self, description, amount, date, category="Others"):
        query = "INSERT INTO income (description, amount, date, category) VALUES (?, ?, ?, ?)"
        self.conn.execute(query, (description, amount, date, category))
        self.conn.commit()

    def view_income(self):
        return pd.read_sql("SELECT * FROM income", self.conn)


# ---------- BUDGET MANAGER ----------
class BudgetManager:
    def __init__(self, db_name="expenses.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT UNIQUE,
            limit_amount REAL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def set_budget(self, category, limit_amount):
        query = """
        INSERT INTO budgets (category, limit_amount)
        VALUES (?, ?)
        ON CONFLICT(category) DO UPDATE SET limit_amount = excluded.limit_amount
        """
        self.conn.execute(query, (category, limit_amount))
        self.conn.commit()

    def get_budgets(self):
        return pd.read_sql("SELECT * FROM budgets", self.conn)

    def get_budget_for_category(self, category):
        cursor = self.conn.execute("SELECT limit_amount FROM budgets WHERE category=?", (category,))
        row = cursor.fetchone()
        return row[0] if row else None

    def delete_budget(self, category):
        self.conn.execute("DELETE FROM budgets WHERE category=?", (category,))
        self.conn.commit()


# ---------- ACCOUNT MANAGER ----------
class Account:
    def __init__(self, db_name):
        self.IncomeManager = IncomeManager(db_name)
        self.ExpenseManager = ExpenseManager(db_name)
        self.ReminderManager = ReminderManager(db_name)
        self.BudgetManager = BudgetManager(db_name)  # 🔹 Integrated here
        self.Balance = 0.0

    def getBalance(self):
        total_income = self.IncomeManager.view_income()["amount"].sum()
        total_expense = self.ExpenseManager.view_expenses()["amount"].sum()
        self.Balance = total_income - total_expense
        return self.Balance

    def addExpense(self, description, amount, date, category):
        self.ExpenseManager.add_expense(description, amount, date, category)
        self.Balance -= amount
        st.success("Expense added successfully!")

    def addIncome(self, description, amount, date, category):
        self.IncomeManager.add_income(description, amount, date, category)
        self.Balance += amount
        st.success("Income added successfully!")

    def expenseList(self):
        return self.ExpenseManager.view_expenses()

    def incomeList(self):
        return self.IncomeManager.view_income()

    def deleteExpense(self, expense_id):
        expenses = self.ExpenseManager.view_expenses()
        if expenses.empty:
            st.warning("No expenses to delete.")
            return
        if expense_id in expenses["id"].values:
            amount = expenses.loc[expenses["id"] == expense_id, "amount"].iloc[0]
            self.ExpenseManager.conn.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
            self.ExpenseManager.conn.commit()
            self.Balance += amount
            st.success(f"Expense {expense_id} deleted successfully!")
        else:
            st.warning(f"Invalid Expense ID: {expense_id}")

    def deleteIncome(self, income_id):
        incomes = self.IncomeManager.view_income()
        if incomes.empty:
            st.warning("No income records to delete.")
            return
        if income_id in incomes["id"].values:
            amount = incomes.loc[incomes["id"] == income_id, "amount"].iloc[0]
            self.IncomeManager.conn.execute("DELETE FROM income WHERE id=?", (income_id,))
            self.IncomeManager.conn.commit()
            self.Balance -= amount
            st.success(f"Income {income_id} deleted successfully!")
        else:
            st.warning(f"Invalid Income ID: {income_id}")

    # ---------- AI TRANSACTION FORMAT ----------
    def format_transactions_for_ai(self):
        expenses = self.ExpenseManager.view_expenses()
        income = self.IncomeManager.view_income()
        formatted_expenses = expenses[['description', 'date', 'amount', 'category']].to_dict(orient='records')
        formatted_income = income[['description', 'date', 'amount', 'category']].to_dict(orient='records')
        transactions = {'income': formatted_income, 'expenses': formatted_expenses}
        return transactions
