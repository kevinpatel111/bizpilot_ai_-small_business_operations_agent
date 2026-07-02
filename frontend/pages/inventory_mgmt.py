import streamlit as st
import pandas as pd
from tools.business_tools import get_inventory_summary
from agents.inventory import run_inventory_agent

def render_inventory_mgmt():
    st.title("📦 Inventory Management")
    
    inventory = get_inventory_summary()
    if inventory.get("status") == "error":
        st.error(inventory.get("message"))
        return
        
    # Stats
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Stock Value", f"${inventory['total_valuation']:,.2f}")
    col2.metric("Total Items In Stock", f"{inventory['total_items']:,}")
    col3.metric("Low Stock Items Count", f"{len(inventory['low_stock_items'])}")
    
    st.markdown("---")
    
    # Restock list
    st.subheader("📋 Suggested Restock List")
    recs = inventory.get("restock_recommendations", [])
    if recs:
        df_recs = pd.DataFrame(recs)
        df_recs.columns = ["Product", "Current Stock", "Reorder Trigger Level", "Suggested Order Qty", "Estimated Cost ($)"]
        st.dataframe(df_recs, use_container_width=True, hide_index=True)
        st.write(f"**Total Reorder Investment Required:** ${df_recs['Estimated Cost ($)'].sum():,.2f}")
    else:
        st.success("All stock items are healthy! No restocks suggested.")
        
    st.markdown("---")
    
    # Overstocked items
    st.subheader("🐢 Overstocked Items (Potential Cash Tied Up)")
    over = inventory.get("overstock_items", [])
    if over:
        df_over = pd.DataFrame(over)[["product", "stocklevel", "reorderlevel", "unitcost", "valuation"]]
        df_over.columns = ["Product", "Current Stock", "Reorder Level", "Unit Cost ($)", "Stock Valuation ($)"]
        st.dataframe(df_over, use_container_width=True, hide_index=True)
    else:
        st.info("No overstocked items detected.")
        
    st.markdown("---")
    
    # Custom query
    st.subheader("💬 Ask Inventory Agent")
    query = st.text_input("Ask the Inventory Agent:", key="inventory_agent_query", placeholder="e.g. Which products represent the highest tied-up capital?")
    if st.button("Consult Inventory Agent"):
        if query:
            with st.spinner("Inventory Agent is analyzing data..."):
                response = run_inventory_agent(query)
                st.info(response)
        else:
            st.warning("Please enter a question.")
