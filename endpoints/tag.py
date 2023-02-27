from fastapi import APIRouter
from models.response import Response
from models.models import Tag
from db.database import Database
from sqlalchemy import and_, desc

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
    return Response(data, 200, "Tag retrieved successfully.", False)