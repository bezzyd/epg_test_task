from pydantic import BaseModel, Field


class Evaluation(BaseModel):
    sender_id: int = Field(default=..., description="Sender id")
    like: bool = Field(default=True, description="Like")
