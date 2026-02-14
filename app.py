import streamlit as st
import plotly.express as px

from models.transaction import Transaction
from services.database import Database
from services.analytics import Analytics
from services.ai_insights import AIInsights
from services.report_generator import ReportGenerator

st.set_page_config(page_title="AI Expense Tracker", layout="wide")

db = Database()
analytics = Analytics(db)
reporter = ReportGenerator(analytics)

st.title("🤖 AI Expense Tracker Dashboard")

# ---------- sidebar ----------
st.sidebar.header("Add Transaction")

t_type = st.sidebar.selectbox("Type", ["income","expense"])
amount = st.sidebar.number_input("Amount", min_value=0.0)
category = st.sidebar.text_input("Category")

if st.sidebar.button("Add Transaction"):
    t = Transaction(1, amount, category, t_type)
    db.add_transaction(t)
    st.sidebar.success("Added!")

if st.sidebar.button("Export Report"):
    reporter.export_csv()
    st.sidebar.success("Saved in result/report.csv")

# ---------- data ----------
df = analytics.load_dataframe()

if df.empty:
    st.warning("Add some transactions first.")
    st.stop()

income, expense, savings = analytics.summary()

# ---------- KPI cards ----------
c1,c2,c3 = st.columns(3)
c1.metric("Income", f"₹ {income:,.0f}")
c2.metric("Expense", f"₹ {expense:,.0f}")
c3.metric("Savings", f"₹ {savings:,.0f}")

# ---------- charts ----------
col1,col2 = st.columns(2)

with col1:
    fig = px.bar(
        df.groupby("type")["amount"].sum().reset_index(),
        x="type", y="amount",
        title="Income vs Expense"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    exp_df = df[df.type=="expense"]
    if not exp_df.empty:
        fig2 = px.pie(exp_df, names="category", values="amount",
                      title="Expense Distribution")
        st.plotly_chart(fig2, use_container_width=True)

daily = exp_df.groupby("date")["amount"].sum().reset_index()
fig3 = px.line(daily, x="date", y="amount",
               markers=True, title="Daily Expense Trend")
st.plotly_chart(fig3, use_container_width=True)

# ---------- AI SECTION ----------
st.subheader("🤖 AI Financial Insights")

ai = AIInsights(df)
insights = ai.generate_insights()

for tip in insights:
    st.info(tip)
