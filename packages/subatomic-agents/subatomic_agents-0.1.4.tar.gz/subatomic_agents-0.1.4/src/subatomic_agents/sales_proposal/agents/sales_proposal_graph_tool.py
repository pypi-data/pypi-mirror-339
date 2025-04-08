from typing import TypedDict, Optional, Any, List
from pydantic import BaseModel, Field, field_validator
from langchain_core.runnables import RunnableConfig

from langchain_core.output_parsers import JsonOutputParser
import json
import re

import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from helpers.document_loaders import get_docs
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langgraph.graph import StateGraph, END

from langchain.tools.retriever import create_retriever_tool
from langgraph.prebuilt import create_react_agent

import os
from langchain_core.tools import tool
from datetime import date

from helpers.helper_react_agents import (
    compile_react_agent, 
    create_retriever_tool_func, 
    generate_agentic_rag_responses
)
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

model = ChatOpenAI(model=os.getenv('OPENAI_MODEL'), temperature=0.7)

class MeetingTranscriptAnalysisRetrievedChunks(BaseModel):
    use_cases_chunks: List[str] = Field(..., description="The Use Cases chunks for the Meeting Transcript Analysis.")
    expected_value_chunks: List[str] = Field(..., description="The Expected Value chunks for the Meeting Transcript Analysis.")
    agents_chunks: List[str] = Field(..., description="The Agents chunks for the Meeting Transcript Analysis.")

class GenerateSalesProposalStructureChunks(BaseModel):
    sales_proposal_sow_chunks: List[str] = Field(
        ..., 
        description="The defined scope of work for the project, including key deliverables, milestones, and responsibilities of each party involved."
    )
    sales_proposal_background_chunks: List[str] = Field(
        ..., 
        description="The client’s current context, including key challenges, goals, and industry positioning, providing relevant insights for the proposed solution."
    )
    sales_proposal_scope_chunks: List[str] = Field(
        ..., 
        description="The proposed solutions to address the client’s needs, detailing specific objectives, methodologies, and expected outcomes."
    )
    sales_proposal_assumptions_chunks: List[str] = Field(
        ..., 
        description="The key assumptions impacting the project, including dependencies, constraints, and conditions necessary for successful execution."
    )
    sales_proposal_pricing_chunks: List[str] = Field(
        ..., 
        description="The pricing structure of the project, including a breakdown of costs, packages, tiers, or customization options that add value to the proposal."
    )
    sales_proposal_timeline_chunks: List[str] = Field(
        ..., 
        description="The proposed project timeline, including major phases, key milestones, and expected completion dates."
    )
    sales_proposal_signatures_chunks: List[str] = Field(
        ..., 
        description="The authorized signatories for the proposal, including formal details required for agreement and approval."
    )

class UseCase(BaseModel):
    """Schema for representing a highlighted use case from the meeting."""
    name: str = Field(..., description="The name of the use case discussed in the meeting.")
    description: str = Field(..., description="A brief explanation of what the use case entails.")
    client_interest_level: str = Field(..., description="How interested the client is in this use case (e.g., High, Medium, Low).")
    business_pain_point: str = Field(..., description="The specific business problem that this use case aims to address.")
    industry_relevance: str = Field(..., description="The industry or sector where this use case is most applicable (e.g., Finance, Healthcare, Manufacturing).")
    existing_solutions: List[str] = Field(..., description="Current solutions or approaches the client is using to address this use case.")

class ExpectedOutcome(BaseModel):
    """Schema for representing the expected value from AI implementation for each use case."""
    use_case_name: str = Field(..., description="The name of the use case this outcome is associated with.")
    ai_impact_summary: str = Field(..., description="A concise summary of how AI will impact this use case.")
    measurable_metrics: List[str] = Field(..., description="Key performance indicators (KPIs) that will measure AI's success (e.g., Cost reduction, Efficiency increase).")
    projected_roi: str = Field(..., description="The estimated return on investment from implementing AI (e.g., High, Medium, Low).")
    implementation_timeline: str = Field(..., description="The expected duration for implementing and seeing results from AI (e.g., Short-term, Mid-term, Long-term).")
    risk_factors: List[str] = Field(..., description="Potential risks or challenges associated with implementing AI for this use case.")

