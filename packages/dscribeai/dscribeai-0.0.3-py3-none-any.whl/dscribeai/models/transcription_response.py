from __future__ import annotations

from typing import List

from pydantic import BaseModel

from .transcription_data import TranscriptionData


class TranscriptionResponse(BaseModel):
    status: str
    operation_id: str
    data: List[TranscriptionData]