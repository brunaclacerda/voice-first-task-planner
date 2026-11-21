from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_async_db
from ..core.logging import setup_logger
from .model import Task
from .schema import TaskCreate

logger = setup_logger(__name__)


class TaskService:
    def __init__(self, db: AsyncSession = Depends(get_async_db)):
        self.db = db

    async def create_task(self, task: TaskCreate):
        logger.info("Create task")
        new_task = Task(**task.model_dump())
        self.db.add(new_task)
        await self.db.commit()
        return new_task
