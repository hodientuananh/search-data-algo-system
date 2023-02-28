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
                        tag_id: Optional[int] = None, category_id: Optional[int] = None):
    session = database.get_db_session(engine)
    data = {
        'knowledge': [],
        'definition': [],
        'exercise': [],
        'methodology': []
    }
    if keyword is not None:
        if tables is not None:
            if "knowledge" in tables:
                knowledge = session.query(Knowledge).filter(Knowledge.name.ilike(f"%{keyword}%")).all()
                data['knowledge'] = knowledge
            if 'definition' in tables:
                definition = session.query(Definition).filter(Definition.description.ilike(f"%{keyword}%")).all()
                data['definition'] = definition
            if 'exercise' in tables:
                exercise = session.query(Exercise).filter(Exercise.content.ilike(f"%{keyword}%")).all()
                data['exercise'] = exercise
            if 'methodology' in tables:
                methodology = session.query(Methodology).filter(Methodology.content.ilike(f"%{keyword}%")).all()
                data['methodology'] = methodology
    elif tag_id is not None:
        knowledge_tag = session.query(Knowledge_Tag).filter(Knowledge_Tag.tag_id == tag_id).all()
        knowledge = session.query(Knowledge).filter(Knowledge.id.in_(c.knowledge_id for c in knowledge_tag)).all()
        data['knowledge'] = knowledge
    elif category_id is not None:
        knowledge = session.query(Knowledge).filter(Knowledge.category_id == category_id).all()
        data['knowledge'] = knowledge
    return Response(data, 200, "Products retrieved successfully.", False)
