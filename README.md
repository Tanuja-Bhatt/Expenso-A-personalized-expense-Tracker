# Expenso-A-personalized-expense-Tracker
<h1> 🚀 Expenso – AI-Powered Personal Expense Tracker</h1>

Expenso is an AI-powered personal finance management application designed to simplify expense tracking, budgeting, and financial planning.
The system automates transaction analysis by allowing users to upload bank statements in CSV format, visualize spending patterns, manage budgets, set bill reminders, and gain intelligent insights through an AI chatbot.

This project bridges the gap between raw bank transaction data and actionable financial intelligence.


<h1>✨ Key Features</h1>

<h1>Bank Statement Upload (CSV)</h1>

  * Import real or sample bank transaction CSV files
  * Automatic parsing and categorization of transactions

<h1>Expense & Income Management</h1>

  * Separate tracking of expenses and income
  * Category-wise classification

<h1>Interactive Reports & Dashboards</h1>

  * Monthly expense vs income trends
  * Category-wise spending analysis
  * KPI metrics (Total Income, Expense, Savings)

  <h1>Budget Planner</h1>

  * Set monthly category-wise budget limits
  * Alerts when spending exceeds limits

  <h1>Bill Reminder System</h1>

  * Create reminders for upcoming bills
  * Track pending and completed reminders
  * Helps avoid missed payments

  <h1>AI Financial Assistant (ETBot)</h1>

  * Ask natural-language queries about spending
  * Get AI-driven financial insights using Cohere API

  <h1>Indian Currency Formatting</h1>

  * Displays amounts in Lakhs and Crores for better regional clarity


<h1>Technology Stack</h1>

| Layer           | Technology         |
| --------------- | ------------------ |
| Frontend        | Streamlit          |
| Backend         | Python             |
| Database        | SQLite             |
| Data Processing | Pandas, NumPy      |
| Visualization   | Plotly             |
| AI Integration  | Cohere API         |
| Authentication  | Custom Auth Module |



 <h1>Project Structure</h1>

```
Expenso/
│
├── home.py
├── auth.py
│
├── pages/
│   ├── upload_transactions.py
│   ├── view_transactions.py
│   ├── budget_planner.py
│   ├── report.py
│   ├── reminders.py
│
├── utils/
│   ├── expenseTracker.py
│   ├── ETbot.py
│
├── sample_data/
│   └── sample_bank_transactions.csv
│
├── requirements.txt
└── .gitignore


```

<h1> How to Run the Project Locally</h1>

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/Expenso-AI-Powered-Expense-Tracker.git
cd Expenso-AI-Powered-Expense-Tracker
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Application

```bash
streamlit run home.py
```

---



## 📌 Use Case

This application is useful for:

* Students managing monthly expenses
* Individuals tracking digital transactions
* Learning data analytics with real-world finance data
* Demonstrating full-stack + AI integration skills

---

## 🚧 Limitations

* Does not support real-time bank account integration
* Requires manual CSV upload
* AI insights depend on external API availability

---

## 🚀 Future Enhancements

* Real-time bank integration using APIs
* SMS & email transaction parsing
* Mobile application (Android/iOS)
* PDF & Excel report export
* Predictive expense analysis using ML

---

## 👩‍💻 Contributors

**Team Project – Equal Contribution**

* Backend & Database Development
* CSV Automation & Data Processing
* UI/UX & Data Visualization
* AI Integration & Testing

---

## 📄 License

This project is developed for **academic and learning purposes**.

---

## 🙌 Acknowledgment

This project was developed as part of academic coursework and inspired by real-world personal finance management systems.

---


