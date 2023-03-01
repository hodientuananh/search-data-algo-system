from fastapi import APIRouter
from models.response import Response
from models.models import Exercise
from db.database import Database
from sqlalchemy import desc

# APIRouter creates path operations for product module
router = APIRouter(
    prefix="/exercise",
    tags=["Exercise"],
    responses={404: {"description": "Not found"}},
)

database = Database()
engine = database.get_db_connection()


@router.get("/")
async def read_all_categories(page_size: int, page: int):
    session = database.get_db_session(engine)
    data = session.query(Exercise).order_by(
        desc(Exercise.name)).limit(page_size).offset((page - 1) * page_size).all()
    return Response(data, 200, "Exercise retrieved successfully.", False)


@router.get("/{exercise_id}")
async def read_exercise(exercise_id: str):
    session = database.get_db_session(engine)
    response_message = "Exercise retrieved successfully"
    data = None
    try:
        data = session.query(Exercise).filter(
            Exercise.id == exercise_id).one()
    except Exception as ex:
        print("Error", ex)
        response_message = "Exercise Not found"
    error = False
    return Response(data, 200, response_message, error)
