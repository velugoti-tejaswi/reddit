from pydantic import BaseModel


class CommentPayloadSchema(BaseModel):
    url: str
