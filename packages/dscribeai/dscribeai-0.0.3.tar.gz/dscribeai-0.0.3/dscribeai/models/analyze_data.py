from typing import Optional

from .transcription_data import TranscriptionData

from .query_result import QueryResult

class AnalyzeData(TranscriptionData):
    video_summary: str
    query_result: Optional[QueryResult] = None