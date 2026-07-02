import streamlit as st
import plotly.express as px
import pandas as pd
from tools.business_tools import get_sales_summary
from agents.sales import run_sales_agent

def render_sales_analytics():
    st.title("📈 Sales Analytics")
    
    sales = get_sales_summary()
    if sales.get("status") == "error":
        st.error(sales.get("message"))
        return
        
    # Stats
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${sales['total_revenue']:,.2f}")
    col2.metric("Total Items Sold", f"{sales['total_items_sold']:,}")
    col3.metric("Data Records", f"{sales['records_count']:,} sales records")
    
    st.markdown("---")
    
    # Graphs
    st.subheader("Monthly Sales Trends")
    if sales.get("monthly_trends"):
        df_trends = pd.DataFrame(sales["monthly_trends"])
        fig = px.bar(df_trends, x="month_yr", y="amount", 
                     labels={"month_yr": "Month", "amount": "Revenue ($)"},
                     template="plotly_dark", color="amount", color_continuous_scale="Viridis")
        st.plotly_chart(fig, use_container_width=True)
        
    st.markdown("---")
    
    # Top & Slow Selling Products Side by Side
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🏆 Top Products (by Revenue)")
        df_top = pd.DataFrame(sales["top_products"])
        df_top.columns = ["Product", "Total Revenue ($)"]
        st.dataframe(df_top, use_container_width=True, hide_index=True)
        
    with c2:
        st.subheader("🐌 Slow-Moving Products (by Quantity)")
        df_slow = pd.DataFrame(sales["slow_moving_products"])
        df_slow.columns = ["Product", "Quantity Sold"]
        st.dataframe(df_slow, use_container_width=True, hide_index=True)
        
    st.markdown("---")
    
    # Custom query
    st.subheader("💬 Ask Sales Agent")
    st.write("Ask specific questions about your sales data (e.g., 'What was our best month?' or 'How is product X performing?').")
    
    query = st.text_input("Ask the Sales Agent:", key="sales_agent_query", placeholder="e.g. List the top selling products by sales volume.")
    if st.button("Consult Sales Agent"):
        if query:
            with st.spinner("Sales Agent is analyzing data..."):
                response = run_sales_agent(query)
                st.info(response)
        else:
            st.warning("Please enter a question.")
