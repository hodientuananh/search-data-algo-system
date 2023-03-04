from math import ceil

from fastapi import APIRouter
from models.response import Response
from models.models import Definition, Knowledge
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
async def read_definition(definition_id: int):
    session = database.get_db_session(engine)
    response_message = "Definition retrieved successfully"
    data = None
    try:
        data = session.query(Definition).filter(
            Definition.id == definition_id).first()
    except Exception as ex:
        print("Error", ex)
        response_message = "Definition Not found"
    error = False
    return Response(data, {}, 200, response_message, error)


@router.get("/{definition_id}/content")
async def get_content_of_definition(definition_id: int):
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
        definition = session.query(Definition).filter(
            Definition.id == definition_id).first()
        knowledge = session.query(Knowledge).filter(Knowledge.id == definition.knowledge_id).first()
        related_knowledge = session.query(Knowledge).filter(Knowledge.category_id == knowledge.category_id).all()
        related_definition = session.query(Definition).filter(Definition.knowledge_id.in_(
            [e.id for e in related_knowledge])
        ).filter(Definition.id != definition_id).all()
        data['knowledge_id'] = definition.knowledge_id
        data['id'] = definition.id
        data['name'] = definition.name
        data['description'] = definition.description
        data['content'] = definition.content
        data['knowledge'] = knowledge
        data['related'] = related_definition
    except Exception as ex:
        print("Error", ex)
        response_message = "Content Not found"
    error = False
    return Response(data, {}, 200, response_message, error)
