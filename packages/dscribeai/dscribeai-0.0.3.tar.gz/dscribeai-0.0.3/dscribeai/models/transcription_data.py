from typing import List, Optional
from pydantic import BaseModel

from .paragraph import Paragraph
from .post_metadata import PostMetadata


class TranscriptionData(BaseModel):
    video_url: str
    post_url: str
    description: str
    transcription: str
    paragraphs: List[Paragraph]
    video_id: str
    transcribed_duration: float
    total_duration: float
    status: str
    platform: str
    title: str
    metadata: Optional[PostMetadata] = None