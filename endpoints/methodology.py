from math import ceil

from fastapi import APIRouter
from models.response import Response
from models.models import Methodology, Knowledge
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
async def read_all_methodology(page_size: int, page: int):
    session = database.get_db_session(engine)
    data = session.query(Methodology).order_by(
        desc(Methodology.name)).limit(page_size).offset((page - 1) * page_size).all()
    total_count = session.query(Methodology).count()
    total_pages = ceil(total_count / page_size)
    pagination = {
        "total_pages": total_pages,
        "current_page": page
    }
    return Response(data, pagination, 200, "Methodology retrieved successfully.", False)


@router.get("/{methodology_id}")
async def read_methodology(methodology_id: int):
    session = database.get_db_session(engine)
    response_message = "Methodology retrieved successfully"
    data = None
    try:
        data = session.query(Methodology).filter(
            Methodology.id == methodology_id).first()
    except Exception as ex:
        print("Error", ex)
        response_message = "Methodology Not found"
    error = False
    return Response(data, {}, 200, response_message, error)


@router.get("/{methodology_id}/content")
async def get_content_of_methodology(methodology_id: int):
    session = database.get_db_session(engine)
    response_message = "Content retrieved successfully"
    data = {
        'knowledge_id': None,
        'id': None,
        'name': None,
        'description': None,
        'content': None,
        'knowledge': None,
        'related': None
    }
    try:
        methodology = session.query(Methodology).filter(
            Methodology.id == methodology_id).first()
        knowledge = session.query(Knowledge).filter(Knowledge.id == methodology.knowledge_id).first()
        related_methodology = session.query(Methodology).filter(Methodology.knowledge_id == knowledge.id).all()

        data['knowledge_id'] = methodology.knowledge_id
        data['id'] = methodology.id
        data['name'] = methodology.name
        data['description'] = methodology.description
        data['content'] = methodology.content
        data['knowledge'] = knowledge
        data['related'] = related_methodology
    except Exception as ex:
        print("Error", ex)
        response_message = "Content Not found"
    error = False
    return Response(data, {}, 200, response_message, error)
