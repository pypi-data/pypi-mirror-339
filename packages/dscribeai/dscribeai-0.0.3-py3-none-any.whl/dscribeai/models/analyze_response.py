from __future__ import annotations

from typing import List

from pydantic import BaseModel

from .analyze_data import AnalyzeData

class AnalyzeResponse(BaseModel):
    status: str
    operation_id: str
    data: List[AnalyzeData]