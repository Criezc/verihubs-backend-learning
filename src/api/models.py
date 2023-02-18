from pydantic import BaseModel, Field
from typing import Optional


class CreateUser(BaseModel):
    username: str
    password: str
    role: str = Field(title="choose between user or CS")


class UpdateUser(BaseModel):
    username: Optional[str]
    password: Optional[str]
    role: Optional[str]


class CreateProducts(BaseModel):
    product_name: str = Field(
        title="Input product name", min_length=5, max_length=100)
    product_version: str = Field(
        title="Input product version", min_length=1, max_length=100)


class CreateTickets(BaseModel):
    title: str = Field(title="Input title for ticket",
                       min_length=5, max_length=100)
    problem: str = Field(title="Describe your problems",
                         min_length=5, max_length=100)
    product_name: str = Field(
        title="Input product name", min_length=5, max_length=100)
    product_version: str = Field(
        title="Input product version", min_length=1, max_length=100)
