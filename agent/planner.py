from agent.llm_client import client, MODEL_NAME
from agent.prompts import PLANNER_PROMPT_TEMPLATE
from models.schemas import ResearchPlan
import json
import logging

logger = logging.getLogger(__name__)

def generate_plan(goal: str) -> ResearchPlan:

    logger.info(
        "Generating research plan",
        extra={"stage": "planning"}
    )

    prompt = PLANNER_PROMPT_TEMPLATE.format(goal=goal)

    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
    )

    text_output = response.output[0].content[0].text

    try:
        plan_dict = json.loads(text_output)
    except json.JSONDecodeError:
        print("Failed to parse JSON from LLM output. Output was:")
        print(text_output)
        raise

    plan = ResearchPlan(**plan_dict)
    return plan