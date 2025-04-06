from pydantic import BaseModel


class Sentence(BaseModel):
    text: str
    start: float
    end: float