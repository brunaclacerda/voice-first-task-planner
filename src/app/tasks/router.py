from fastapi import APIRouter, Depends

from ..core.logging import setup_logger
from .schema import TaskCreate
from .service import TaskService

logger = setup_logger(__name__)

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get("/")
def list_tasks():
    return [{"id": 1, "title": "Course project 2"}]


@router.get("/{task_id}")
def get_task(task_id: int):
    return {"id": task_id, "title": "Course project"}


@router.post("/")
async def create_task(task: TaskCreate, service: TaskService = Depends()):
    logger.info("Create task")
    return await service.create_task(task)