class SubatomicSolution(BaseModel):
    """Schema for representing Subatomic's AI-driven solution to the use case."""
    use_case_name: str = Field(..., description="The name of the use case being addressed.")
    ai_co_worker_agents_involved: List[str] = Field(..., description="The specific AI Co-worker Agents that will be used to solve this use case.")
    solution_workflow: str = Field(..., description="A step-by-step outline of how Subatomic will solve the use case using AI.")
    key_technologies_used: List[str] = Field(..., description="The core technologies, frameworks, or AI models involved in the solution.")
    expected_delivery_timeframe: str = Field(..., description="The estimated time required to deliver a working solution (e.g., 2 weeks, 3 months).")
    potential_challenges: List[str] = Field(..., description="Possible obstacles that might arise during implementation and delivery.")

class MeetingTranscriptAnalysis(BaseModel):
    """Schema for unifying all extracted insights from the meeting transcript."""
    client_name: str = Field(..., description="The client's name")
    use_cases: List[UseCase] = Field(..., description="A list of the most relevant use cases discussed in the meeting.")
    expected_outcomes: List[ExpectedOutcome] = Field(..., description="A detailed breakdown of the expected value AI will bring to each use case.")
    subatomic_solutions: List[SubatomicSolution] = Field(..., description="Subatomic’s approach to solving and delivering results using AI Co-worker Agents.")

# Main schemas
class SalesProposalCoverPage(BaseModel):
    company_name: str = Field(..., description="The name of the company issuing the proposal")
    title: str = Field(..., description="The title of the proposal")
    dated: date = Field(..., description="The date of the proposal")
    proposal_purpose: str = Field(..., description="The purpose or subtitle of the proposal")
    subtitle: str = Field(..., description="A brief descriptive phrase summarizing the project")

class SalesProposalSection(BaseModel):
    section_name: str = Field(..., description="Name of the section")
    section_important_information: list[str] = Field(..., description="Important information about the section that must be used for the Sales Proposal")

class SalesProposalStructure(BaseModel):
    main_aim: str = Field(..., description="The main aim of the Sales Proposal")
    sales_proposal_sections: List[SalesProposalSection] = Field(..., description="List of Sales Proposal Sections")

#Statement of Work (SOW)
class SOWSchema(BaseModel):
    dated: date = Field(..., description="Date when the SOW is drafted")
    service_provider: str = Field(..., description="Name of the service provider entity")
    service_provider_dba: Optional[str] = Field(None, description="Doing Business As name for the service provider")
    customer: str = Field(..., description="Name of the customer entity")
    msa_date: date = Field(..., description="Date of the Master Services Agreement")
    msa_terms: str = Field(..., description="Textual description of the SOW being governed by the MSA terms")

#Background
class BackgroundSchema(BaseModel):
    problem_statement: str = Field(..., description="A brief description of the problem being addressed")
    company_description: str = Field(..., description="Description of the company, its history, and its services (minimum 1 paragraph)")
    problem_details: str = Field(..., description="Detailed explanation of the problem and its impact (minimum 1 paragraph)")

    # Validators to ensure company_description and problem_details are at least 1 paragraph long
    @field_validator("company_description", "problem_details")
    def must_be_paragraph(cls, value):
        if len(value.split("\n")) < 1 or len(value.strip()) < 100:  # At least ~100 characters as a basic paragraph
            raise ValueError("Field must be at least one paragraph long (minimum ~100 characters)")
        return value
    
#Scope    
class SolutionProposalListingItem(BaseModel):
    title: str = Field(..., description="Title of the first listing item")
    bullet_points: List[str] = Field(..., description="List of bullet points under the item")
    summary: str = Field(..., description="Summary or conclusion for the item")

