import os
import sys
# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from fastmcp import FastMCP
from tools.business_tools import search_business_data, get_sales_summary, get_inventory_summary, get_finance_summary, get_file_path
from tools.reporting_tools import generate_pdf_report, export_excel_report, generate_charts
from utils.logger import logger
import pandas as pd

# Initialize FastMCP Server
mcp = FastMCP("BizPilot AI Operations Server")

@mcp.tool
def read_csv(file_type: str) -> str:
    """
    Read contents of an uploaded business CSV file.
    file_type must be one of: 'sales', 'inventory', 'expenses'.
    """
    path = get_file_path(file_type)
    if not path:
        return f"Error: No CSV file found for {file_type}."
    try:
        df = pd.read_csv(path)
        # return a preview of the first 20 rows
        return f"Showing first 20 rows of {file_type} data:\n{df.head(20).to_string(index=False)}"
    except Exception as e:
        logger.error(f"Error in read_csv: {e}")
        return f"Error reading CSV: {str(e)}"

@mcp.tool
def read_excel(file_type: str) -> str:
    """
    Read contents of an uploaded business Excel file.
    file_type must be one of: 'sales', 'inventory', 'expenses'.
    """
    path = get_file_path(file_type)
    if not path:
        return f"Error: No Excel file found for {file_type}."
    try:
        df = pd.read_excel(path)
        # return a preview of the first 20 rows
        return f"Showing first 20 rows of {file_type} data:\n{df.head(20).to_string(index=False)}"
    except Exception as e:
        logger.error(f"Error in read_excel: {e}")
        return f"Error reading Excel: {str(e)}"

@mcp.tool
def search_uploaded_business_data(query: str) -> str:
    """
    Search all uploaded business files (sales, inventory, expenses) for matching text.
    """
    return search_business_data(query)

@mcp.tool
def create_pdf_report(health_score: int, summary: str, recommendations_json: str) -> str:
    """
    Generate a business operations PDF report.
    recommendations_json must be a JSON array of strings containing recommendation bullet points.
    """
    try:
        recs = json.loads(recommendations_json)
    except Exception:
        recs = [recommendations_json]
        
    summary_data = {
        "health_score": health_score,
        "summary": summary,
        "recommendations": recs
    }
    
    pdf_path = generate_pdf_report(summary_data)
    if pdf_path:
        return f"PDF report successfully created at: {pdf_path}"
    return "Error: Failed to create PDF report."

@mcp.tool
def create_excel_report() -> str:
    """
    Export consolidated sales, inventory, and expense data to a multi-tab Excel spreadsheet.
    """
    excel_path = export_excel_report()
    if excel_path:
        return f"Excel workbook successfully created at: {excel_path}"
    return "Error: Failed to create Excel report."

@mcp.tool
def create_chart(chart_type: str) -> str:
    """
    Generate and save a business operations chart.
    chart_type must be one of: 'sales_trend', 'expense_categories', 'inventory_levels'.
    Returns the path to the saved PNG chart.
    """
    path = generate_charts(chart_type)
    if path:
        return f"Chart successfully saved at: {path}"
    return f"Error: Failed to generate chart for type '{chart_type}'."

if __name__ == "__main__":
    logger.info("Starting BizPilot FastMCP Server...")
    mcp.run()
