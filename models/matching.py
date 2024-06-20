from pydantic import BaseModel

class Matching(BaseModel):
    user_id: int
    matching: list
    likes: list
    dislikes: list