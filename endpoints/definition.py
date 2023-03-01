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
    return Response(data, 200, "Definition retrieved successfully.", False)


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
    return Response(data, 200, response_message, error)
