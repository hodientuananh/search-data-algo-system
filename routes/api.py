from fastapi import APIRouter
from endpoints import tag, category, search

router = APIRouter()
router.include_router(tag.router)
router.include_router(category.router)
router.include_router(search.router)