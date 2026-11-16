from fastapi import APIRouter

from ..tasks.router import router as tasks_router

router = APIRouter()

router.include_router(tasks_router)


@router.get("/")
def read_root():
    return {"Hello": "World"}
