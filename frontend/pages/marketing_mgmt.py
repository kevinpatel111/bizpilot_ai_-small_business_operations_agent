import streamlit as st
from agents.marketing import run_marketing_agent

def render_marketing_mgmt():
    st.title("📣 Marketing & Promotions Generator")
    st.write("Generate high-converting promotional copies, social media posts, or WhatsApp messages.")
    
    tab1, tab2 = st.tabs(["⚡ Fast Promo Generator", "💬 Consult Marketing Agent"])
    
    with tab1:
        st.subheader("Generate Campaign Copy")
        product = st.text_input("Product Name", placeholder="e.g., Organic Cotton T-Shirt")
        campaign_type = st.selectbox("Campaign Goal", ["General Awareness", "Clearance Sale (Slow Item)", "Holiday Discount", "Buy One Get One (BOGO)"])
        channel = st.selectbox("Channel", ["Instagram Post", "WhatsApp Broadcast Message", "Facebook Ad Copy", "Email Newsletter Headline"])
        details = st.text_area("Extra Details (Optional)", placeholder="e.g., 20% off this weekend only, free shipping on orders over $50")
        
        if st.button("Generate Copy"):
            if product:
                prompt = (
                    f"Create {channel} marketing copy for the product '{product}'. "
                    f"The campaign goal is: '{campaign_type}'. "
                    f"Additional details to include: '{details if details else 'None'}'."
                )
                with st.spinner("Drafting copy..."):
                    copy = run_marketing_agent(prompt)
                    st.success("Draft Completed!")
                    st.markdown("---")
                    st.code(copy, language="markdown")
            else:
                st.warning("Please enter a product name.")
                
    with tab2:
        st.subheader("Ask the Marketing Agent")
        st.write("Ask the marketing agent for campaign strategies, discount recommendations for slow-moving items, or social media calendars.")
        
        query = st.text_input("Ask the Marketing Agent:", key="marketing_agent_query", placeholder="e.g. Suggest a discount and WhatsApp message for my slowest-selling items.")
        if st.button("Consult Marketing Agent"):
            if query:
                with st.spinner("Marketing Agent is planning campaigns..."):
                    response = run_marketing_agent(query)
                    st.info(response)
            else:
                st.warning("Please enter a question.")
                
    # Proactive recommendations
    st.markdown("---")
    st.subheader("💡 Automated Slow-Item Campaigns")
    if st.button("Auto-Draft Promos for Slow-Moving Products"):
        with st.spinner("Checking sales records and generating copy..."):
            response = run_marketing_agent("Find my slow-moving products and write a social media post and discount recommendation for each.")
            st.info(response)
