import streamlit as st
from database.db import get_chat_history, add_chat_message, clear_chat_history
from agents.coordinator import run_coordinator_agent

def render_chat():
    st.title("💬 AI Chat Assistant")
    st.write("Ask our Coordinator Agent anything about your business sales, inventory, or expenses.")
    
    session_id = st.session_state.get("session_id", "default_user")
    
    # Clear history button
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("Clear Chat", use_container_width=True):
            clear_chat_history(session_id)
            st.success("Chat history cleared.")
            st.rerun()
            
    # Retrieve and show chat messages
    messages = get_chat_history(session_id)
    
    # If empty, add a default welcoming message
    if not messages:
        welcome_text = (
            "Hello! I am your BizPilot AI Coordinator. I can coordinate with specialized agents to analyze "
            "your sales records, monitor inventory levels, outline marketing plans, or compile a complete health advisory. "
            "How can I help you today?"
        )
        add_chat_message(session_id, "assistant", welcome_text)
        messages = [{"role": "assistant", "content": welcome_text}]
        
    # Render messages
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    # User Input
    user_query = st.chat_input("Ask a question about your business...")
    if user_query:
        # Display user message instantly
        with st.chat_message("user"):
            st.write(user_query)
            
        # Save to DB
        add_chat_message(session_id, "user", user_query)
        
        # Run Coordinator Agent
        with st.spinner("Coordinator Agent is consulting specialized agents..."):
            response = run_coordinator_agent(user_query)
            
        # Display assistant message
        with st.chat_message("assistant"):
            st.write(response)
            
        # Save response to DB
        add_chat_message(session_id, "assistant", response)
        st.rerun()
