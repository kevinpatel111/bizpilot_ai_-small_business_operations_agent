from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from tools.business_tools import get_sales_summary, get_inventory_summary, get_finance_summary
from utils.logger import logger

def get_advisor_agent() -> Agent:
    """Returns the configured Business Advisor Agent."""
    return Agent(
        name="advisor_agent",
        model="gemini-2.5-flash",
        instruction=(
            "You are the Business Advisor Agent for BizPilot AI. Your goal is to synthesize the overall health "
            "of a small business by analyzing its sales, inventory, and financial summaries. You have access to "
            "get_sales_summary, get_inventory_summary, and get_finance_summary tools. Always call all three tools "
            "to understand the complete picture of the business before formulating your advice. "
            "You must output: "
            "1. A Business Health Score (an integer from 0 to 100 based on revenue, inventory turnover/alerts, and net margin). "
            "2. Top Risks (e.g., low stock products, falling revenue, high expenses). "
            "3. Top Opportunities (e.g., promotional possibilities, restock high-yield products). "
            "4. A structured Action Plan. "
            "5. Core Weekly Recommendations. "
            "Structure your response clearly with headers and bullet points. Make it sound professional and actionable."
        ),
        tools=[get_sales_summary, get_inventory_summary, get_finance_summary]
    )

def run_advisor_agent(query: str) -> str:
    """Runs the Business Advisor Agent on the provided query."""
    try:
        agent = get_advisor_agent()
        runner = InMemoryRunner()
        response = runner.run(agent, query)
        return str(response)
    except Exception as e:
        logger.error(f"Error running Advisor Agent: {e}")
        return f"Error analyzing business health: {str(e)}"
