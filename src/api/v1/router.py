from fastapi import APIRouter
from api.v1.cats import router as cats_router
from api.v1.missions import router as missions_router

v1_router = APIRouter()
v1_router.include_router(cats_router)
v1_router.include_router(missions_router)
