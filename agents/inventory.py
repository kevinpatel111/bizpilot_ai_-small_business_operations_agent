from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from tools.business_tools import get_inventory_summary
from utils.logger import logger

def get_inventory_agent() -> Agent:
    """Returns the configured Inventory Agent."""
    return Agent(
        name="inventory_agent",
        model="gemini-2.5-flash",
        instruction=(
            "You are the Inventory Management Agent for BizPilot AI. Your goal is to help small business owners "
            "track stock levels, detect low stock items or overstocked items, estimate current inventory valuation, "
            "and suggest restock amounts (and costs). You have access to the get_inventory_summary tool. "
            "Always use this tool when answering questions about stock, reordering, valuation, low stock alerts, "
            "or inventory health. Format your suggestions cleanly as a list or a table."
        ),
        tools=[get_inventory_summary]
    )

def run_inventory_agent(query: str) -> str:
    """Runs the Inventory Agent on the provided user query."""
    try:
        agent = get_inventory_agent()
        runner = InMemoryRunner()
        response = runner.run(agent, query)
        return str(response)
    except Exception as e:
        logger.error(f"Error running Inventory Agent: {e}")
        return f"Error analyzing inventory data: {str(e)}"
