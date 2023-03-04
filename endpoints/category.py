from fastapi import APIRouter
from models.response import Response
from models.models import Category
from db.database import Database
from sqlalchemy import desc
from math import ceil


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
        desc(Category.name)).limit(page_size).offset((page - 1) * page_size).all()
    total_count = session.query(Category).count()
    total_pages = ceil(total_count / page_size)
    pagination = {
        "total_pages": total_pages,
        "current_page": page
    }
    return Response(data, pagination, 200, "Category retrieved successfully.", False)


@router.get("/{category_id}")
async def read_category(category_id: int):
    session = database.get_db_session(engine)
    response_message = "Category retrieved successfully"
    data = None
    try:
        data = session.query(Category).filter(
            Category.id == category_id).first()
    except Exception as ex:
        print("Error", ex)
        response_message = "Category Not found"
    error = False
    # pagination = {
    #     "total_pages": 1,
    #     "current_page": 1
    # }
    return Response(data, {}, 200, response_message, error)
