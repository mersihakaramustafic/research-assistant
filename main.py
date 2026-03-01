from agent.planner import generate_plan
from agent.executor import execute_plan, synthesize_report
from storage.persistence import load_plan, save_plan, plan_exists
from infrastructure.logging_config import setup_logging

from dotenv import load_dotenv
load_dotenv()


def main():
    setup_logging()

    if plan_exists():
        print("Found existing plan. Loading to resume...")
        plan = load_plan()

    else:
        print("=== Market Research AI Agent ===\n")
        goal = input("Enter your research goal: ")

        plan = generate_plan(goal)
        save_plan(plan)

    print("\n=== Generated Plan ===")
    for t in plan.tasks:
        print(f"{t.id}. {t.description} [{t.status}]")

    input("\nPress Enter to execute tasks...\n")

    completed_plan = execute_plan(plan)

    print("\n=== Task Results ===")
    for t in completed_plan.tasks:
        print(f"\nTask {t.id}: {t.description}")
        print(f"Result: {t.result}\n{'-'*50}")

    report = synthesize_report(completed_plan)

    print("\n=== FINAL MARKET RESEARCH REPORT ===\n")
    print(report)


if __name__ == "__main__":
    main()