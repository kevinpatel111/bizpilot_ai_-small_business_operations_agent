import os
import pandas as pd
from typing import Dict, Any, List, Optional
from database.db import get_registered_files
from utils.logger import logger

def get_file_path(file_type: str) -> Optional[str]:
    """Get the path of the registered file, or fallback to sample data in data/ folder."""
    files = get_registered_files()
    if file_type in files:
        path = files[file_type]["filepath"]
        if os.path.exists(path):
            return path
            
    # Fallback to sample data directory
    fallback_path = os.path.join("data", f"{file_type}.csv")
    if os.path.exists(fallback_path):
        return fallback_path
        
    return None

def load_data(file_type: str) -> Optional[pd.DataFrame]:
    """Load the business data file as a Pandas DataFrame."""
    path = get_file_path(file_type)
    if not path:
        logger.info(f"No file found for type {file_type}")
        return None
        
    try:
        _, ext = os.path.splitext(path.lower())
        if ext == ".csv":
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)
            
        # Standardize column headers (lowercase, stripped whitespace)
        df.columns = [col.strip().lower() for col in df.columns]
        return df
    except Exception as e:
        logger.error(f"Error loading {file_type} data from {path}: {e}")
        return None

def search_business_data(query: str) -> str:
    """
    Search across all uploaded business files (sales, inventory, expenses) 
    for rows matching the query keyword.
    """
    results = []
    for file_type in ["sales", "inventory", "expenses"]:
        df = load_data(file_type)
        if df is not None:
            # Simple case-insensitive match on all string columns
            mask = df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)
            matched_df = df[mask]
            if not matched_df.empty:
                results.append(f"--- MATCHES IN {file_type.upper()} DATA ({len(matched_df)} rows) ---")
                results.append(matched_df.head(10).to_string(index=False))
                results.append("\n")
                
    if not results:
        return f"No results found for query '{query}'."
    return "\n".join(results)

# Sales Analysis Functions
def get_sales_summary() -> Dict[str, Any]:
    """Generate sales analytics metrics and summary."""
    df = load_data("sales")
    if df is None or df.empty:
        return {"status": "error", "message": "No sales data available. Please upload a sales report."}
        
    try:
        # Expected columns: date, product, quantity, amount
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
        
        # Convert date
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
        
        total_revenue = df["amount"].sum()
        total_items_sold = df["quantity"].sum()
        
        # Top products
        top_products = df.groupby("product")["amount"].sum().reset_index()
        top_products = top_products.sort_values(by="amount", ascending=False).head(5).to_dict(orient="records")
        
        # Product sales counts
        product_counts = df.groupby("product")["quantity"].sum().reset_index()
        
        # Slow-moving products (bottom 5 items based on items sold)
        slow_products = product_counts.sort_values(by="quantity", ascending=True).head(5).to_dict(orient="records")
        
        # Monthly trends
        df["month_yr"] = df["date"].dt.to_period("M")
        monthly_sales = df.groupby("month_yr")["amount"].sum().reset_index()
        monthly_sales["month_yr"] = monthly_sales["month_yr"].astype(str)
        monthly_trends = monthly_sales.to_dict(orient="records")
        
        return {
            "status": "success",
            "total_revenue": float(total_revenue),
            "total_items_sold": int(total_items_sold),
            "top_products": top_products,
            "slow_moving_products": slow_products,
            "monthly_trends": monthly_trends,
            "records_count": len(df)
        }
    except Exception as e:
        logger.error(f"Error in get_sales_summary: {e}")
        return {"status": "error", "message": f"Failed to compute sales analytics: {str(e)}"}