class Section(BaseModel):
    title: str = Field(..., description="Title of the section")
    description: Optional[str] = Field(None, description="Description or overview of the section")
    items: List[str] = Field(..., min_items=1, description="List of items under the section (must contain at least one item)")

class SalesProposalScope(BaseModel):
    subtitle: Optional[str] = Field(None, description="Subtitle of the scope")
    description: str = Field(..., description="High-level description of the solution's scope")
    solution_listing: List[SolutionProposalListingItem] = Field(..., description="Details of how the solution addresses the problem")
    sections: List[Section] = Field(..., description="Additional sections describing long-term value, benefits, and features")

#Project Assumptions
class AssumptionItem(BaseModel):
    number: int = Field(..., description="The numbered order of the assumption")
    description: str = Field(..., description="Detailed description of the assumption")

class ProjectAssumptionsSchema(BaseModel):
    assumptions: List[AssumptionItem] = Field(..., description="List of assumptions included in the section")

#Pricing
class PricingOption(BaseModel):
    category: str = Field(..., description="Category of the pricing (e.g., Standard Pricing or TKO Miller Pricing)")
    annual_fees: str = Field(..., description="Description of annual fees (e.g., 'Tiered', 'Custom', or '$')")
    one_time_fees: str = Field(..., description="Description of one-time fees (e.g., 'Custom', or '$')")

class Assumption(BaseModel):
    number: int = Field(..., description="Number of the assumption")
    description: str = Field(..., description="Detailed description of the assumption")

class NestedSubitem(BaseModel):
    subtitle: str = Field(..., description="Subtitle of the nested subitem")
    description: str = Field(None, description="Description of the nested subitem")
    subitems: Optional[List[str]] = Field(None, description="Optional list of further nested subitems")

class PaymentTerm(BaseModel):
    description: str = Field(..., description="Details about the payment term")
    subitems: List[NestedSubitem] = Field(
        ...,
        description="List of additional subitems or details, supporting nested levels of bullet points",
    )

class PricingSchema(BaseModel):
    pricing_description: str = Field(None, description="Description of the pricing section")
    pricing_table: List[PricingOption] = Field(..., description="List of pricing options")
    
    assumptions: List[Assumption] = Field(..., description="List of assumptions")
    
    terms_description: str = Field(None, description="Description or overview of the terms section")
    payment_terms: List[PaymentTerm] = Field(..., description="List of payment terms and conditions")

# Timeline
class TimelineRow(BaseModel):
    phase: str = Field(..., description="Name of the project phase (e.g., Discovery, Design)")
    proposed_start_date: date = Field(..., description="Proposed start date for the phase")
    activities: Optional[str] = Field(None, description="Description of activities for this phase")
    deliverable: Optional[str] = Field(None, description="Expected deliverable for this phase")

class TimelineSchema(BaseModel):
    description: str = Field(..., description="Description providing context for the timeline")
    rows: List[TimelineRow] = Field(..., description="List of timeline rows representing project phases and details")

#Signature
class SignatureDetails(BaseModel):
    by: str = Field(None, description="Name of the person signing on behalf of the entity. If there is no info. about that, just return [insert service (recipient/provider) data]")
    company: str = Field(..., description="Name of the company. If there is no info. about that, just return [insert company name]")
    title: str = Field(None, description="Title or position of the signer. If there is no info. about that, just return [insert service (recipient/provider) title]")
    email: str = Field(None, description="Email address of the signer. If there is no info. about that, just return [insert service (recipient/provider) email]")

class SignaturesSchema(BaseModel):
    witness_text: str = Field(..., description="Text describing the agreement execution context")
    service_recipient: SignatureDetails = Field(..., description="Details of the service recipient")
    service_provider: SignatureDetails = Field(..., description="Details of the service provider")

