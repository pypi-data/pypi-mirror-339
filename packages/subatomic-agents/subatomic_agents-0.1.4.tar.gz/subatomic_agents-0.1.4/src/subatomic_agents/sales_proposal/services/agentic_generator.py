import os
from typing import List
from uuid import uuid4
from helpers.outputs.general_outputs import html_to_pdf
from helpers.outputs.sales_proposal_outputs import generate_full_sales_proposal_with_css
from react_agent_architecture.react_agent_architecture import (
    AgentOrchestrator, 
    SalesProposalAgentBuilder, 
    SalesProposalToolset
)
from sales_proposal.models.input_schema import SalesProposalInput
from sales_proposal.services.generator import SalesProposalGeneratorService
from pathlib import Path
from pdf2docx import parse
from langchain_core.tools import tool

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
css_file_path = os.path.join(BASE_DIR, "..", "..", "static", "css_for_pdf_formats", "sales_proposal.css")

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def get_project_root() -> Path:
    current_path = Path.cwd()
    for parent in [current_path] + list(current_path.parents):
        if any((parent / marker).exists() for marker in ["pyproject.toml", "requirements.txt", ".git"]):
            return parent
    return current_path 

@tool
def sales_proposal_tool(
    meeting_summary_urls: List[str],
    meeting_summary_file_types: List[str],
    meeting_transcript_url: str,
    meeting_transcript_file_type: str
):
    """
    Use this tool for generating a Sales Proposal
    """
    try:
        input_data = SalesProposalInput(
            meeting_summary_urls=meeting_summary_urls,
            meeting_summary_file_types=meeting_summary_file_types,
            meeting_transcript_url=meeting_transcript_url,
            meeting_transcript_file_type=meeting_transcript_file_type
        )
        print("✅ SalesProposalInput successfully created.")
    except Exception as e:
        print(f"❌ Error creating SalesProposalInput: {e}")

    try:
        sales_proposal_generator_service = SalesProposalGeneratorService(
            input_data=input_data
        )
        print("✅ SalesProposalGeneratorService successfully instantiated.")
    except Exception as e:
        print(f"❌ Error instantiating SalesProposalGeneratorService: {e}")

    try:
        results = sales_proposal_generator_service.generate()
        print("✅ Sales proposal generated.")
    except Exception as e:
        print(f"❌ Error generating sales proposal: {e}")

    try:
        full_html_content = generate_full_sales_proposal_with_css(results, css_file_path)
        print("✅ Full HTML content with CSS generated.")
    except Exception as e:
        print(f"❌ Error generating full HTML content with CSS: {e}")

    try:
        pdf_stream = html_to_pdf(full_html_content)
        print("✅ PDF stream generated.")
    except Exception as e:
        print(f"❌ Error converting HTML to PDF: {e}")

    try:
        unique_id = str(uuid4())
        project_root = get_project_root()
        
        pdf_path = project_root / f"sales_proposal_{unique_id}.pdf"
        with open(pdf_path, "wb") as f:
            if hasattr(pdf_stream, "read"):
                f.write(pdf_stream.read())
            else:
                f.write(pdf_stream)
        print(f"✅ PDF written to {pdf_path}")
    except Exception as e:
        print(f"❌ Error writing PDF file: {e}")

    try:
        temp_filename_docx = f"sales_proposal_{unique_id}.docx"
        docx_file = project_root / temp_filename_docx

        parse(pdf_path, docx_file)
        print(f"✅ DOCX file generated at {docx_file}")
    except Exception as e:
        print(f"❌ Error generating DOCX file: {e}")

    print("🎉 The Sales Proposal was successfully generated.")
    return f"The Sales Proposal was successfully generated"

def sales_proposal_agentic_generator(
    query: str
):
    tools = [sales_proposal_tool]

    toolset = SalesProposalToolset(tools)
    builder = SalesProposalAgentBuilder(toolset)
    orchestrator = AgentOrchestrator(builder)

    result = orchestrator.run(query)

    return result