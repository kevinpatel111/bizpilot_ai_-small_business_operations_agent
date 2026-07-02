# BizPilot AI - Architecture Documentation

This document explains the technical architecture, data flow, and components of the **BizPilot AI – Small Business Operations Agent** application.

---

## Architecture Design

BizPilot AI is designed around a multi-agent hierarchy built on the **Google Agent Development Kit (ADK)**. The entry point of user interaction is a modern Streamlit frontend. It relies on a local SQLite database for persistent storage (file registry, settings, and chat history) and processes files on disk.

```
+-------------------------------------------------------------------+
|                       Streamlit Frontend UI                       |
|  (Dashboard, Uploads, Chat, Sales, Inventory, Finance, Reports)    |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|                        Coordinator Agent                          |
|    - Orchestrates and dispatches requests to specialized agents   |
|    - Synthesizes composite outputs                                |
+-------------------------------------------------------------------+
                                  |
       +------------------+-------+-------+-------------------+
       |                  |               |                   |
       v                  v               v                   v
+--------------+   +--------------+   +---------+   +-----------------+
| Sales Agent  |   | Invent Agent |   | Fin Agent|   | Marketing/Support|
| - Top/Slow   |   | - Low Stock  |   | - Expense|   | - Promo Copy     |
| - Trends     |   | - Reorders   |   | - Margin |   | - Support Drafts |
+--------------+   +--------------+   +---------+   +-----------------+
       |                  |               |                   |
       +------------------+-------+-------+-------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|                      Core Tools Engine (Local)                    |
|    - Pandas calculations (business_tools.py)                      |
|    - Matplotlib static graphs and PDF compilation                 |
+-------------------------------------------------------------------+
          ^                                                   ^
          | (reads/writes)                                    | (registered tools)
          v                                                   v
+------------------------+                          +-----------------+
| Local Files & SQLite   |                          |  FastMCP Server |
|  - sales/expenses CSV  |                          |  - Read CSV/XLS |
|  - bizpilot.db         |                          |  - Expose tools |
+------------------------+                          +-----------------+
```

---

## Agent System (Google ADK)

Each agent in the `agents/` directory is defined using the ADK `Agent` constructor and run using the `InMemoryRunner`.
1.  **Coordinator Agent (`agents/coordinator.py`)**: Routes prompts and manages agent-to-agent delegation. Exposes specialized agents as tools (`analyze_sales`, `analyze_inventory`, `analyze_finance`, `draft_customer_reply`, `create_marketing_copy`, `advise_on_business`).
2.  **Specialized Agents**: 
    *   **Sales Agent**: Map queries to `get_sales_summary`.
    *   **Inventory Agent**: Map queries to `get_inventory_summary`.
    *   **Finance Agent**: Map queries to `get_finance_summary`.
    *   **Customer Support Agent**: Map queries to `get_inventory_summary` (availability check).
    *   **Marketing Agent**: Map queries to `get_sales_summary` (slow-product check).
    *   **Business Advisor Agent**: Synthesizes the overall business performance.

---

## Data & Tools Engine

The `tools/` folder acts as the core business logic.
-   `business_tools.py`: Uses Pandas for loading, filtering, and performing metrics calculations on `.csv` or `.xlsx` files. Includes standard fallbacks to default files in the `data/` directory.
-   `reporting_tools.py`: Compiles reports:
    *   **PDF Performance Report**: Uses `fpdf2` to build a branded PDF containing executive summaries, KPI tables, and recommendations.
    *   **Excel Export**: Consolidates separate CSV/Excel files into a multi-tab Excel spreadsheet (`openpyxl` engine).
    *   **Matplotlib Charts**: Generates static line, pie, and bar charts for reporting engines.

---

## Model Context Protocol (MCP) Server

The MCP Server (`mcp/server.py`) is built using the high-level **FastMCP** framework.
-   Allows external agents or model clients to execute operations on BizPilot AI data using standard Model Context Protocol.
-   Exposes 6 standard tools: `read_csv`, `read_excel`, `search_uploaded_business_data`, `create_pdf_report`, `create_excel_report`, `create_chart`.
-   Supports standard transports (stdio and HTTP).
