from agent.llm_client import client, MODEL_NAME
from agent.prompts import TASK_SUMMARY_PROMPT_TEMPLATE, FINAL_REPORT_PROMPT_TEMPLATE
from storage.persistance import save_plan
from tools.web_search import search_web


def execute_plan(plan):
    """
    Executes each task sequentially. Uses web search tool when appropriate.
    """

    print("\n=== EXECUTION START ===\n")

    for task in plan.tasks:
        if task.status == "completed":
            continue  # skip already done tasks

        print(f"[Agent] Executing Task {task.id}: {task.description}")

        # Tool Selection Logic
        if any(keyword in task.description.lower()
               for keyword in ["research", "identify", "analyze", "market", "trend"]):
            print(f"[Tool] Searching web for: {task.description}")
            tool_output = search_web(task.description)
        else:
            tool_output = "No external tool used."

        # Summarize Findings
        prompt = TASK_SUMMARY_PROMPT_TEMPLATE.format(
            task_description=task.description,
            tool_output=tool_output
        )

        response = client.responses.create(
            model=MODEL_NAME,
            input=prompt,
        )

        # Extract summary text
        task.result = response.output[0].content[0].text
        task.status = "completed"

        print(f"[Agent] Completed Task {task.id}\n")

        # Save plan after each task
        save_plan(plan)

    return plan


def synthesize_report(plan):
    """
    Create final structured report from completed tasks.
    """

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