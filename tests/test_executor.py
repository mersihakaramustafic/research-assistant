from unittest.mock import MagicMock, patch
from models.schemas import ResearchPlan, Task
from agent.executor import execute_plan


def test_execute_plan_completes_all_tasks():
    
    plan = ResearchPlan(
        goal="Research AI",
        tasks=[
            Task(id=1, description="Identify market players"),
            Task(id=2, description="Write a conclusion"),
        ],
    )

    usage = MagicMock(input_tokens=100, output_tokens=50, total_tokens=150)
    content = MagicMock(text="Task result")
    response = MagicMock(output=[MagicMock(content=[content])], usage=usage)

    with patch("agent.executor.client") as mock_client, \
         patch("agent.executor.search_web", return_value="search results"), \
         patch("agent.executor.save_plan"):
        mock_client.responses.create.return_value = response
        result = execute_plan(plan)

    assert all(t.status == "completed" for t in result.tasks)
    assert all(t.result == "Task result" for t in result.tasks)
