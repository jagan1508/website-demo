from sqlalchemy.orm import Session
from app.models.product import Product


class ProductRepository:

    @staticmethod
    def create(db: Session, product_data: dict):
        product = Product(**product_data)

        db.add(product)
        db.commit()
        db.refresh(product)

        return product

    @staticmethod
    def get_all(db: Session):
        return db.query(Product).all()

    @staticmethod
    def get_by_id(db: Session, product_id: int):
        return db.query(Product).filter(Product.id == product_id).first()
    
    @staticmethod
    def update(db: Session, product_id: int, update_data: dict):
        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            return None

        for key, value in update_data.items():
            setattr(product, key, value)

        db.commit()
        db.refresh(product)

        return product