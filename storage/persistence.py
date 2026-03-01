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
    try:
        with open(PLAN_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Plan file is corrupted and cannot be read: {e}") from e
    try:
        return ResearchPlan(**data)
    except Exception as e:
        raise RuntimeError(f"Plan file has an invalid structure: {e}") from e


def plan_exists() -> bool:
    return os.path.exists(PLAN_PATH)