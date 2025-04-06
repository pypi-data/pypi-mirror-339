from pydantic import BaseModel


class PostMetadata(BaseModel):
    upload_time: str
    comment_count: int
    like_count: int
    thumbnail: str
    retweet_count: int
    quote_count: int