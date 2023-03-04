from math import ceil

from fastapi import APIRouter
from models.response import Response
from models.models import Feature, Knowledge
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
    total_count = session.query(Feature).count()
    total_pages = ceil(total_count / page_size)
    pagination = {
        "total_pages": total_pages,
        "current_page": page
    }
    return Response(data, pagination, 200, "Feature retrieved successfully.", False)


@router.get("/{feature_id}")
async def read_feature(feature_id: int):
    session = database.get_db_session(engine)
    response_message = "Feature retrieved successfully"
    data = None
    try:
        data = session.query(Feature).filter(
            Feature.id == feature_id).first()
    except Exception as ex:
        print("Error", ex)
        response_message = "Feature Not found"
    error = False
    # pagination = {
    #     "total_pages": 1,
    #     "current_page": 1
    # }
    return Response(data, {}, 200, response_message, error)


@router.get("/{feature_id}/content")
async def get_content_of_feature(feature_id: int):
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
        feature = session.query(Feature).filter(
            Feature.id == feature_id).first()
        knowledge = session.query(Knowledge).filter(Knowledge.id == feature.knowledge_id).first()
        related_knowledge = session.query(Knowledge).filter(Knowledge.category_id == knowledge.category_id).all()
        related_feature = session.query(Feature).filter(Feature.knowledge_id.in_([e.id for e in related_knowledge]))\
            .filter(Feature.id != feature_id).all()
        data['knowledge_id'] = feature.knowledge_id
        data['id'] = feature.id
        data['name'] = feature.name
        data['description'] = feature.description
        data['content'] = feature.content
        data['knowledge'] = knowledge
        data['related'] = related_feature
    except Exception as ex:
        print("Error", ex)
        response_message = "Content Not found"
    error = False
    return Response(data, {}, 200, response_message, error)