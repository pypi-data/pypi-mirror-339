from langchain_community.document_loaders import (
    YoutubeLoader, 
    PyPDFLoader, 
    TextLoader, 
    UnstructuredURLLoader, 
    UnstructuredPowerPointLoader, 
    Docx2txtLoader, 
    UnstructuredExcelLoader, 
    UnstructuredXMLLoader,
    JSONLoader
)
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from dotenv import load_dotenv, find_dotenv
import tempfile
import uuid
import requests
from errors.document_loader_errors import (
    FileHandlerError,
    VideoTranscriptError,
    ImageHandlerError
)
from helpers.file_types import FileType
import gdown
import os

import google.generativeai as genai
import time

from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from langchain_community.vectorstores.utils import filter_complex_metadata
from helpers.helper_github import pull_gather_repo_info

load_dotenv(find_dotenv())

STRUCTURED_TABULAR_FILE_EXTENSIONS = {"csv", "xls", "xlsx", "gsheet", "xml"}
FILE_TYPES_TO_CHECK = {'pdf', 'csv', 'txt', 'pptx'}

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 100
)

def get_docs(file_url: str, file_type: str, verbose=True):
    file_type = file_type.lower()

    if file_type in FILE_TYPES_TO_CHECK:
        try:
            # Make a HEAD request to get content type
            head_response = requests.head(file_url, allow_redirects=True)
            content_type = head_response.headers.get('Content-Type') 
            if content_type is None:
                raise FileHandlerError(f"Failed to retrieve Content-Type from URL ", file_url)
            # If the content type is HTML
            if 'text/html' in content_type:
                file_type = "url"
                print("text/html in content_type: change file_type to url")  
        
        except requests.exceptions.RequestException as e:
            exception_map = {
                requests.exceptions.MissingSchema: "Invalid URL format.",
                requests.exceptions.ConnectionError: "Failed to connect to the server.",
                requests.exceptions.Timeout: "Request timed out.",
            }
            # Check if the exception is in the map; if not, default to a generic message
            error_message = exception_map.get(type(e), f"Request failed: {e}")
            print(error_message)
            raise FileHandlerError(error_message, file_url)
  
    try:
        docs = []
        file_loader = file_loader_map[FileType(file_type)]
        docs = file_loader(file_url, verbose)
        return docs

    except KeyError:
        print(f"Unsupported file type: {file_type}")
        raise FileHandlerError(f"Unsupported file type", file_url)
    
    except Exception as e:
        print(f"Failed to load the document: {e}")
        raise FileHandlerError(f"Document loading failed", file_url)

def load_url_documents(url: str, verbose=False):
    try:
        # Using the global session to load documents with custom headers
        url_loader = UnstructuredURLLoader(urls=[url])
        docs = url_loader.load()
            
    except requests.exceptions.RequestException as e:
        print(f"HTTP error occurred: {e}")
        raise FileHandlerError(f"Failed to load document from URL due to HTTP error", url) from e
    except Exception as e:
        print(f"Failed to load document from URL: {e}")
        raise FileHandlerError(f"Failed to load document from URL", url)
    
    if docs:
        split_docs = splitter.split_documents(docs)

        if verbose:
            print(f"Found URL")
            print(f"Splitting documents into {len(split_docs)} chunks")

        return split_docs
    
def load_multiple_urls_documents(url: str, verbose=False):
    try:
        # Using the global session to load documents with custom headers
        loader = FireCrawlLoader(
            api_key=os.getenv('FIRECRAWL_API_KEY'),
            url=url,
            mode="crawl",
        )        
        docs = loader.load()
            
    except requests.exceptions.RequestException as e:
        print(f"HTTP error occurred: {e}")
        raise FileHandlerError(f"Failed to load document from URL due to HTTP error", url) from e
    except Exception as e:
        print(f"Failed to load document from URL: {e}")
        raise FileHandlerError(f"Failed to load document from URL", url)
    
    if docs:
        split_docs = splitter.split_documents(docs)

        if verbose:
            print(f"Found URL")
            print(f"Splitting documents into {len(split_docs)} chunks")

        return filter_complex_metadata(split_docs)


