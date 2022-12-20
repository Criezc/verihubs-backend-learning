from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class UserEntity(BaseModel):
    id: Optional[UUID] = uuid4()
    username: str = Field(default=None)
    password: str = Field(default=None)
    role: str = Field(default=None)

    class Config:
        the_schema = {
            "user_demo": {
                "id": uuid4(),
                "username": "Nova",
                "password": "123",
                "role": "user"
            }
        }


class UserLoginEntity(BaseModel):

    username: str = Field(default=None)
    password: str = Field(default=None)

    class Config:
        the_schema = {
            "user_demo": {
                "username": "Nova",
                "password": "123",
            }
        }
