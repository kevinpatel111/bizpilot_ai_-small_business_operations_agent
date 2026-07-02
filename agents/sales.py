from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from tools.business_tools import get_sales_summary
from utils.logger import logger
import os

def get_sales_agent() -> Agent:
    """Returns the configured Sales Analysis Agent."""
    return Agent(
        name="sales_agent",
        model="gemini-2.5-flash",
        instruction=(
            "You are the Sales Analysis Agent for BizPilot AI. Your goal is to help small business owners "
            "understand their sales performance, identify top products, highlight slow-moving products, "
            "and spot revenue trends. You have access to the get_sales_summary tool to fetch the latest "
            "sales numbers. Always use this tool when answering questions about sales, revenue, top products, "
            "or sales trends. Format your response clearly using bullet points and tables where appropriate."
        ),
        tools=[get_sales_summary]
    )

def run_sales_agent(query: str) -> str:
    """Runs the Sales Agent on the provided user query and returns the response."""
    try:
        agent = get_sales_agent()
        runner = InMemoryRunner()
        response = runner.run(agent, query)
        # response is usually a string, or has a .text / .content property. We'll stringify it safely.
        return str(response)
    except Exception as e:
        logger.error(f"Error running Sales Agent: {e}")
        return f"Error analyzing sales data: {str(e)}"
