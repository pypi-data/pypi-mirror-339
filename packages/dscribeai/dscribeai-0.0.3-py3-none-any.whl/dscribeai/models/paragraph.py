from typing import List
from pydantic import BaseModel

from .sentence import Sentence


class Paragraph(BaseModel):
    sentences: List[Sentence]
    num_words: int
    start: float
    end: float