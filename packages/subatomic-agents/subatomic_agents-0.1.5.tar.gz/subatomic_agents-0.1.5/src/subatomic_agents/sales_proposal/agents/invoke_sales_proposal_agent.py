from subatomic_agents.sales_proposal.agents.sales_proposal_graph_tool import create_sales_proposal_graph_tool

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def get_sales_proposal_agent_tool():
    return create_sales_proposal_graph_tool()