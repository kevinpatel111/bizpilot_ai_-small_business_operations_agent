from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from tools.business_tools import get_inventory_summary
from utils.logger import logger

def get_support_agent() -> Agent:
    """Returns the configured Customer Support Agent."""
    return Agent(
        name="support_agent",
        model="gemini-2.5-flash",
        instruction=(
            "You are the Customer Support Agent for BizPilot AI. Your goal is to draft professional, "
            "empathetic, and helpful customer support replies. You can address refund policies, return procedures, "
            "complaint summaries, and product availability. You have access to the get_inventory_summary tool "
            "to check product availability and stock levels. If a customer asks if a product is in stock, always "
            "verify it using this tool before replying. Structure drafts clearly and mark placeholder values "
            "(like customer name, dates, etc.) with brackets [like this] so the user can edit them."
        ),
        tools=[get_inventory_summary]
    )

def run_support_agent(query: str) -> str:
    """Runs the Customer Support Agent on the provided user query."""
    try:
        agent = get_support_agent()
        runner = InMemoryRunner()
        response = runner.run(agent, query)
        return str(response)
    except Exception as e:
        logger.error(f"Error running Support Agent: {e}")
        return f"Error drafting customer support reply: {str(e)}"
