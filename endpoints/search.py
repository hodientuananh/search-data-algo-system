from math import ceil

from fastapi import APIRouter, Query
from models.response import Response
from models.models import Knowledge, Definition, Exercise, Methodology, Knowledge_Tag, Tag
from db.database import Database
from typing import Optional, List, Union

# APIRouter creates path operations for product module
router = APIRouter(
    prefix="/search",
    tags=["Search"],
    responses={404: {"description": "Not found"}},
)

database = Database()
engine = database.get_db_connection()


@router.get("/")
async def search_result(keyword: Optional[str] = None, tables: Union[List[str], None] = Query(default=None),
                        tag_id: Optional[int] = None, category_id: Optional[int] = None,
                        page_size: int = 5, page: int = 1):
    session = database.get_db_session(engine)
    data = {
        'knowledge': {},
        'definition': {},
        'exercise': {},
        'methodology': {}
    }
    if keyword is not None:
        if tables is not None:
            if "knowledge" in tables:
                knowledge = session.query(Knowledge).filter(Knowledge.name.ilike(f"%{keyword}%")).all()
                knowledge_total_count = session.query(Knowledge).filter(Knowledge.name.ilike(f"%{keyword}%")).count()
                knowledge_total_pages = ceil(knowledge_total_count / page_size)
                pagination = {
                    "total_pages": knowledge_total_pages,
                    "current_page": page
                }
                data['knowledge'] = {
                    'data': knowledge,
                    'pagination': pagination
                }
            if 'definition' in tables:
                definition = session.query(Definition).filter(Definition.description.ilike(f"%{keyword}%")).all()
                definition_total_count = session.query(Definition).filter(Definition.description.ilike(f"%{keyword}%")).count()
                definition_total_pages = ceil(definition_total_count / page_size)
                pagination = {
                    "total_pages": definition_total_pages,
                    "current_page": page
                }
                data['definition'] = {
                    'data': definition,
                    'pagination': pagination
                }
            if 'exercise' in tables:
                exercise = session.query(Exercise).filter(Exercise.content.ilike(f"%{keyword}%")).all()
                exercise_total_count = session.query(Exercise).filter(Exercise.content.ilike(f"%{keyword}%")).count()
                exercise_total_pages = ceil(exercise_total_count / page_size)
                pagination = {
                    "total_pages": exercise_total_pages,
                    "current_page": page
                }
                data['definition'] = {
                    'data': exercise,
                    'pagination': pagination
                }
            if 'methodology' in tables:
                methodology = session.query(Methodology).filter(Methodology.content.ilike(f"%{keyword}%")).all()
                methodology_total_count = session.query(Methodology).filter(Methodology.content.ilike(f"%{keyword}%")).count()
                methodology_total_pages = ceil(methodology_total_count / page_size)
                pagination = {
                    "total_pages": methodology_total_pages,
                    "current_page": page
                }
                data['methodology'] = {
                    'data': methodology,
                    'pagination': pagination
                }
    elif tag_id is not None:
        knowledge_tag = session.query(Knowledge_Tag).filter(Knowledge_Tag.tag_id == tag_id).all()
        knowledge = session.query(Knowledge).filter(Knowledge.id.in_(c.knowledge_id for c in knowledge_tag)).all()
        data['knowledge'] = knowledge
    elif category_id is not None:
        knowledge = session.query(Knowledge).filter(Knowledge.category_id == category_id).all()
        data['knowledge'] = knowledge
    return Response(data,{}, 200, "Products retrieved successfully.", False)
