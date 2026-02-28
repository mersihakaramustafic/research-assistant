from agent.llm_client import client, MODEL_NAME
from agent.prompts import TASK_SUMMARY_PROMPT_TEMPLATE, FINAL_REPORT_PROMPT_TEMPLATE
from storage.persistence import save_plan
from tools.web_search import search_web
import logging

logger = logging.getLogger(__name__)

def execute_plan(plan):
    
    print("\n=== EXECUTION START ===\n")

    for task in plan.tasks:
        if task.status == "completed":
            continue

        print(f"[Agent] Executing Task {task.id}: {task.description}")
        logger.info(
            "Starting task execution",
            extra={"task_id": task.id, "stage": "execution"}
        )

        if any(keyword in task.description.lower()
               for keyword in ["research", "identify", "analyze", "market", "trend"]):
            print(f"[Tool] Searching web for: {task.description}")
            tool_output = search_web(task.description)
        else:
            tool_output = "No external tool used."

        prompt = TASK_SUMMARY_PROMPT_TEMPLATE.format(
            task_description=task.description,
            tool_output=tool_output
        )

        response = client.responses.create(
            model=MODEL_NAME,
            input=prompt,
        )

        logger.info(
            "LLM call completed",
            extra={
                "task_id": task.id,
                "stage": "execution"
            }
        )

        task.result = response.output[0].content[0].text
        task.status = "completed"

        print(f"[Agent] Completed Task {task.id}\n")

        logger.info(
            "Task completed",
            extra={"task_id": task.id, "stage": "execution"}
        )

        save_plan(plan)

    return plan


def synthesize_report(plan):

    compiled_results = "\n\n".join(
        f"{t.description}\n{t.result}" for t in plan.tasks
    )

    prompt = FINAL_REPORT_PROMPT_TEMPLATE.format(
        compiled_task_results=compiled_results
    )

    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
    )

    report_text = response.output[0].content[0].text
    return report_text