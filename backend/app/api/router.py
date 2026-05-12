from fastapi import APIRouter
from app.api.routes.products import router as product_router
from app.api.routes.categories import router as category_router

api_router = APIRouter()

api_router.include_router(product_router)
api_router.include_router(category_router)