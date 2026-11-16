from fastapi import APIRouter

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get("/")
def list_tasks():
    return [{"id": 1, "title": "Course project"}]


@router.get("/{task_id}")
def get_task(task_id: int):
    return {"id": task_id, "title": "Course project"}
