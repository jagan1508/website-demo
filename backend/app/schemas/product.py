from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    stock: int
    category_id: int


class ProductResponse(ProductCreate):
    id: int
    class Config:
        from_attributes = True
