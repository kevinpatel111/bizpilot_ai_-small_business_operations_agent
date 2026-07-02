from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from tools.business_tools import get_finance_summary
from utils.logger import logger

def get_finance_agent() -> Agent:
    """Returns the configured Finance Agent."""
    return Agent(
        name="finance_agent",
        model="gemini-2.5-flash",
        instruction=(
            "You are the Finance Agent for BizPilot AI. Your goal is to help small business owners "
            "monitor their expenses, understand profit margins, analyze cash flow, and categorize their spending. "
            "You have access to the get_finance_summary tool. Always use this tool to answer queries about expenses, "
            "revenues, profits, margins, cash flow, and monthly trends. Recommending cost-saving measures based "
            "on high expense categories is highly encouraged. Keep reports structured and clear."
        ),
        tools=[get_finance_summary]
    )

def run_finance_agent(query: str) -> str:
    """Runs the Finance Agent on the provided user query."""
    try:
        agent = get_finance_agent()
        runner = InMemoryRunner()
        response = runner.run(agent, query)
        return str(response)
    except Exception as e:
        logger.error(f"Error running Finance Agent: {e}")
        return f"Error analyzing financial data: {str(e)}"