class FileHandler:
    def __init__(self, file_loader, file_extension):
        self.file_loader = file_loader
        self.file_extension = file_extension

    def load(self, url):
        # Generate a unique filename with a UUID prefix
        unique_filename = f"{uuid.uuid4()}.{self.file_extension}"

        try:
            # Download the file from the URL and save it to a temporary file
            response = requests.get(url, timeout=10)  
            response.raise_for_status()  # Raise an HTTPError for bad responses

            with tempfile.NamedTemporaryFile(delete=False, prefix=unique_filename) as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name

        except requests.exceptions.RequestException as req_err:
            print(f"HTTP request error: {req_err}")
            raise FileHandlerError(f"Failed to download file from URL", url) from req_err
        except Exception as e:
            print(f"An error occurred while downloading or saving the file: {e}")
            raise FileHandlerError(f"Failed to handle file download", url) from e

        # Use the file_loader to load the documents
        try:
            if self.file_loader == JSONLoader:
                loader = self.file_loader(file_path=temp_file_path, jq_schema='.', text_content=False)
            else:
                loader = self.file_loader(file_path=temp_file_path)
        except Exception as e:
            print(f"No such file found at {temp_file_path}")
            print(e)
            raise FileHandlerError(f"No file found", temp_file_path) from e

        try:
            documents = loader.load()
        except Exception as e:
            print(f"File content might be private or unavailable or the URL is incorrect.")
            raise FileHandlerError(f"No file content available", temp_file_path) from e

        # Remove the temporary file
        os.remove(temp_file_path)

        return documents

def load_pdf_documents(pdf_url: str, verbose=False):
    pdf_loader = FileHandler(PyPDFLoader, "pdf")
    docs = pdf_loader.load(pdf_url)

    if docs:
        split_docs = splitter.split_documents(docs)

        if verbose:
            print(f"Found PDF file")
            print(f"Splitting documents into {len(split_docs)} chunks")

        return split_docs


def load_csv_documents(csv_url: str, verbose=False):
    csv_loader = FileHandler(CSVLoader, "csv")
    docs = csv_loader.load(csv_url)

    if docs:
        if verbose:
            print(f"Found CSV file")
            print(f"Splitting documents into {len(docs)} chunks")

        return docs

def load_txt_documents(notes_url: str, verbose=False):
    notes_loader = FileHandler(TextLoader, "txt")
    docs = notes_loader.load(notes_url)

    if docs: 

        split_docs = splitter.split_documents(docs)

        if verbose:
            print(f"Found TXT file")
            print(f"Splitting documents into {len(split_docs)} chunks")

        return split_docs

def load_md_documents(notes_url: str, verbose=False):
    notes_loader = FileHandler(TextLoader, "md")
    docs = notes_loader.load(notes_url)

    if docs:

        split_docs = splitter.split_documents(docs)

        if verbose:
            print(f"Found MD file")
            print(f"Splitting documents into {len(split_docs)} chunks")

        return split_docs

def load_pptx_documents(pptx_url: str, verbose=False):
    pptx_handler = FileHandler(UnstructuredPowerPointLoader, 'pptx')

    docs = pptx_handler.load(pptx_url)
    if docs: 

        split_docs = splitter.split_documents(docs)

        if verbose:
            print(f"Found PPTX file")
            print(f"Splitting documents into {len(split_docs)} chunks")

        return split_docs

def load_docx_documents(docx_url: str, verbose=False):
    docx_handler = FileHandler(Docx2txtLoader, 'docx')
    docs = docx_handler.load(docx_url)
    if docs: 

        split_docs = splitter.split_documents(docs)

        if verbose:
            print(f"Found DOCX file")
            print(f"Splitting documents into {len(split_docs)} chunks")

        return split_docs

def load_xls_documents(xls_url: str, verbose=False):
    xls_handler = FileHandler(UnstructuredExcelLoader, 'xls')
    docs = xls_handler.load(xls_url)
    if docs: 

        split_docs = splitter.split_documents(docs)

        if verbose:
            print(f"Found XLS file")
            print(f"Splitting documents into {len(split_docs)} chunks")

        return split_docs

