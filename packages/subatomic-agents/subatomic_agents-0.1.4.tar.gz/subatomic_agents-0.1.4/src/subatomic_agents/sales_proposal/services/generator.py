from typing import Tuple, Dict, Any

from sales_proposal.models.input_schema import SalesProposalInput
from sales_proposal.factories.config_factory import SalesProposalConfigFactory
from sales_proposal.agents.invoke_sales_proposal_agent import get_sales_proposal_agent_tool

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

class SalesProposalGeneratorService:
    def __init__(self, input_data: SalesProposalInput):
        self.input_data = input_data
        self.config_factory = SalesProposalConfigFactory(prompt_config_keys=[
            "subatomic_elicit_docs",
            "subatomic_generate_meeting_transcript_analysis",
            "subatomic_generate_sales_proposal_cover_page",
            "subatomic_generate_sales_proposal_structure",
            "subatomic_generate_statement_of_work",
            "subatomic_generate_background",
            "subatomic_generate_scope",
            "subatomic_generate_project_assumptions",
            "subatomic_generate_pricing",
            "subatomic_generate_timeline",
            "subatomic_generate_signatures"
        ])

    def generate(self):
        try:
            agent = get_sales_proposal_agent_tool()
            config = self.config_factory.create_config()

            result = agent.invoke(self.input_data.model_dump(), config)

            filtered_result = {
                key: value for key, value in result.items()
                if key not in ['vector_store', 'meeting_transcript_vector_store']
            }

            self.config_factory.cleanup(config)

            print("AGENT RESPONSE: Sales proposal generated successfully.")
            return filtered_result

        except Exception as e:
            print(f"Sales proposal generation error: {e}")
            return {"error": str(e)}
