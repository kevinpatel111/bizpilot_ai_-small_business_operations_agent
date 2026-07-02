import streamlit as st
import os
import uuid
from dotenv import load_dotenv

# Set page config FIRST before any streamlit calls!
st.set_page_config(
    page_title="BizPilot AI - Business Operations Agent",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load env variables
load_dotenv()

from frontend.components.auth import render_login
from frontend.pages.dashboard import render_dashboard
from frontend.pages.upload import render_upload
from frontend.pages.chat import render_chat
from frontend.pages.sales_analytics import render_sales_analytics
from frontend.pages.inventory_mgmt import render_inventory_mgmt
from frontend.pages.finance_mgmt import render_finance_mgmt
from frontend.pages.marketing_mgmt import render_marketing_mgmt
from frontend.pages.reports_mgmt import render_reports_mgmt
from frontend.pages.settings import render_settings

# Session states initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Set custom styling (vibrant dark mode, premium typography)
st.markdown("""
    <style>
    /* Main body background color */
    .stApp {
        background-color: #0E1117;
        color: #ECEFF1;
    }
    
    /* Input borders and card layouts */
    div[data-baseweb="select"] > div {
        background-color: #1E293B !important;
        border-color: rgba(255,255,255,0.1) !important;
    }
    
    /* Custom button aesthetics */
    .stButton>button {
        border-radius: 8px;
        background: linear-gradient(135deg, #1E88E5, #1565C0);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #1565C0, #0D47A1);
        box-shadow: 0 4px 15px rgba(30,136,229,0.4);
        transform: translateY(-1px);
    }
    
    /* Header gradients */
    h1 {
        background: linear-gradient(45deg, #2196F3, #00E676);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 1. Access control
if not st.session_state.authenticated:
    render_login()
else:
    # Sidebar navigation
    st.sidebar.title("✈️ BizPilot AI")
    st.sidebar.write("Small Business Operations Agent")
    
    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Upload Data",
            "AI Chat",
            "Sales Analytics",
            "Inventory",
            "Finance",
            "Marketing",
            "Reports",
            "Settings"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.caption("System Status: **Online**")
    if os.getenv("GEMINI_API_KEY"):
        st.sidebar.caption("Gemini AI API: **Connected**")
    else:
        st.sidebar.caption("Gemini AI API: ⚠️ **Disconnected**")
        
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()
        
    # Route pages
    if page == "Dashboard":
        render_dashboard()
    elif page == "Upload Data":
        render_upload()
    elif page == "AI Chat":
        render_chat()
    elif page == "Sales Analytics":
        render_sales_analytics()
    elif page == "Inventory":
        render_inventory_mgmt()
    elif page == "Finance":
        render_finance_mgmt()
    elif page == "Marketing":
        render_marketing_mgmt()
    elif page == "Reports":
        render_reports_mgmt()
    elif page == "Settings":
        render_settings()
