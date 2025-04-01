from typing import List

from pydantic import BaseModel


class AdditionModel(BaseModel):
    additional_info: str
    additional_number: int
    id: int


class EntityModel(BaseModel):
    addition: AdditionModel
    id: int
    important_numbers: List[int]
    title: str
    verified: bool


class EntityListModel(BaseModel):
    entity: List[EntityModel]
