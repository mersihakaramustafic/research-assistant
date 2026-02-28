from agent.llm_client import client, MODEL_NAME
from agent.prompts import PLANNER_PROMPT_TEMPLATE
from models.schemas import ResearchPlan
import json


def generate_plan(goal: str) -> ResearchPlan:
    """
    Generate a structured research plan from a high-level goal.
    """

    prompt = PLANNER_PROMPT_TEMPLATE.format(goal=goal)

    # Call the OpenAI Responses API
    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
    )

    # Extract text output
    text_output = response.output[0].content[0].text

    # Parse JSON into ResearchPlan
    try:
        plan_dict = json.loads(text_output)
    except json.JSONDecodeError:
        print("Failed to parse JSON from LLM output. Output was:")
        print(text_output)
        raise

    plan = ResearchPlan(**plan_dict)
    return plan