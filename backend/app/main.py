from fastapi import FastAPI

from app.api.router import api_router
from app.core.database import Base, engine
from app.models.product import Product
from app.models.category import Category

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Art Store API")

app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "Art Store Backend Running"}