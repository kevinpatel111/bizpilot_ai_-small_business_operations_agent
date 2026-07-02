import streamlit as st
import os
from utils.security import validate_file_extension, validate_file_size, validate_csv_schema
from database.db import register_file, get_registered_files, delete_registered_file
from utils.logger import logger

def render_upload():
    st.title("📂 Upload Business Data")
    st.write("Upload your sales, inventory, and expense files. We support CSV and Excel format.")
    
    os.makedirs("data", exist_ok=True)
    
    file_types = {
        "sales": "Sales Records (Columns required: Date, Product, Quantity, Amount)",
        "inventory": "Inventory Records (Columns required: Product, StockLevel, ReorderLevel, UnitCost)",
        "expenses": "Expense Records (Columns required: Date, Category, Amount, Description)"
    }
    
    uploaded_files = get_registered_files()
    
    # 3 upload panels
    for f_type, label in file_types.items():
        st.subheader(f"{f_type.capitalize()} Report Upload")
        
        # Display current file status
        if f_type in uploaded_files:
            file_info = uploaded_files[f_type]
            st.info(f"✅ Current file: **{file_info['filename']}** (Uploaded: {file_info['uploaded_at']})")
            if st.button(f"Remove {f_type.capitalize()} File", key=f"del_{f_type}"):
                delete_registered_file(f_type)
                # optionally delete actual file on disk
                if os.path.exists(file_info['filepath']):
                    try:
                        os.remove(file_info['filepath'])
                    except Exception as e:
                        logger.error(f"Error deleting physical file: {e}")
                st.success(f"Removed {f_type} file registration.")
                st.rerun()
        
        # Drag and drop input
        uploaded_file = st.file_uploader(label, type=["csv", "xlsx", "xls"], key=f"upload_{f_type}")
        
        if uploaded_file is not None:
            # Perform validations
            filename = uploaded_file.name
            
            # 1. Ext check
            if not validate_file_extension(filename):
                st.error("Invalid file extension. Please upload a .csv, .xlsx, or .xls file.")
                continue
                
            # Temporary save to check size and schema
            temp_path = os.path.join("data", f"temp_{f_type}_{filename}")
            try:
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                    
                # 2. Size check
                if not validate_file_size(temp_path):
                    st.error("File size exceeds 10MB limit.")
                    os.remove(temp_path)
                    continue
                    
                # 3. Schema check
                is_valid, err_msg = validate_csv_schema(temp_path, f_type)
                if not is_valid:
                    st.error(f"Schema validation failed: {err_msg}")
                    os.remove(temp_path)
                    continue
                
                # If valid, rename to permanent path
                _, ext = os.path.splitext(filename.lower())
                perm_filename = f"{f_type}{ext}"
                perm_path = os.path.join("data", perm_filename)
                
                # Remove old file if exists
                if os.path.exists(perm_path):
                    os.remove(perm_path)
                    
                os.rename(temp_path, perm_path)
                
                # Register in database
                register_file(f_type, filename, perm_path)
                st.success(f"Successfully uploaded and validated {filename}!")
                st.rerun()
                
            except Exception as e:
                logger.error(f"Upload processing failed for {filename}: {e}")
                st.error(f"An error occurred while saving the file: {str(e)}")
                if os.path.exists(temp_path):
                    os.remove(temp_path)
