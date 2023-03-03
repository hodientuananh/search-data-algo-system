from math import ceil

from fastapi import APIRouter
from models.response import Response
from models.models import Definition
from db.database import Database
from sqlalchemy import desc

# APIRouter creates path operations for product module
router = APIRouter(
    prefix="/definition",
    tags=["Definition"],
    responses={404: {"description": "Not found"}},
)

database = Database()
engine = database.get_db_connection()


@router.get("/")
async def read_all_definitions(page_size: int, page: int):
    session = database.get_db_session(engine)
    data = session.query(Definition).order_by(
        desc(Definition.name)).limit(page_size).offset((page - 1) * page_size).all()
    total_count = session.query(Definition).count()
    total_pages = ceil(total_count / page_size)
    pagination = {
        "total_pages": total_pages,
        "current_page": page
    }
    return Response(data, pagination, 200, "Definition retrieved successfully.", False)


@router.get("/{definition_id}")
async def read_definition(definition_id: str):
    session = database.get_db_session(engine)
    response_message = "Definition retrieved successfully"
    data = None
    try:
        data = session.query(Definition).filter(
            Definition.id == definition_id).one()
    except Exception as ex:
        print("Error", ex)
        response_message = "Definition Not found"
    error = False
    # pagination = {
    #     "total_pages": 1,
    #     "current_page": 1
    # }
    return Response(data, {}, 200, response_message, error)
