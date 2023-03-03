from math import ceil

from fastapi import APIRouter
from models.response import Response
from models.models import Tag
from db.database import Database
from sqlalchemy import desc

# APIRouter creates path operations for product module
router = APIRouter(
    prefix="/tag",
    tags=["Tag"],
    responses={404: {"description": "Not found"}},
)

database = Database()
engine = database.get_db_connection()

@router.get("/")
async def read_all_tags(page_size: int, page: int):
    session = database.get_db_session(engine)
    data = session.query(Tag).order_by(
        desc(Tag.name)).limit(page_size).offset((page-1)*page_size).all()
    total_count = session.query(Tag).count()
    total_pages = ceil(total_count / page_size)
    pagination = {
        "total_pages": total_pages,
        "current_page": page
    }
    return Response(data, pagination, 200, "Tag retrieved successfully.", False)

@router.get("/{tag_id}")
async def read_tag(tag_id: str):
    session = database.get_db_session(engine)
    response_message = "Tag retrieved successfully"
    data = None
    try:
        data = session.query(Tag).filter(
            Tag.id == tag_id).one()
    except Exception as ex:
        print("Error", ex)
        response_message = "Tag Not found"
    error = False
    # pagination = {
    #     "total_pages": 1,
    #     "current_page": 1
    # }
    return Response(data, {}, 200, response_message, error)