def load_xlsx_documents(xlsx_url: str, verbose=False):
    xlsx_handler = FileHandler(UnstructuredExcelLoader, 'xlsx')
    docs = xlsx_handler.load(xlsx_url)
    if docs: 

        split_docs = splitter.split_documents(docs)

        if verbose:
            print(f"Found XLSX file")
            print(f"Splitting documents into {len(split_docs)} chunks")

        return split_docs

def load_xml_documents(xml_url: str, verbose=False):
    xml_handler = FileHandler(UnstructuredXMLLoader, 'xml')
    docs = xml_handler.load(xml_url)
    if docs: 

        split_docs = splitter.split_documents(docs)

        if verbose:
            print(f"Found XML file")
            print(f"Splitting documents into {len(split_docs)} chunks")

        return split_docs
    
def load_json_documents(json_url: str, verbose=False):
    json_handler = FileHandler(JSONLoader, 'json')
    docs = json_handler.load(json_url)
    if docs: 

        split_docs = splitter.split_documents(docs)

        if verbose:
            print(f"Found JSON file")
            print(f"Splitting documents into {len(split_docs)} chunks")

        return split_docs
    
def load_github_repo(github_repo: str, verbose = True):
    github_content = pull_gather_repo_info(repo_url=github_repo)
    docs = Document(page_content=github_content, metadata={"source": github_repo})
    
    if docs:
        split_docs = splitter.split_documents([docs])

        if verbose:
            print(f"Found GitHub Repo.")
            print(f"Splitting documents into {len(split_docs)} chunks")

        return split_docs

class FileHandlerForGoogleDrive:
    def __init__(self, file_loader, file_extension='docx'):
        self.file_loader = file_loader
        self.file_extension = file_extension

    def load(self, url):
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                unique_filename = os.path.join(temp_dir, f"{uuid.uuid4()}.{self.file_extension}")
                
                print(f"Downloading file from URL: {url}")
                
                try:
                    gdown.download(url=url, output=unique_filename, fuzzy=True)
                    print(f"File downloaded successfully to {unique_filename}")
                except Exception as e:
                    print(e)
                    print("File content might be private or unavailable, or the URL is incorrect.")
                    raise FileHandlerError("No file content available") from e

                try:
                    loader = self.file_loader(file_path=unique_filename)
                except Exception as e:
                    print(f"No such file found at {unique_filename}")
                    raise FileHandlerError("No file found", unique_filename) from e

                try:
                    documents = loader.load()
                    print("File loaded successfully.")
                except Exception as e:
                    print(e)
                    print("Error loading file content.")
                    raise FileHandlerError("No file content available") from e

                return documents
        except Exception as e:
            print("An unexpected error occurred during the file handling process.")
            raise e
        
def load_gdocs_documents(drive_folder_url: str, verbose=False):

    gdocs_loader = FileHandlerForGoogleDrive(Docx2txtLoader)

    docs = gdocs_loader.load(drive_folder_url)

    if docs: 

        split_docs = splitter.split_documents(docs)

        if verbose:
            print(f"Found Google Docs files")
            print(f"Splitting documents into {len(split_docs)} chunks")

        return split_docs

def load_gsheets_documents(drive_folder_url: str, verbose=False):
    gsheets_loader = FileHandlerForGoogleDrive(UnstructuredExcelLoader, 'xlsx')
    docs = gsheets_loader.load(drive_folder_url)
    if docs: 

        split_docs = splitter.split_documents(docs)

        if verbose:
            print(f"Found Google Sheets files")
            print(f"Splitting documents into {len(split_docs)} chunks")

        return split_docs

def load_gslides_documents(drive_folder_url: str, verbose=False):
    gslides_loader = FileHandlerForGoogleDrive(UnstructuredPowerPointLoader, 'pptx')
    docs = gslides_loader.load(drive_folder_url)
    if docs: 

        split_docs = splitter.split_documents(docs)

        if verbose:
            print(f"Found Google Slides files")
            print(f"Splitting documents into {len(split_docs)} chunks")

        return split_docs

