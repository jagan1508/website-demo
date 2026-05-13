from pydantic import BaseModel, Field
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

class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float]  = None  
    image_url: Optional[str] = None
    stock: Optional[int] = None
    category_id: Optional[int] = None
