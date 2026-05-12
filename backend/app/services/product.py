from sqlalchemy.orm import Session

from app.repository.product import ProductRepository


class ProductService:

    @staticmethod
    def create_product(db: Session, product_data):
        return ProductRepository.create(db, product_data.dict())

    @staticmethod
    def get_products(db: Session):
        return ProductRepository.get_all(db)

    @staticmethod
    def get_product(db: Session, product_id: int):
        return ProductRepository.get_by_id(db, product_id)