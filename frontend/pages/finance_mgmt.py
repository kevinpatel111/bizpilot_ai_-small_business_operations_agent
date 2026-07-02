import streamlit as st
import pandas as pd
import plotly.express as px
from tools.business_tools import get_finance_summary
from agents.finance import run_finance_agent

def render_finance_mgmt():
    st.title("💸 Financial Management")
    
    finance = get_finance_summary()
    if finance.get("status") == "error":
        st.error(finance.get("message"))
        return
        
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"${finance['total_revenue']:,.2f}")
    col2.metric("Total Expenses", f"${finance['total_expenses']:,.2f}")
    col3.metric("Net Profit", f"${finance['net_profit']:,.2f}")
    col4.metric("Profit Margin", f"{finance['profit_margin']:.1f}%")
    
    st.markdown("---")
    
    # Graphs
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Expenses by Category")
        df_cat = pd.DataFrame(finance["expenses_by_category"])
        df_cat.columns = ["Category", "Amount ($)"]
        fig_pie = px.pie(df_cat, names="Category", values="Amount ($)", template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.subheader("Monthly Expenses Trend")
        if finance.get("monthly_expenses"):
            df_trends = pd.DataFrame(finance["monthly_expenses"])
            fig_line = px.line(df_trends, x="month_yr", y="amount", markers=True,
                               labels={"month_yr": "Month", "amount": "Expense ($)"},
                               template="plotly_dark", color_discrete_sequence=["#FF5252"])
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("No monthly expense trends available.")
            
    st.markdown("---")
    
    # Table breakdown
    st.subheader("📋 Expense Categories Details")
    st.dataframe(df_cat, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Custom query
    st.subheader("💬 Ask Finance Agent")
    query = st.text_input("Ask the Finance Agent:", key="finance_agent_query", placeholder="e.g. How can I reduce my expenses?")
    if st.button("Consult Finance Agent"):
        if query:
            with st.spinner("Finance Agent is analyzing expenses..."):
                response = run_finance_agent(query)
                st.info(response)
        else:
            st.warning("Please enter a question.")
