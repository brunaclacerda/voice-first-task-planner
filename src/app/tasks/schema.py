from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str


class TaskCreate(TaskBase):
    """Schema class for request"""
