import json
from unittest.mock import MagicMock, patch
from models.schemas import ResearchPlan


def test_generate_plan_returns_research_plan():
    
    usage = MagicMock(input_tokens=100, output_tokens=50, total_tokens=150)
    content = MagicMock(text=json.dumps({
        "goal": "Research AI market",
        "tasks": [
            {"id": 1, "description": "Identify key players"},
            {"id": 2, "description": "Analyze market size"},
        ],
    }))
    response = MagicMock(output=[MagicMock(content=[content])], usage=usage)

    with patch("agent.planner.client") as mock_client:
        mock_client.responses.create.return_value = response
        from agent.planner import generate_plan
        plan = generate_plan("Research AI market")

    assert isinstance(plan, ResearchPlan)
    assert plan.goal == "Research AI market"
    assert len(plan.tasks) == 2
