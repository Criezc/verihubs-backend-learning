from pydantic import BaseModel, Field
from typing import Optional
import uuid


class CreateUser(BaseModel):
    id: Optional[uuid.UUID] = uuid.uuid4()
    username: str
    password: str
    role: str = Field(title="choose between user or CS")
