import requests
import xml.etree.ElementTree as ET

def get_repository_hash_and_name(repo_url):
    url = "https://git1file.com/api/process-codebase"
    
    files = {
        "repo_url": (None, repo_url)
    }

    response = requests.post(url, files=files)

    if response.status_code == 200:
        data = response.json()
        repo_hash = data.get("hash", "Hash not found")
        repo_full_name = data.get("repository", "Repository not found")  # Expected format: "owner/repo_name"

        print(f"Info. gathered successfully => Repo. Hash: {repo_hash} and Repo. Full Name: {repo_full_name}")

        return repo_full_name, repo_hash
    else:
        return None, f"Error: {response.status_code}, {response.text}"

def get_repository_analysis(repo_full_name, repo_hash):
    if not repo_full_name or not repo_hash:
        return "Invalid repository or hash"

    url = f"https://git1file.com/api/analysis/{repo_full_name.replace('/', '%2F')}/{repo_hash}"

    headers = {
        "accept": "*/*"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        print(f"Successful response: {str(response.json())}")

        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"

def get_file_analysis(analysis_id, analysis_type="raw"):
    """
    Fetches detailed file analysis for a given analysis ID and type.
    
    :param analysis_id: The ID of the analysis (retrieved from get_repository_analysis).
    :param analysis_type: The type of analysis to fetch (default: "raw").
    :return: Parsed XML data or error message.
    """
    url = f"https://git1file.com/api/analysis/file?analysisId={analysis_id}&type={analysis_type}"

    headers = {
        "accept": "*/*"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            root = ET.fromstring(response.text)  # Parse XML
            return ET.tostring(root, encoding="unicode")  # Convert XML tree to string
        except ET.ParseError:
            return "Error: Failed to parse XML response"
    else:
        return f"Error: {response.status_code}, {response.text}"

def pull_gather_repo_info(
    repo_url: str
):
    repo_full_name, repo_hash = get_repository_hash_and_name(repo_url)

    if "Error" not in repo_hash:
        analysis_result = get_repository_analysis(repo_full_name, repo_hash)
        
        if isinstance(analysis_result, dict) and "id" in analysis_result:
            analysis_id = analysis_result["id"]
            file_analysis_result = get_file_analysis(analysis_id, "raw")
            return file_analysis_result
        else:
            print("Error retrieving analysis ID:", analysis_result)
    else:
        print(f"Hash has an error: {repo_hash}")