def load_gpdf_documents(drive_folder_url: str, verbose=False):

    gpdf_loader = FileHandlerForGoogleDrive(PyPDFLoader,'pdf')

    docs = gpdf_loader.load(drive_folder_url)
    if docs: 

        if verbose:
            print(f"Found Google PDF files")
            print(f"Splitting documents into {len(docs)} chunks")

        return docs

def load_docs_youtube_url(youtube_url: str, verbose=True) -> str:
    try:
        loader = YoutubeLoader.from_youtube_url(youtube_url, add_video_info=False)
    except Exception as e:
        print(f"No such video found at {youtube_url}")
        raise VideoTranscriptError(f"No video found", youtube_url) from e

    try:
        docs = loader.load()
        
    except Exception as e:
        print(f"Video transcript might be private or unavailable in 'en' or the URL is incorrect.")
        raise VideoTranscriptError(f"No video transcripts available", youtube_url) from e
    
    if verbose:
        print(f"Found video")
        print(f"Combined documents into a single string.")
        print(f"Beginning to process transcript...")

    split_docs = splitter.split_documents(docs)

    return split_docs

llm_for_img = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

def generate_docs_from_img(img_url, verbose: bool=False):
    message = HumanMessage(
    content=[
            {
                "type": "text",
                "text": "Give me a summary of what you see in the image. It must be 3 detailed paragraphs.",
            }, 
            {"type": "image_url", "image_url": img_url},
        ]
    )

    try:
        response = llm_for_img.invoke([message]).content
        print(f"Generated summary: {response}")
        docs = Document(page_content=response, metadata={"source": img_url})
        split_docs = splitter.split_documents([docs])
    except Exception as e:
        print(f"Error processing the request due to Invalid Content or Invalid Image URL")
        raise ImageHandlerError(f"Error processing the request", img_url) from e

    return split_docs

def generate_extense_docs_from_img(img_url, verbose: bool=False):
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": (
                    "You are a domain-specific knowledge extraction expert. Carefully examine the image and produce a detailed, multi-paragraph report that captures every relevant aspect of the content within its domain.\n\n"
                    "The report must be technical, structured, and exhaustive, organized as follows:\n\n"
                    "1. **Domain Classification**: Clearly identify the domain this image belongs to (e.g., medicine, engineering, finance, law, education, chemistry, etc.). Justify your reasoning based on visual or semantic cues in the image.\n\n"
                    "2. **Visual and Structural Description**: Describe in detail what is visible — include layout, orientation, axes, data types, anatomical structures, technical equipment, symbols, or text — depending on the domain. Preserve original terminology.\n\n"
                    "3. **Semantic Interpretation**: Analyze what the image is conveying or measuring. Interpret charts, relationships, labels, and configurations. Describe inferred meaning from a domain-expert point of view.\n\n"
                    "4. **Concept and Pattern Extraction**: Identify all domain-specific concepts, terminologies, units, patterns, or formulas that are present or implied. Break them down with clarity. Include any relational structures (e.g., cause-effect, comparison, classification).\n\n"
                    "5. **Procedural or Diagnostic Insight** (if applicable): If the image involves procedures (e.g., medical scans, legal processes, scientific methods), describe the underlying process or diagnostic implication.\n\n"
                    "6. **Relevant Metadata**: Extract or infer any technical metadata such as scale, orientation, timestamps, region of interest, model or version identifiers, citations, standards, or codes.\n\n"
                    "7. **Knowledge Graph Candidates**: List candidate terms, entities, definitions, and relationships that can be transformed into nodes and edges in a domain knowledge graph. Be specific and concise. Use the format: `Term: Definition | Category | Related Terms`\n\n"
                    "Your response should contain multiple dense and technical paragraphs. Avoid any generic observations. Focus on high-fidelity, domain-grounded, and structurally useful content."
                ),
            },
            {"type": "image_url", "image_url": img_url},
        ]
    )

    try:
        response = llm_for_img.invoke([message]).content
        print(f"Generated domain-specific report: {response}")
        docs = Document(page_content=response, metadata={"source": img_url})
        split_docs = splitter.split_documents([docs])
    except Exception as e:
        print("Error processing the request due to invalid content or image URL.")
        raise ImageHandlerError("Error processing the request", img_url) from e

    return split_docs