class AgentState(TypedDict):
    meeting_summary_urls: List[str]
    meeting_summary_file_types: List[str]
    meeting_transcript_url: str
    meeting_transcript_file_type: str

    client_name: str

    vector_store: Any
    meeting_transcript_vector_store: Any

    meeting_transcript_analysis: MeetingTranscriptAnalysis
    sales_proposal_cover_page: SalesProposalCoverPage
    sales_proposal_structure: SalesProposalStructure
    final_sales_proposal: Any

def save_dict_to_txt(dictionary, file_path):
    """
    Save a dictionary to a text file in JSON format, excluding specified attributes.
    
    Args:
        dictionary (dict): The dictionary to save.
        file_path (str): The path to the text file.
    """
    # Exclude specific keys
    filtered_dict = {key: value for key, value in dictionary.items() if key not in ['vector_store', 'meeting_transcript_vector_store']}
    
    # Save the filtered dictionary to a file
    with open(file_path, 'w') as file:
        json.dump(filtered_dict, file, indent=4)

def return_retriever_from_vectorstore(vectorstore):
    return vectorstore.as_retriever(
            search_kwargs={"k": 3},
        )

def compile_rag_retrievers_node(state: AgentState, config: RunnableConfig):
    embeddings = OpenAIEmbeddings(model=os.environ.get('OPENAI_EMBEDDINGS_MODEL'))
    configuration = config.get("configurable", {})

    NON_ALLOWED_FILE_TYPES = {"user_gtxt", "user_gdoc", "user_gsheet", "user_gslide", "user_gpdf"}

    file_urls = state['meeting_summary_urls']
    file_types = state['meeting_summary_file_types']

    # Validate input lengths
    if len(file_urls) != len(file_types):
        raise ValueError("file_urls and file_types must have the same length.")

    # Function to process a single file
    def process_file(file_url, file_type):
        return get_docs(file_url, file_type)
    
    def process_non_allowed_files(file_urls, file_types):
        docs_list = []
        for file_url, file_type in zip(file_urls, file_types):
            if file_type in NON_ALLOWED_FILE_TYPES:
                try:
                    docs = get_docs(file_url, file_type)  # Process sequentially
                    docs_list.extend(docs)
                except Exception as e:
                    print(f"[ERROR] Failed to process file {file_url} of type {file_type}: {str(e)}")
        return docs_list

    # Multithreading for processing file_urls and file_types
    allowed_files = [(url, ftype) for url, ftype in zip(file_urls, file_types) if ftype not in NON_ALLOWED_FILE_TYPES]
    doc_list = []

    with ThreadPoolExecutor() as executor:
        future_to_file = {
            executor.submit(process_file, file_url, file_type): (file_url, file_type)
            for file_url, file_type in allowed_files
        }
        for future in as_completed(future_to_file):
            try:
                docs = future.result()
                doc_list.extend(docs)
            except Exception as e:
                print(f"[ERROR] Failed to process file {future_to_file[future]}: {str(e)}")
    
    doc_list.extend(process_non_allowed_files(file_urls, file_types))

    # Process the meeting transcript
    meeting_transcript_docs = get_docs(
        state['meeting_transcript_url'], 
        state['meeting_transcript_file_type']
    )

    # Create vector stores
    vector_store_docs = Chroma.from_documents(doc_list, embedding=embeddings, persist_directory=f"./{configuration.get('vector_store_folder_name')}")
    vector_store_meeting_transcript = Chroma.from_documents(meeting_transcript_docs, embedding=embeddings, persist_directory=f"./{configuration.get('meeting_transcript_vector_store_folder_name')}")

    print("FIRST STEP - COMPILE RAG RETRIEVERS: SUCCESSFULLY DONE")

    # Return the retrievers
    return {
        "vector_store": vector_store_docs,
        "meeting_transcript_vector_store": vector_store_meeting_transcript
    }