# Inventory Functions
def get_inventory_summary() -> Dict[str, Any]:
    """Generate inventory status, alerts, and recommendations."""
    df = load_data("inventory")
    if df is None or df.empty:
        return {"status": "error", "message": "No inventory data available. Please upload inventory records."}
        
    try:
        # Expected columns: product, stocklevel, reorderlevel, unitcost
        df["stocklevel"] = pd.to_numeric(df["stocklevel"], errors="coerce").fillna(0)
        df["reorderlevel"] = pd.to_numeric(df["reorderlevel"], errors="coerce").fillna(0)
        df["unitcost"] = pd.to_numeric(df["unitcost"], errors="coerce").fillna(0)
        
        # Calculations
        df["valuation"] = df["stocklevel"] * df["unitcost"]
        total_valuation = df["valuation"].sum()
        total_items = df["stocklevel"].sum()
        
        # Low Stock (Stock <= ReorderLevel)
        low_stock_df = df[df["stocklevel"] <= df["reorderlevel"]]
        low_stock = low_stock_df.to_dict(orient="records")
        
        # Overstock (Stock > ReorderLevel * 4 or hard threshold)
        overstock_df = df[df["stocklevel"] > df["reorderlevel"] * 3]
        overstock = overstock_df.to_dict(orient="records")
        
        # Restock recommendations
        recommendations = []
        for idx, row in low_stock_df.iterrows():
            # Reorder amount to reach 2x the reorder level or a safety threshold
            reorder_qty = int((row["reorderlevel"] * 2) - row["stocklevel"])
            if reorder_qty <= 0:
                reorder_qty = int(row["reorderlevel"] + 10)
                
            cost = reorder_qty * row["unitcost"]
            recommendations.append({
                "product": row["product"],
                "current_stock": int(row["stocklevel"]),
                "reorder_level": int(row["reorderlevel"]),
                "suggested_reorder_qty": reorder_qty,
                "estimated_cost": float(cost)
            })
            
        return {
            "status": "success",
            "total_valuation": float(total_valuation),
            "total_items": int(total_items),
            "low_stock_items": low_stock,
            "overstock_items": overstock,
            "restock_recommendations": recommendations,
            "records_count": len(df)
        }
    except Exception as e:
        logger.error(f"Error in get_inventory_summary: {e}")
        return {"status": "error", "message": f"Failed to analyze inventory: {str(e)}"}

# Finance Functions
def get_finance_summary() -> Dict[str, Any]:
    """Generate financial metrics, expenses, and cash flow summary."""
    expenses_df = load_data("expenses")
    sales_df = load_data("sales")
    
    if expenses_df is None or expenses_df.empty:
        return {"status": "error", "message": "No expense data available. Please upload expenses."}
        
    try:
        # Expected columns in expenses: date, category, amount, description
        expenses_df["amount"] = pd.to_numeric(expenses_df["amount"], errors="coerce").fillna(0)
        expenses_df["date"] = pd.to_datetime(expenses_df["date"], errors="coerce")
        expenses_df = expenses_df.dropna(subset=["date"])
        
        total_expenses = expenses_df["amount"].sum()
        
        # Expense categorization
        expense_by_cat = expenses_df.groupby("category")["amount"].sum().reset_index()
        expense_by_cat = expense_by_cat.sort_values(by="amount", ascending=False).to_dict(orient="records")
        
        # Revenue from sales
        total_revenue = 0
        if sales_df is not None and not sales_df.empty:
            sales_df["amount"] = pd.to_numeric(sales_df["amount"], errors="coerce").fillna(0)
            total_revenue = sales_df["amount"].sum()
            
        net_profit = total_revenue - total_expenses
        profit_margin = (net_profit / total_revenue) * 100 if total_revenue > 0 else 0
        
        # Monthly trends
        expenses_df["month_yr"] = expenses_df["date"].dt.to_period("M")
        monthly_exp = expenses_df.groupby("month_yr")["amount"].sum().reset_index()
        monthly_exp["month_yr"] = monthly_exp["month_yr"].astype(str)
        monthly_expenses = monthly_exp.to_dict(orient="records")
        
        return {
            "status": "success",
            "total_expenses": float(total_expenses),
            "total_revenue": float(total_revenue),
            "net_profit": float(net_profit),
            "profit_margin": float(profit_margin),
            "expenses_by_category": expense_by_cat,
            "monthly_expenses": monthly_expenses,
            "records_count": len(expenses_df)
        }
    except Exception as e:
        logger.error(f"Error in get_finance_summary: {e}")
        return {"status": "error", "message": f"Failed to compute finance summary: {str(e)}"}
