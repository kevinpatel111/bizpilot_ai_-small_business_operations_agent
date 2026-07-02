import streamlit as st
import os
from database.db import init_db
from dotenv import load_dotenv

# Helper to write to .env
def update_env_variable(key: str, value: str):
    """Safely updates or appends a key-value pair in the local .env file."""
    env_file = ".env"
    lines = []
    found = False
    
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            lines = f.readlines()
            
    for i, line in enumerate(lines):
        if line.strip().startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            found = True
            break
            
    if not found:
        lines.append(f"{key}={value}\n")
        
    with open(env_file, "w") as f:
        f.writelines(lines)
        
    # Reload env
    os.environ[key] = value

def render_settings():
    st.title("⚙️ System Settings")
    st.write("Manage system keys, passwords, and database configurations.")
    
    # 1. API Key management
    st.subheader("🔑 LLM Configurations")
    current_key = os.getenv("GEMINI_API_KEY", "")
    masked_key = f"{current_key[:6]}...{current_key[-6:]}" if len(current_key) > 12 else ""
    
    st.write(f"Current Gemini API Key: `{masked_key if masked_key else 'Not Configured'}`")
    new_key = st.text_input("Enter New Gemini API Key", type="password", placeholder="AIzaSy...")
    
    if st.button("Update API Key"):
        if new_key:
            update_env_variable("GEMINI_API_KEY", new_key)
            st.success("API Key updated and saved to .env!")
            st.rerun()
        else:
            st.warning("Please enter a key.")
            
    st.markdown("---")
    
    # 2. Security configurations
    st.subheader("🔒 Administrator Password")
    new_pass = st.text_input("Change Admin Password", type="password", placeholder="New Password")
    if st.button("Update Password"):
        if new_pass:
            update_env_variable("ADMIN_PASSWORD", new_pass)
            st.success("Admin Password updated successfully!")
            st.rerun()
        else:
            st.warning("Please enter a password.")
            
    st.markdown("---")
    
    # 3. Database Diagnostics
    st.subheader("🛠️ Database Maintenance")
    st.write("Perform system diagnostics or reset data stores.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Reset / Initialize Database Schema"):
            try:
                init_db()
                st.success("Database tables verified/re-initialized successfully!")
            except Exception as e:
                st.error(f"Failed to initialize database: {e}")
                
    with col2:
        if st.button("Clear Cache & Logs"):
            # Delete log files inside logs/
            logs_dir = "logs"
            if os.path.exists(logs_dir):
                for f in os.listdir(logs_dir):
                    try:
                        os.remove(os.path.join(logs_dir, f))
                    except Exception:
                        pass
                st.success("Logs and file caches cleared successfully.")
            else:
                st.info("No logs directory found.")
