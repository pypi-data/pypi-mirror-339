from enum import Enum

class FileType(Enum):
    PDF = 'pdf'
    CSV = 'csv'
    TXT = 'txt'
    MD = 'md'
    URL = "url"
    MULTIPLE_URLS = 'multiple_urls'
    PPTX = 'pptx'
    DOCX = "docx"
    XLS = "xls"
    XLSX = "xlsx"
    XML = 'xml'
    JSON = 'json'
    GDOC = 'gdoc'
    GSHEET = "gsheet"
    GSLIDE = "gslide"
    GPDF = 'gpdf'

    GITHUB = 'github'
    YOUTUBE_URL = 'youtube_url' 
    IMG = 'img'
    EXTENSE_IMG = 'extense_img'
    MP3 = 'mp3'
    MP4 = 'mp4'