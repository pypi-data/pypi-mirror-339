from pydantic import BaseModel


class QueryResult(BaseModel):
    answer: str