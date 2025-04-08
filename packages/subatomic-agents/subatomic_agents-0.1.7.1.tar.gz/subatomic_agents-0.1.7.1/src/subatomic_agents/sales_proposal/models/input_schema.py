from pydantic import BaseModel
from typing import List

class SalesProposalInput(BaseModel):
    meeting_summary_urls: List[str]
    meeting_summary_file_types: List[str]
    meeting_transcript_url: str
    meeting_transcript_file_type: str