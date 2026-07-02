from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from tools.business_tools import get_sales_summary
from utils.logger import logger

def get_marketing_agent() -> Agent:
    """Returns the configured Marketing Agent."""
    return Agent(
        name="marketing_agent",
        model="gemini-2.5-flash",
        instruction=(
            "You are the Marketing Agent for BizPilot AI. Your goal is to help small business owners "
            "develop promotional campaigns, write social media posts, and design WhatsApp marketing messages. "
            "You have access to the get_sales_summary tool. If the user asks for promotional campaigns for slow-moving "
            "items, first query get_sales_summary to identify those items and then write custom-tailored campaign "
            "ideas (such as buy-one-get-one, specific discount % recommendations). Write copy that is engaging, "
            "includes emojis, and provides call-to-actions."
        ),
        tools=[get_sales_summary]
    )

def run_marketing_agent(query: str) -> str:
    """Runs the Marketing Agent on the provided user query."""
    try:
        agent = get_marketing_agent()
        runner = InMemoryRunner()
        response = runner.run(agent, query)
        return str(response)
    except Exception as e:
        logger.error(f"Error running Marketing Agent: {e}")
        return f"Error creating marketing copy: {str(e)}"
