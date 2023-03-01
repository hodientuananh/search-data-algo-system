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
        desc(Category.name)).limit(page_size).offset((page - 1) * page_size).all()
    return Response(data, 200, "Category retrieved successfully.", False)


@router.get("/{category_id}")
async def read_category(category_id: str):
    session = database.get_db_session(engine)
    response_message = "Category retrieved successfully"
    data = None
    try:
        data = session.query(Category).filter(
            Category.id == category_id).one()
    except Exception as ex:
        print("Error", ex)
        response_message = "Category Not found"
    error = False
    return Response(data, 200, response_message, error)