def generate_meeting_transcript_analysis_node(state: AgentState, config: RunnableConfig):

    json_parser = JsonOutputParser(pydantic_object=MeetingTranscriptAnalysis)
    rag_json_parser = JsonOutputParser(pydantic_object=MeetingTranscriptAnalysisRetrievedChunks)

    retriever = return_retriever_from_vectorstore(state['vector_store'])
    mt_retriever = return_retriever_from_vectorstore(state['meeting_transcript_vector_store'])

    retriever_tool = create_retriever_tool_func(
        name="meeting_summary_vector_store",
        description="Retrieves key insights from meeting summaries, focusing on critical questions such as: What use cases were highlighted as most interesting to the client? What is the expected value or outcome from implementing AI to solve each use case? How would Subatomic solve and deliver the results using its AI Co-worker Agents?",
        retriever=retriever
    )

    mt_retriever_tool = create_retriever_tool_func(
        name="meeting_transcript_vector_store",
        description="Retrieves relevant information from meeting transcripts, ensuring comprehensive answers to key questions like: What use cases were highlighted as most interesting to the client? What is the expected value or outcome from implementing AI to solve each use case? How would Subatomic solve and deliver the results using its AI Co-worker Agents?",
        retriever=mt_retriever
    )

    questions = {
        "use_cases_chunks": "What use cases were highlighted as most interesting to the client?",
        "expected_value_chunks": "What is the expected value or outcome from implementing AI to solve each use case?",
        "agents_chunks": "How would Subatomic solve and deliver the results using its AI Co-worker Agents?"
    }

    prompt_variables = {
        "questions": questions,
        "format_instructions": rag_json_parser.get_format_instructions()
    }
    
    react_agent = compile_react_agent([retriever_tool, mt_retriever_tool])

    configuration = config.get("configurable", {})

    docs_system_prompt = configuration.get("subatomic_elicit_docs_system_prompt")
    docs_user_prompt = configuration.get("subatomic_elicit_docs_user_prompt")

    retrieved_chunks_json = generate_agentic_rag_responses(
        react_agent=react_agent,
        system_prompt=docs_system_prompt,
        prompt_variables=prompt_variables,
        user_prompt=docs_user_prompt
    )

    retrieved_chunks = rag_json_parser.parse(retrieved_chunks_json)

    #org_user = configuration.get("org_user")
    #cursor = configuration.get("cursor")
    system_prompt = configuration.get("subatomic_generate_meeting_transcript_analysis_system_prompt")
    user_prompt = configuration.get("subatomic_generate_meeting_transcript_analysis_user_prompt")

    template = ChatPromptTemplate([
        ("system", system_prompt),
        ("human", user_prompt),
    ])
    
    messages = template.format_messages(
        use_cases_chunks=retrieved_chunks['use_cases_chunks'], 
        expected_value_chunks=retrieved_chunks['expected_value_chunks'], 
        agents_chunks=retrieved_chunks['agents_chunks'],
        format_instructions=json_parser.get_format_instructions()
    )
    generate_meeting_transcript_analysis_json = model.invoke(messages)

    meeting_transcript_analysis = json_parser.parse(generate_meeting_transcript_analysis_json.content)

    print(f"SECOND STEP - GENERATE MEETING TRANSCRIPT ANALYSIS: SUCCESSFULLY DONE => {meeting_transcript_analysis}")

    return {"meeting_transcript_analysis": meeting_transcript_analysis}

