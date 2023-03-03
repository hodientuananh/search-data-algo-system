from math import ceil

from fastapi import APIRouter
from models.response import Response
from models.models import Knowledge, Definition, Feature, Methodology, Exercise
from db.database import Database
from sqlalchemy import desc

# APIRouter creates path operations for product module
router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge"],
    responses={404: {"description": "Not found"}},
)

database = Database()
engine = database.get_db_connection()


@router.get("/")
async def read_all_knowledge(page_size: int, page: int):
    session = database.get_db_session(engine)
    data = session.query(Knowledge).order_by(
        desc(Knowledge.name)).limit(page_size).offset((page - 1) * page_size).all()
    total_count = session.query(Knowledge).count()
    total_pages = ceil(total_count / page_size)
    pagination = {
        "total_pages": total_pages,
        "current_page": page
    }
    return Response(data, pagination, 200, "Knowledge retrieved successfully.", False)


@router.get("/{knowledge_id}")
async def read_knowledge(knowledge_id: int):
    session = database.get_db_session(engine)
    response_message = "Knowledge retrieved successfully"
    data = None
    try:
        data = session.query(Knowledge).filter(
            Knowledge.id == knowledge_id).one()
    except Exception as ex:
        print("Error", ex)
        response_message = "Knowledge Not found"
    error = False
    # pagination = {
    #     "total_pages": 1,
    #     "current_page": 1
    # }
    return Response(data, {}, 200, response_message, error)

@router.get("/{knowledge_id}/content")
async def get_content_of_knowledge(knowledge_id: int):
    session = database.get_db_session(engine)
    response_message = "Content retrieved successfully"
    data = {
        'id': None,
        'name': None,
        'description': None,
        'definition': None,
        'feature': None,
        'methodology': None,
        'exercise': None,
        'related': None
    }
    try:
        knowledge = session.query(Knowledge).filter(
            Knowledge.id == knowledge_id).one()
        definition = session.query(Definition).filter(
            Definition.knowledge_id == knowledge_id).one()
        feature = session.query(Feature).filter(Feature.knowledge_id == knowledge_id).one()
        methodology = session.query(Methodology).filter(Methodology.knowledge_id == knowledge_id).all()
        exercise = session.query(Exercise).filter(Exercise.knowledge_id == knowledge_id).all()
        related_knowledge = session.query(Knowledge).filter(Knowledge.category_id == knowledge.category_id).all()
        data['id'] = knowledge.id
        data['name'] = knowledge.name
        data['description'] = knowledge.description
        data['definition'] = definition
        data['feature'] = feature
        data['methodology'] = methodology
        data['exercise'] = exercise
        data['related'] = related_knowledge
    except Exception as ex:
        print("Error", ex)
        response_message = "Content Not found"
    error = False
    return Response(data, {}, 200, response_message, error)