class FileHandlerAudioAndVideo:
    def __init__(self, file_extension):
        self.file_extension = file_extension

    def load(self, url, file_type="default"):
        # Extract the filename from the URL
        filename = url.split("/")[-1]
        temp_file_path = None

        try:
            # Download the file from the URL and save it with the original name
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            
            temp_file_path = tempfile.gettempdir() + os.sep + filename
            with open(temp_file_path, 'wb') as temp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    temp_file.write(chunk)

            print(f"File downloaded successfully: {temp_file_path}")

        except requests.RequestException as req_err:
            print(f"HTTP request error: {req_err}")
            raise FileHandlerError("Failed to download file from URL", url) from req_err
        except Exception as e:
            print(f"An error occurred while downloading or saving the file: {e}")
            raise FileHandlerError("Failed to handle file download", url) from e

        # Upload the file to the GenAI service
        try:
            genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
            myfile = genai.upload_file(temp_file_path)

            # Process based on file type (e.g., mp3, mp4)
            if file_type == "mp3":
                model = genai.GenerativeModel("gemini-1.5-flash")
                result = model.generate_content([myfile, "Provide the full transcript of this audio (MINIMUM OF 5 PARAGRAPHS WITH 1000 WORDS)"])
            elif file_type == "mp4":
                model = genai.GenerativeModel("gemini-1.5-flash")
                while myfile.state.name == "PROCESSING":
                    print("Processing video...")
                    time.sleep(5)
                    myfile = genai.get_file(myfile.name)

                result = model.generate_content([myfile, "Provide a full description of the video (MINIMUM OF 5 PARAGRAPHS WITH 1000 WORDS)"])

            docs = Document(page_content=result.text, metadata={"source": url})
            split_docs = splitter.split_documents([docs])
        except Exception as e:
            print(f"An error occurred during GenAI processing: {e}")
            raise FileHandlerError("Failed to process file with GenAI", temp_file_path) from e
        finally:
            # Remove the temporary file
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)

        return split_docs

def generate_docs_from_mp3(file_url: str, verbose: bool=False):
    audio_handler = FileHandlerAudioAndVideo("mp3")
    docs = audio_handler.load(file_url, "mp3")

    if docs:
        if verbose:
            print(f"Found MP3 file")
            print(f"Splitting documents into {len(docs)} chunks")

        return docs
    
def generate_docs_from_mp4(file_url: str, verbose: bool=False):
    audio_handler = FileHandlerAudioAndVideo("mp4")
    docs = audio_handler.load(file_url, "mp4")

    if docs:
        if verbose:
            print(f"Found MP4 file")
            print(f"Splitting documents into {len(docs)} chunks")

        return docs
    
file_loader_map = {
    FileType.PDF: load_pdf_documents,
    FileType.CSV: load_csv_documents,
    FileType.TXT: load_txt_documents,
    FileType.MD: load_md_documents,
    FileType.URL: load_url_documents,
    FileType.MULTIPLE_URLS: load_multiple_urls_documents,
    FileType.PPTX: load_pptx_documents,
    FileType.DOCX: load_docx_documents,
    FileType.XLS: load_xls_documents,
    FileType.XLSX: load_xlsx_documents,
    FileType.XML: load_xml_documents,
    FileType.JSON: load_json_documents,
    FileType.GDOC: load_gdocs_documents,
    FileType.GSHEET: load_gsheets_documents,
    FileType.GSLIDE: load_gslides_documents,
    FileType.GPDF: load_gpdf_documents,
    FileType.GITHUB: load_github_repo,
    FileType.YOUTUBE_URL: load_docs_youtube_url,
    FileType.IMG: generate_docs_from_img,
    FileType.EXTENSE_IMG: generate_extense_docs_from_img,
    FileType.MP3: generate_docs_from_mp3,
    FileType.MP4: generate_docs_from_mp4
}