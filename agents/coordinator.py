from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from agents.sales import run_sales_agent
from agents.inventory import run_inventory_agent
from agents.finance import run_finance_agent
from agents.support import run_support_agent
from agents.marketing import run_marketing_agent
from agents.advisor import run_advisor_agent
from utils.logger import logger

# Declare the delegator functions to be used as tools
def analyze_sales(query: str) -> str:
    """Useful when you need to analyze sales performance, trends, or product sales numbers."""
    logger.info(f"Coordinator delegating to Sales Agent with query: {query}")
    return run_sales_agent(query)

def analyze_inventory(query: str) -> str:
    """Useful when you need to check stock levels, reorder quantities, low stock alerts, or overstock items."""
    logger.info(f"Coordinator delegating to Inventory Agent with query: {query}")
    return run_inventory_agent(query)

def analyze_finance(query: str) -> str:
    """Useful when you need to analyze expenses, profits, profit margins, or cash flow records."""
    logger.info(f"Coordinator delegating to Finance Agent with query: {query}")
    return run_finance_agent(query)

def draft_customer_reply(query: str) -> str:
    """Useful when you need to draft replies to customer questions, product availability inquiries, returns, or refunds."""
    logger.info(f"Coordinator delegating to Support Agent with query: {query}")
    return run_support_agent(query)

def create_marketing_copy(query: str) -> str:
    """Useful when you need to suggest marketing campaigns, promotions, social media posts, or WhatsApp messages."""
    logger.info(f"Coordinator delegating to Marketing Agent with query: {query}")
    return run_marketing_agent(query)

def advise_on_business(query: str) -> str:
    """Useful when you need an overall business health analysis, business health score, risks, opportunities, or a weekly action plan."""
    logger.info(f"Coordinator delegating to Business Advisor Agent with query: {query}")
    return run_advisor_agent(query)

def get_coordinator_agent() -> Agent:
    """Returns the configured Coordinator Agent."""
    return Agent(
        name="coordinator_agent",
        model="gemini-2.5-flash",
        instruction=(
            "You are the central Coordinator Agent for BizPilot AI. Your job is to understand the user's request "
            "and delegate the tasks to the appropriate specialized agents by calling their corresponding tools. "
            "You have access to: "
            "- analyze_sales (delegates to Sales Agent) "
            "- analyze_inventory (delegates to Inventory Agent) "
            "- analyze_finance (delegates to Finance Agent) "
            "- draft_customer_reply (delegates to Customer Support Agent) "
            "- create_marketing_copy (delegates to Marketing Agent) "
            "- advise_on_business (delegates to Business Advisor Agent) "
            "If a query requires multiple agents (e.g., both sales and inventory), call both tools and synthesize "
            "their outputs into a cohesive final response. Be friendly, helpful, and direct your responses to the business owner."
        ),
        tools=[
            analyze_sales,
            analyze_inventory,
            analyze_finance,
            draft_customer_reply,
            create_marketing_copy,
            advise_on_business
        ]
    )

def run_coordinator_agent(query: str) -> str:
    """Runs the Coordinator Agent on the user query."""
    try:
        agent = get_coordinator_agent()
        runner = InMemoryRunner()
        response = runner.run(agent, query)
        return str(response)
    except Exception as e:
        logger.error(f"Error running Coordinator Agent: {e}")
        return f"Error executing request: {str(e)}"
