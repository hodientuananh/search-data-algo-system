from fastapi import APIRouter
from models.response import Response
from models.models import Category
from db.database import Database
from sqlalchemy import desc

# APIRouter creates path operations for product module
router = APIRouter(
    prefix="/category",
    tags=["Category"],
    responses={404: {"description": "Not found"}},
)

database = Database()
engine = database.get_db_connection()

@router.get("/")
async def read_all_categories(page_size: int, page: int):
    session = database.get_db_session(engine)
    data = session.query(Category).order_by(
        desc(Category.name)).limit(page_size).offset((page-1)*page_size).all()
    return Response(data, 200, "Category retrieved successfully.", False)