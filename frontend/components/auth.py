import streamlit as st
import os
from utils.security import check_auth
from dotenv import load_dotenv

load_dotenv()

def render_login():
    """Renders a visually appealing glassmorphic login screen."""
    # Custom CSS for login page design
    st.markdown("""
        <style>
        .login-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2rem;
            border-radius: 15px;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            max-width: 400px;
            margin: auto;
        }
        .login-title {
            font-size: 2rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 0.5rem;
            text-align: center;
            background: linear-gradient(45deg, #1E88E5, #00E676);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .login-subtitle {
            color: #b0bec5;
            margin-bottom: 2rem;
            text-align: center;
            font-size: 0.9rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="height: 10vh"></div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">BizPilot AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">Small Business Operations Agent</div>', unsafe_allow_html=True)
        
        password = st.text_input("Enter Admin Password", type="password", placeholder="password")
        correct_password = os.getenv("ADMIN_PASSWORD", "admin123")
        
        if st.button("Access Dashboard", use_container_width=True):
            if check_auth(password, correct_password):
                st.session_state.authenticated = True
                st.success("Access Granted!")
                st.rerun()
            else:
                st.error("Invalid password. Please try again.")
                
        st.markdown('</div>', unsafe_allow_html=True)
