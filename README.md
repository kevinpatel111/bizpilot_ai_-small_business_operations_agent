# BizPilot AI - Small Business Operations Agent

BizPilot AI is a production-ready multi-agent business operations and analytics application. Powered by Google's Agent Development Kit (ADK), Gemini 2.5 Flash, FastMCP, SQLite, and Streamlit, it helps small business owners analyze sales records, monitor stock levels, categorize expenses, and receive proactive operational recommendations.

---

## Key Features

1.  **Coordinator Agent (ADK Orchestration)**: Central director that interprets user requests, dispatches them to specialized agents, and merges responses.
2.  **Specialized Agents**:
    *   **Sales Analysis Agent**: Identifies top products, slow-moving items, and revenue growth.
    *   **Inventory Agent**: Provides low stock/overstock warnings and reorder recommendations.
    *   **Finance Agent**: Details net profits, margins, and groups expenses.
    *   **Customer Support Agent**: Generates customer response drafts and checks stock levels.
    *   **Marketing Agent**: Suggests campaigns, social media posts, and WhatsApp copy.
    *   **Business Advisor Agent**: Synthesizes the overall business health, risks, and next steps.
3.  **Operations Dashboard**: High-level visual widgets showing total revenue, profit margins, active low-stock flags, and expense charts.
4.  **CSV/Excel Drag-and-Drop Uploads**: Integrated size limit (10MB) and strict column schema validations.
5.  **Model Context Protocol (MCP) Server**: Exposes data ingestion, search, charting, and PDF/Excel generation tools for external agentic integrations.
6.  **Secured Access**: Password-locked login system.

---

## Code Structure

```
.
├── agents/             # Google ADK agent configurations and runner functions
├── database/           # SQLite database setup and query modules
├── tools/              # Core business calculations, PDF reports, and Excel sheets
├── mcp/                # FastMCP server registration and setup
├── frontend/           # Streamlit view pages and styling components
├── utils/              # Security validations, logging, and passwords
├── data/               # Sample and uploaded business CSV data files
├── docs/               # Architecture diagrams and deep dives
├── requirements.txt    # Application dependencies
└── app.py              # Main Streamlit app entry point
```

---

## Local Setup Instructions

### 1. Prerequisites
- Python 3.10+
- A Google Gemini API Key

### 2. Install Dependencies
Clone the repository, initialize a virtual environment, and install the libraries:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Setup Configurations
Copy the `.env` template and add your credentials:
```env
# Google Gemini API Key
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Security Password for Streamlit Login
ADMIN_PASSWORD=admin123

# Database configuration
DB_PATH=database/bizpilot.db
```

### 4. Running the Dashboard
Launch the Streamlit app locally:
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser and enter the password (default: `admin123`).

### 5. Running the MCP Server
Run the FastMCP server locally in stdio transport mode:
```bash
python mcp/server.py
```
Or run as a local HTTP transport endpoint:
```bash
fastmcp run mcp/server.py:mcp --transport http --port 8000
```

---

## Docker Deployment

You can build and deploy the entire stack using Docker Compose:

1.  Add your `GEMINI_API_KEY` to the local `.env` file.
2.  Start the services:
    ```bash
    docker-compose up --build
    ```
This launches:
-   **Streamlit frontend** at `http://localhost:8501`
-   **FastMCP HTTP Server** at `http://localhost:8000`

---

## License
MIT License. See [LICENSE](LICENSE) for details.
