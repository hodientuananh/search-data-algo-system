from fastapi import APIRouter
from models.response import Response
from models.models import Feature
from db.database import Database
from sqlalchemy import desc

# APIRouter creates path operations for product module
router = APIRouter(
    prefix="/feature",
    tags=["Feature"],
    responses={404: {"description": "Not found"}},
)

database = Database()
engine = database.get_db_connection()


@router.get("/")
async def read_all_categories(page_size: int, page: int):
    session = database.get_db_session(engine)
    data = session.query(Feature).order_by(
        desc(Feature.name)).limit(page_size).offset((page - 1) * page_size).all()
    return Response(data, 200, "Feature retrieved successfully.", False)


@router.get("/{feature_id}")
async def read_feature(feature_id: str):
    session = database.get_db_session(engine)
    response_message = "Feature retrieved successfully"
    data = None
    try:
        data = session.query(Feature).filter(
            Feature.id == feature_id).one()
    except Exception as ex:
        print("Error", ex)
        response_message = "Feature Not found"
    error = False
    return Response(data, 200, response_message, error)
