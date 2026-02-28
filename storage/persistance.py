import json
from models.schemas import ResearchPlan

def save_plan(plan: ResearchPlan, filename="data/plan.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(plan.dict(), f, indent=2, ensure_ascii=False)

def load_plan(filename="data/plan.json") -> ResearchPlan:
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    return ResearchPlan(**data)