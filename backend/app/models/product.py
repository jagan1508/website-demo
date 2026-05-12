from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)  
    price = Column(Float, nullable=False)
    image_url = Column(String)
    stock = Column(Integer, default=1)
    category_id = Column(Integer, ForeignKey("categories.id"))