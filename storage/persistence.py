import json
import os
from models.schemas import ResearchPlan

DATA_DIR = "data"
PLAN_PATH = os.path.join(DATA_DIR, "plan.json")

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def save_plan(plan: ResearchPlan):
    ensure_data_dir()
    with open(PLAN_PATH, "w", encoding="utf-8") as f:
        json.dump(plan.dict(), f, indent=2, ensure_ascii=False)


def load_plan() -> ResearchPlan:
    with open(PLAN_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return ResearchPlan(**data)


def plan_exists() -> bool:
    return os.path.exists(PLAN_PATH)