def generate_sales_proposal_cover_page_node(state: AgentState, config: RunnableConfig):
    json_parser = JsonOutputParser(pydantic_object=SalesProposalCoverPage)
    
    retriever = return_retriever_from_vectorstore(state['vector_store'])
    mt_retriever = return_retriever_from_vectorstore(state['meeting_transcript_vector_store'])

    cover_page_chunks = retriever.invoke("""
    What is the client company's exact name and the purpose of the proposal? (A brief description of the project)
    """)

    mt_cover_page_chunks = mt_retriever.invoke("""
    What is the client company's exact name and the purpose of the proposal? (A brief description of the project)
    """)

    model = ChatOpenAI(model=os.getenv('OPENAI_MODEL'), temperature=0.7)

    company_name = model.invoke(f"""
                                Given the following chunks, extract the full name of the client company please:
                                Cover Page Chunks: {cover_page_chunks} (MOST CRITICAL)
                                Meeting Transcript Page Chunks: {mt_cover_page_chunks}
                                Remember that it must not be Subatomic.
                                """)
    
    configuration = config.get("configurable", {})
    #org_user = configuration.get("org_user")
    #cursor = configuration.get("cursor")
    system_prompt = configuration.get("subatomic_generate_sales_proposal_cover_page_system_prompt")
    user_prompt = configuration.get("subatomic_generate_sales_proposal_cover_page_user_prompt")
    
    template = ChatPromptTemplate([
        ("system", system_prompt),
        ("human", user_prompt+f"\nRemember that you must use this company name: {company_name.content}"),
    ])

    messages = template.format_messages(
        meeting_transcript_analysis=state['meeting_transcript_analysis'],
        cover_page_chunks=cover_page_chunks + mt_cover_page_chunks, 
        format_instructions=json_parser.get_format_instructions()
    )

    generate_sales_proposal_cover_page_json = model.invoke(messages)

    sales_proposal_cover_page = json_parser.parse(generate_sales_proposal_cover_page_json.content)

    print(f"THIRD STEP - GENERATE SALES PROPOSAL COVER PAGE: SUCCESSFULLY DONE => {sales_proposal_cover_page}")

    return {"sales_proposal_cover_page": sales_proposal_cover_page, "client_name": company_name.content}

