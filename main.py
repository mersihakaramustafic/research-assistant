from dotenv import load_dotenv
load_dotenv()

from agent.planner import generate_plan
from agent.executor import execute_plan, synthesize_report


def main():
    print("=== Market Research AI Agent ===\n")
    goal = input("Enter your research goal: ")

    # Generate structured plan
    plan = generate_plan(goal)

    print("\n=== Generated Plan ===")
    for t in plan.tasks:
        print(f"{t.id}. {t.description} [{t.status}]")

    input("\nPress Enter to execute tasks...\n")

    # Execute plan (tool calls + summarization)
    completed_plan = execute_plan(plan)

    # Display task results
    print("\n=== Task Results ===")
    for t in completed_plan.tasks:
        print(f"\nTask {t.id}: {t.description}")
        print(f"Result: {t.result}\n{'-'*50}")

    # Synthesize final report
    report = synthesize_report(completed_plan)

    print("\n=== FINAL MARKET RESEARCH REPORT ===\n")
    print(report)


if __name__ == "__main__":
    main()