from unittest.mock import patch, MagicMock
from tools.web_search import search_web


def test_search_web_returns_formatted_results():
    
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "organic_results": [
            {
                "title": "Top Laptops 2025",
                "snippet": "Market grew by 15% with $10 billion in revenue.",
                "link": "https://example.com/laptops",
            }
        ]
    }

    with patch("tools.web_search.requests.get", return_value=mock_response):
        results = search_web("best laptops Europe")

    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0]["title"] == "Top Laptops 2025"
    assert results[0]["source"] == "example.com"
    assert any("15%" in s for s in results[0]["key_stats"])
