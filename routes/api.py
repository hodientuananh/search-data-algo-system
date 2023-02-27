from fastapi import APIRouter
from endpoints import product, tag, category

router = APIRouter()
router.include_router(product.router)
router.include_router(tag.router)
router.include_router(category.router)