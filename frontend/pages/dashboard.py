import streamlit as st
import plotly.express as px
import pandas as pd
from tools.business_tools import get_sales_summary, get_inventory_summary, get_finance_summary
from agents.advisor import run_advisor_agent

def render_dashboard():
    st.title("📊 Operations Dashboard")
    st.write("Overview of your small business sales, inventory, and finance.")
    
    # 1. Fetch metrics
    sales = get_sales_summary()
    inventory = get_inventory_summary()
    finance = get_finance_summary()
    
    # Check if files are uploaded
    if sales.get("status") == "error" and inventory.get("status") == "error" and finance.get("status") == "error":
        st.warning("⚠️ No data files have been uploaded yet. Fallback sample data is being shown if available, or go to 'Upload Data' to upload your records.")
        
    # Top-level numbers
    revenue = sales.get("total_revenue", 0.0) if sales.get("status") == "success" else 0.0
    expenses = finance.get("total_expenses", 0.0) if finance.get("status") == "success" else 0.0
    profit = revenue - expenses
    margin = (profit / revenue * 100) if revenue > 0 else 0
    
    low_stock_count = 0
    if inventory.get("status") == "success":
        low_stock_count = len(inventory.get("low_stock_items", []))
        
    # CSS glassmorphism cards style
    st.markdown("""
        <style>
        .metric-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .metric-title {
            font-size: 0.9rem;
            color: #b0bec5;
            margin-bottom: 0.5rem;
        }
        .metric-val {
            font-size: 1.8rem;
            font-weight: 700;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Metrics Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Total Revenue</div><div class="metric-val" style="color: #00E676">${revenue:,.2f}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Total Expenses</div><div class="metric-val" style="color: #FF5252">${expenses:,.2f}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Net Profit</div><div class="metric-val" style="color: #29B6F6">${profit:,.2f} ({margin:.1f}%)</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Low Stock Alerts</div><div class="metric-val" style="color: #FFD740">{low_stock_count}</div></div>', unsafe_allow_html=True)
        
    st.markdown("---")
    
    # Charts Row
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Monthly Sales Revenue")
        if sales.get("status") == "success" and sales.get("monthly_trends"):
            df_trends = pd.DataFrame(sales["monthly_trends"])
            fig_sales = px.line(df_trends, x="month_yr", y="amount", markers=True, 
                                labels={"month_yr": "Month", "amount": "Revenue ($)"},
                                template="plotly_dark", color_discrete_sequence=["#00E676"])
            st.plotly_chart(fig_sales, use_container_width=True)
        else:
            st.info("No monthly sales data to plot.")
            
    with col_chart2:
        st.subheader("Expenses Breakdown")
        if finance.get("status") == "success" and finance.get("expenses_by_category"):
            df_exp = pd.DataFrame(finance["expenses_by_category"])
            fig_exp = px.pie(df_exp, names="category", values="amount", 
                             template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_exp, use_container_width=True)
        else:
            st.info("No expense categories data to plot.")
            
    # Bottom Row: Best Selling vs Low Stock
    col_table1, col_table2 = st.columns(2)
    
    with col_table1:
        st.subheader("🏆 Best-Selling Products")
        if sales.get("status") == "success" and sales.get("top_products"):
            df_top = pd.DataFrame(sales["top_products"])
            # Format columns
            df_top.columns = ["Product", "Sales Amount ($)"]
            st.dataframe(df_top, use_container_width=True, hide_index=True)
        else:
            st.info("No sales records available.")
            
    with col_table2:
        st.subheader("⚠️ Low Stock Items")
        if inventory.get("status") == "success" and inventory.get("low_stock_items"):
            df_low = pd.DataFrame(inventory["low_stock_items"])[["product", "stocklevel", "reorderlevel"]]
            df_low.columns = ["Product", "Stock", "Reorder Level"]
            st.dataframe(df_low, use_container_width=True, hide_index=True)
        else:
            st.success("All stock items are healthy!")
            
    st.markdown("---")
    
    # Quick Advisor Recommendations
    st.subheader("💡 AI Business Advisor Recommendations")
    if st.button("Generate Latest AI Operations Audit"):
        with st.spinner("Analyzing operations data..."):
            audit = run_advisor_agent("Evaluate business health score, list top 3 risks, top 3 opportunities, and next steps.")
            st.markdown(audit)
    else:
        st.write("Click the button above to generate a live operations audit from the AI Business Advisor Agent.")
