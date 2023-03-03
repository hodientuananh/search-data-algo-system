from math import ceil

from fastapi import APIRouter
from models.response import Response
from models.models import Methodology
from db.database import Database
from sqlalchemy import desc

# APIRouter creates path operations for product module
router = APIRouter(
    prefix="/methodology",
    tags=["Methodology"],
    responses={404: {"description": "Not found"}},
)

database = Database()
engine = database.get_db_connection()


@router.get("/")
async def read_all_categories(page_size: int, page: int):
    session = database.get_db_session(engine)
    data = session.query(Methodology).order_by(
        desc(Methodology.name)).limit(page_size).offset((page - 1) * page_size).all()
    total_count = session.query(Methodology).count()
    total_pages = ceil(total_count / page_size)
    # pagination = {
    #     "total_pages": total_pages,
    #     "current_page": page
    # }
    return Response(data, {}, 200, "Methodology retrieved successfully.", False)


@router.get("/{methodology_id}")
async def read_methodology(methodology_id: str):
    session = database.get_db_session(engine)
    response_message = "Methodology retrieved successfully"
    data = None
    try:
        data = session.query(Methodology).filter(
            Methodology.id == methodology_id).one()
    except Exception as ex:
        print("Error", ex)
        response_message = "Methodology Not found"
    error = False
    pagination = {
        "total_pages": 1,
        "current_page": 1
    }
    return Response(data, pagination, 200, response_message, error)
