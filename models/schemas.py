from pydantic import BaseModel
from typing import List, Optional

class Task(BaseModel):
    id: int
    description: str
    status: str = "pending"
    result: Optional[str] = None

class ResearchPlan(BaseModel):
    goal: str
    tasks: List[Task]