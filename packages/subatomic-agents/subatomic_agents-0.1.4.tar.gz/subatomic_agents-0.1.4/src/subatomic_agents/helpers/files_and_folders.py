from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import shutil
import uuid
from langchain import hub

def fetch_prompts_for_key(key):
    try:
        system_prompt = hub.pull(f"{key}_prompt").messages[0].prompt.template
        user_prompt = hub.pull(f"{key}_prompt").messages[1].prompt.template
        return {
            f"{key}_system_prompt": system_prompt,
            f"{key}_user_prompt": user_prompt
        }
    except Exception as e:
        return {
            f"{key}_system_prompt": f"Error: {str(e)}",
            f"{key}_user_prompt": f"Error: {str(e)}"
        }
    
def build_config_with_multithreading(keys):
    config = {"configurable": {}}

    with ThreadPoolExecutor() as executor:
        future_to_key = {executor.submit(fetch_prompts_for_key, key): key for key in keys}
        
        for future in as_completed(future_to_key):
            key = future_to_key[future]
            try:
                # Fetch results and update the configuration
                result = future.result()
                config["configurable"].update(result)
            except Exception as e:
                config["configurable"].update({
                    f"{key}_system_prompt": f"Error: {str(e)}",
                    f"{key}_user_prompt": f"Error: {str(e)}"
                })

    return config

def create_random_folder():
    folder_name = str(uuid.uuid4())
    os.makedirs(folder_name)
    return folder_name

def remove_folder(folder_name):
    """Removes the specified folder if it exists."""
    if os.path.exists(folder_name) and os.path.isdir(folder_name):
        shutil.rmtree(folder_name)

def remove_folders_concurrently(folder_list, max_workers=5):
    """Removes multiple folders concurrently using ThreadPoolExecutor."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(remove_folder, folder_list)

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