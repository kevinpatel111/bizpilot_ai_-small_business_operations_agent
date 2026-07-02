import os
import pandas as pd
from typing import Tuple, List, Dict
from utils.logger import logger

# Configuration Limits
MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}

# Column schemas
REQUIRED_COLUMNS: Dict[str, List[str]] = {
    "sales": ["date", "product", "quantity", "amount"],
    "inventory": ["product", "stocklevel", "reorderlevel", "unitcost"],
    "expenses": ["date", "category", "amount", "description"]
}

def validate_file_size(filepath: str) -> bool:
    """Validate that the file size is under the limit."""
    try:
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        if size_mb > MAX_FILE_SIZE_MB:
            logger.warning(f"File {filepath} exceeds size limit: {size_mb:.2f}MB > {MAX_FILE_SIZE_MB}MB")
            return False
        return True
    except Exception as e:
        logger.error(f"Error checking file size for {filepath}: {e}")
        return False

def validate_file_extension(filename: str) -> bool:
    """Validate that the file extension is allowed."""
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_EXTENSIONS

def validate_csv_schema(filepath: str, file_type: str) -> Tuple[bool, str]:
    """
    Validate that the uploaded CSV/Excel file contains the required columns.
    Returns (is_valid, error_message).
    """
    if file_type not in REQUIRED_COLUMNS:
        return False, f"Unknown file type: {file_type}"
    
    try:
        _, ext = os.path.splitext(filepath.lower())
        if ext == ".csv":
            # read only top few lines to validate schema efficiently
            df = pd.read_csv(filepath, nrows=5)
        else:
            df = pd.read_excel(filepath, nrows=5)
            
        columns = [col.lower().strip().replace(" ", "") for col in df.columns]
        missing = []
        for req in REQUIRED_COLUMNS[file_type]:
            if req not in columns:
                missing.append(req)
                
        if missing:
            logger.warning(f"File validation failed for {file_type}. Missing columns: {missing}")
            return False, f"Missing required columns: {', '.join(missing)}"
            
        return True, "Valid"
    except Exception as e:
        logger.error(f"Error validating schema for {filepath}: {e}")
        return False, f"Failed to read file: {str(e)}"

def check_auth(password: str, correct_password: str) -> bool:
    """Check if the provided password matches the configured password."""
    if not correct_password:
        return True # If password is not configured, allow access
    return password == correct_password
