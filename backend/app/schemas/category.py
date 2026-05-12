from pydantic import BaseModel
from typing import Optional

class CategoryCreate(BaseModel):
    name: str


class CategoryResponse(CategoryCreate):
    id: int
    class Config:
        from_attributes = True