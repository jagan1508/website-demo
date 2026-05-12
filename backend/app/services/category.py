from sqlalchemy.orm import Session

from app.repository.category import CategoryRepository


class CategoryService:

    @staticmethod
    def create_category(db: Session, category_data):
        return CategoryRepository.create(db, category_data.dict())

    @staticmethod
    def get_categories(db: Session):
        return CategoryRepository.get_all(db)

    @staticmethod
    def get_category(db: Session, category_id: int):
        return CategoryRepository.get_by_id(db, category_id)