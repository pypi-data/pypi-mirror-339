from concurrent.futures import ThreadPoolExecutor
import json
import os
import re
import shutil
from langchain.tools.retriever import create_retriever_tool
from pathlib import Path
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
import requests
import uuid
from langgraph.prebuilt import create_react_agent

from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 100
)

def create_retriever_tool_func(name, description, retriever):
    retriever_tool = create_retriever_tool(
        retriever,
        name,
        description
    )

    return retriever_tool

def replace_placeholders(input_string, prompt_variables):
    """
    Replace placeholders in the input string with corresponding values from the prompt_variables dictionary.
    
    Args:
        input_string (str): The string containing placeholders to replace.
        prompt_variables (dict): A dictionary where keys match the placeholders in the input string.
        
    Returns:
        str: The input string with placeholders replaced by their respective values.
    """
    def replacer(match):
        placeholder = match.group(1)
        return str(prompt_variables.get(placeholder, match.group(0)))

    pattern = r"\{(\w+)\}"
    return re.sub(pattern, replacer, input_string)

def save_dict_to_txt(dictionary, file_path):
    """
    Save a dictionary to a text file in JSON format, excluding specified attributes.
    
    Args:
        dictionary (dict): The dictionary to save.
        file_path (str): The path to the text file.
    """
    # Exclude specific keys
    filtered_dict = {key: value for key, value in dictionary.items() if key not in ['vector_store', 'subatomic_vector_store', 'meeting_transcript_vector_store']}
    
    # Save the filtered dictionary to a file
    with open(file_path, 'w') as file:
        json.dump(filtered_dict, file, indent=4)


def load_dict_from_txt(filename):
    """
    Load a dictionary from a text file in JSON format located at the root of the project.
    
    Args:
        filename (str): The name of the text file.
    
    Returns:
        dict: The loaded dictionary.
    """
    root_path = Path(__file__).resolve().parents[3]  # Move up two levels to root
    file_path = root_path / filename  # Construct the full path
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with file_path.open('r', encoding='utf-8') as file:
        dictionary = json.load(file)
    
    return dictionary

def generate_agentic_rag_responses(react_agent, system_prompt, prompt_variables, user_prompt):

    improved_user_prompt = replace_placeholders(user_prompt, prompt_variables)

    prompt_template = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": improved_user_prompt}
    ]
    result = react_agent.invoke({"messages": prompt_template})

    #print(f"Results: {result}")

    return result['messages'][-1].content

def return_retriever_from_vectorstore(vectorstore):
    return vectorstore.as_retriever(
            search_kwargs={"k": 3},
        )

def fetch_markdown(url):
    """Fetches the Markdown content from a URL."""
    try:
        response = requests.get(url, timeout=10)  # Add timeout for better reliability
        if response.status_code == 200:
            return response.text  # Return the raw Markdown content as a string
        else:
            return None  # Handle failed requests gracefully
    except requests.RequestException:
        return None  # Handle network errors

def process_multiple_websites_as_md_documents(url_list):
    """Fetch and process Markdown content from multiple URLs using multithreading."""
    website_content = []

    # Using ThreadPoolExecutor for parallel execution
    with ThreadPoolExecutor(max_workers=10) as executor:  # Optimal thread count
        results = executor.map(fetch_markdown, url_list)  # Fetch URLs concurrently

    # Process responses
    for response_text in results:
        if response_text:
            list_docs = splitter.create_documents([response_text])  # Process with splitter
            website_content.extend(list_docs)

    return website_content

def create_random_folder():
    folder_name = str(uuid.uuid4())
    os.makedirs(folder_name)
    print(f"Folder created: {folder_name}")
    return folder_name

def remove_folder(folder_name):
    """Removes the specified folder if it exists."""
    if os.path.exists(folder_name) and os.path.isdir(folder_name):
        shutil.rmtree(folder_name)
        print(f"Folder removed: {folder_name}")
    else:
        print(f"Folder does not exist: {folder_name}")

def remove_folders_concurrently(folder_list, max_workers=5):
    """Removes multiple folders concurrently using ThreadPoolExecutor."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(remove_folder, folder_list)

def compile_react_agent(tools):
    """
    Returns:
        ReAct agent configured with relevant web retrieval tools.
    """
    
    # Ensure environment variable exists
    openai_model = os.getenv('OPENAI_MODEL')
    if not openai_model:
        raise ValueError("OPENAI_MODEL environment variable is not set.")

    model = ChatOpenAI(model=openai_model, temperature=0.7)

    # Create and return the ReAct agent
    return create_react_agent(model, tools=tools)

def pydantic_to_dict(obj):
    if isinstance(obj, BaseModel):
        return obj.model_dump()  # Pydantic v2
    elif isinstance(obj, dict):
        return {key: pydantic_to_dict(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [pydantic_to_dict(item) for item in obj]
    elif isinstance(obj, str):
        return json.loads(obj)
    else:
        return obj