def generate_sales_proposal_structure_node(state: AgentState, config: RunnableConfig):
    #chain_name = "generate_sales_proposal_structure"
    json_parser = JsonOutputParser(pydantic_object=SalesProposalStructure)
    rag_json_parser = JsonOutputParser(pydantic_object=GenerateSalesProposalStructureChunks)

    retriever = return_retriever_from_vectorstore(state['vector_store'])
    mt_retriever = return_retriever_from_vectorstore(state['meeting_transcript_vector_store'])

    retriever_tool = create_retriever_tool_func(
        name="meeting_summary_vector_store",
        description=""" 
        Retrieves key insights from **meeting summaries**, focusing on project scope, deliverables, and strategy. Ideal for concise, high-level extraction.

        **Scope:**
        - **Project Scope & Deliverables:** Milestones, responsibilities, engagement terms.  
        - **Client Context:** Challenges, objectives, market position.  
        - **Proposed Solutions:** Methodologies, goals, expected outcomes.  
        - **Key Assumptions:** Dependencies, constraints, conditions.  
        - **Pricing Structure:** Cost breakdowns, value components.  
        - **Project Timeline:** Phases, milestones, completion dates.  
        - **Authorization & Agreements:** Approvals, signatories.  
        """,
        retriever=retriever
    )

    mt_retriever_tool = create_retriever_tool_func(
        name="meeting_transcript_vector_store",
        description=""" 
        Retrieves **detailed insights from full transcripts** for deeper analysis of discussions, opinions, and decisions.

        **Scope:**
        - **Project Scope & Deliverables:** Explicit statements on milestones, roles.  
        - **Client Context:** Direct mentions of challenges, goals.  
        - **Proposed Solutions:** Methodologies, expected outcomes.  
        - **Key Assumptions & Constraints:** Dependencies, limitations.  
        - **Pricing Structure:** Cost breakdowns, negotiations.  
        - **Project Timeline:** Deadlines, phases, updates.  
        - **Authorization & Approvals:** Signatories, agreement terms.  
        """,
        retriever=mt_retriever
    )

    questions = {
        "sales_proposal_sow_chunks": "What is the defined scope of work for this project? Please outline the key deliverables, milestones, and responsibilities of each party involved in the engagement.",
        "sales_proposal_background_chunks": "What is the client’s current context, including their key challenges, goals, and industry positioning? Provide relevant insights that set the stage for the proposed solution.",
        "sales_proposal_scope_chunks": "What solutions are being proposed to address the client’s needs? Detail the specific objectives, methodologies, and expected outcomes of the project.",
        "sales_proposal_assumptions_chunks": "What are the key assumptions that impact the project, such as dependencies, constraints, and conditions that must be met for successful execution?",
        "sales_proposal_pricing_chunks": "How is the pricing structured for this project? Provide a breakdown of costs, including any relevant packages, tiers, or customization options that add value to the proposal.",
        "sales_proposal_timeline_chunks": "What is the proposed project timeline, including major phases, key milestones, and expected completion dates?",
        "sales_proposal_signatures_chunks": "Who are the authorized signatories for this proposal, and what formal details need to be included for agreement and approval?"
    }

    prompt_variables = {
        "questions": questions,
        "format_instructions": rag_json_parser.get_format_instructions()
    }
    
    react_agent = compile_react_agent([retriever_tool, mt_retriever_tool])

    configuration = config.get("configurable", {})

    docs_system_prompt = configuration.get("subatomic_elicit_docs_system_prompt")
    docs_user_prompt = configuration.get("subatomic_elicit_docs_user_prompt")

    #org_user = configuration.get("org_user")
    #cursor = configuration.get("cursor")
    system_prompt = configuration.get("subatomic_generate_sales_proposal_structure_system_prompt")
    user_prompt = configuration.get("subatomic_generate_sales_proposal_structure_user_prompt")

    retrieved_chunks_json = generate_agentic_rag_responses(
        react_agent=react_agent,
        system_prompt=docs_system_prompt,
        prompt_variables=prompt_variables,
        user_prompt=docs_user_prompt
    )

    retrieved_chunks = rag_json_parser.parse(retrieved_chunks_json)

    template = ChatPromptTemplate([
        ("system", system_prompt),
        ("human", user_prompt+f"\nRemember that you must use this company name: {state['client_name']}"),
    ])

    messages = template.format_messages(
        meeting_transcript_analysis = state['meeting_transcript_analysis'],
        client_details = state['sales_proposal_cover_page'],
        sales_proposal_sow_chunks = retrieved_chunks['sales_proposal_sow_chunks'],
        sales_proposal_background_chunks = retrieved_chunks['sales_proposal_background_chunks'],
        sales_proposal_scope_chunks = retrieved_chunks['sales_proposal_scope_chunks'],
        sales_proposal_assumptions_chunks = retrieved_chunks['sales_proposal_assumptions_chunks'],
        sales_proposal_pricing_chunks = retrieved_chunks['sales_proposal_pricing_chunks'],
        sales_proposal_timeline_chunks = retrieved_chunks['sales_proposal_timeline_chunks'],
        sales_proposal_signatures_chunks = retrieved_chunks['sales_proposal_signatures_chunks'],
        format_instructions=json_parser.get_format_instructions()
    )

    generate_sales_proposal_structure_json = model.invoke(messages)

    sales_proposal_structure = json_parser.parse(generate_sales_proposal_structure_json.content)

    print(f"FOURTH STEP - GENERATE THE SALES PROPOSAL STRUCTURE: SUCCESSFULLY DONE => {sales_proposal_structure}")

    return {"sales_proposal_structure": sales_proposal_structure}


