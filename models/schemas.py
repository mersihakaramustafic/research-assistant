from pydantic import BaseModel
from typing import List

class Task(BaseModel):
    id: int
    description: str
    status: str = "pending"
    result: str | None = None


class ResearchPlan(BaseModel):
    goal: str
    tasks: List[Task]