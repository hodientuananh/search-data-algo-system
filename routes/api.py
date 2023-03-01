from fastapi import APIRouter
from endpoints import tag, category, search, knowledge, definition, feature, methodology, exercise

router = APIRouter()
router.include_router(tag.router)
router.include_router(category.router)
router.include_router(search.router)
router.include_router(knowledge.router)
router.include_router(definition.router)
router.include_router(feature.router)
router.include_router(methodology.router)
router.include_router(exercise.router)