def generate_sales_proposal_node(state: AgentState, config: RunnableConfig):
    """
    Generate sections of a sales proposal using multithreading and scalable JSON parser handling.

    Args:
        state (Dict[str, Any]): The state object containing required data and configuration.
        config (Dict[str, Any]): The configuration object with prompts and other settings.

    Returns:
        Any: The final generated sales proposal.
    """
    # Map section names to their respective schemas
    section_schema_map = {
        "statement_of_work": SOWSchema,
        "background": BackgroundSchema,
        "scope": SalesProposalScope,
        "project_assumptions": ProjectAssumptionsSchema,
        "pricing": PricingSchema,
        "timeline": TimelineSchema,
        "signatures": SignaturesSchema
    }

    model = ChatOpenAI(model=os.getenv('OPENAI_MODEL'), temperature=0.7)

    # Extract necessary details from state and config
    sections_list = state['sales_proposal_structure']['sales_proposal_sections']
    main_aim = state['sales_proposal_structure']['main_aim']
    configuration = config.get("configurable", {})

    def process_section(section):
        """
        Process a single section to generate its content using the appropriate schema and prompts.

        Args:
            section: Section details including its name.

        Returns:
            Processed section with its generated content.
        """
        section_name = section['section_name']

        # Determine the schema for the section
        schema_class = section_schema_map.get(section_name)
        if not schema_class:
            raise ValueError(f"Unsupported section name: {section_name}")

        # Set up the JSON parser using the determined schema
        json_parser = JsonOutputParser(pydantic_object=schema_class)

        # Configure prompts for the section
        system_prompt = configuration.get(f"subatomic_generate_{section_name}_system_prompt")
        user_prompt = configuration.get(f"subatomic_generate_{section_name}_user_prompt")
        if not system_prompt or not user_prompt:
            raise ValueError(f"Prompts are not configured for section: {section_name}")

        template = ChatPromptTemplate([
            ("system", system_prompt),
            ("human", user_prompt+f"\nRemember that you must use this company name: {state['client_name']}"),
        ])

        # Generate responses using the RAG agent
        messages = template.format_messages(
            main_aim = main_aim,
            section = {**section, **state['meeting_transcript_analysis']},
            format_instructions=json_parser.get_format_instructions()
        )

        result = model.invoke(messages)
        
        # Parse the result using the JSON parser
        return {"section_name": section_name, "result": json_parser.parse(result.content)}

    # Multithreading to process all sections concurrently
    start_time = time.time()
    results = []

    with ThreadPoolExecutor() as executor:
        future_to_section = {executor.submit(process_section, section): section for section in sections_list}
        for future in as_completed(future_to_section):
            section = future_to_section[future]
            try:
                results.append(future.result())
            except Exception as e:
                print(f"Error processing section {section['section_name']}: {str(e)}")

    # Organize results by section names
    results_dict = {res["section_name"]: res["result"] for res in results}

    end_time = time.time()
    print(f"Total time taken for generating sales proposal sections: {end_time - start_time:.2f} seconds")

    # Build the final sales proposal
    final_sales_proposal = {
        "main_aim": main_aim,
        "cover_page": state['sales_proposal_cover_page'],
        **{section['section_name']: results_dict.get(section['section_name']) for section in sections_list}
    }

    print(f"FOURTH STEP - GENERATE THE SALES PROPOSAL: SUCCESSFULLY DONE => {final_sales_proposal}")
    return {"final_sales_proposal": final_sales_proposal}

def create_sales_proposal_graph_tool():
    # Create the Graph
    graph_builder = StateGraph(AgentState)

    graph_builder.add_node("compile_rag_retrievers_node", compile_rag_retrievers_node)
    graph_builder.add_node("generate_meeting_transcript_analysis_node", generate_meeting_transcript_analysis_node)
    graph_builder.add_node("generate_sales_proposal_cover_page_node", generate_sales_proposal_cover_page_node)
    graph_builder.add_node("generate_sales_proposal_structure_node", generate_sales_proposal_structure_node)
    graph_builder.add_node("generate_sales_proposal_node", generate_sales_proposal_node)

    graph_builder.set_entry_point("compile_rag_retrievers_node")
    graph_builder.add_edge("compile_rag_retrievers_node", "generate_meeting_transcript_analysis_node")
    graph_builder.add_edge("generate_meeting_transcript_analysis_node", "generate_sales_proposal_cover_page_node")
    graph_builder.add_edge("generate_sales_proposal_cover_page_node", "generate_sales_proposal_structure_node")
    graph_builder.add_edge("generate_sales_proposal_structure_node", "generate_sales_proposal_node")
    graph_builder.add_edge("generate_sales_proposal_node", END)

    # Compile the Graph
    graph = graph_builder.compile().with_config({"run_name": f"create_sales_proposal_agent"})
    
    #create_png_graph(graph)

    return graph