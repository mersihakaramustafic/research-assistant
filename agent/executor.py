from agent.llm_client import client, MODEL_NAME
from agent.prompts import TASK_SUMMARY_PROMPT_TEMPLATE, FINAL_REPORT_PROMPT_TEMPLATE
from storage.persistence import save_plan
from tools.web_search import search_web
import logging

logger = logging.getLogger(__name__)

def execute_plan(plan):

    print("\n=== EXECUTION START ===\n")

    total_input_tokens = 0
    total_output_tokens = 0

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

        usage = response.usage
        total_input_tokens += usage.input_tokens
        total_output_tokens += usage.output_tokens
        logger.info(
            "LLM call completed",
            extra={
                "task_id": task.id,
                "stage": "execution",
                "input_tokens": usage.input_tokens,
                "output_tokens": usage.output_tokens,
                "total_tokens": usage.total_tokens,
            }
        )
        print(f"[Execution] Task {task.id} tokens - Input: {usage.input_tokens}, Output: {usage.output_tokens}, Total: {usage.total_tokens}")

        task.result = response.output[0].content[0].text
        task.status = "completed"

        print(f"[Agent] Completed Task {task.id}\n")

        logger.info(
            "Task completed",
            extra={"task_id": task.id, "stage": "execution"}
        )

        save_plan(plan)

    print(f"[Execution] Total tokens - Input: {total_input_tokens}, Output: {total_output_tokens}, Total: {total_input_tokens + total_output_tokens}")
    logger.info(
        "Execution total token usage",
        extra={"stage": "execution", "input_tokens": total_input_tokens,
               "output_tokens": total_output_tokens, "total_tokens": total_input_tokens + total_output_tokens}
    )

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

    usage = response.usage
    logger.info(
        "Final generation token usage",
        extra={"stage": "final_generation", "input_tokens": usage.input_tokens,
               "output_tokens": usage.output_tokens, "total_tokens": usage.total_tokens}
    )
    print(f"[Final Generation] Tokens — Input: {usage.input_tokens}, Output: {usage.output_tokens}, Total: {usage.total_tokens}")

    report_text = response.output[0].content[0].text
    return report_text