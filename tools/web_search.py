import requests
import os
import re

def search_web(query: str, max_results: int = 5) -> str:

    api_key = os.getenv("SERPAPI_API_KEY")

    if not api_key:
        raise ValueError("SERPAPI_API_KEY not found in environment variables.")
    
    url = "https://serpapi.com/search"

    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": max_results
    }

    try:
        response = requests.get(url=url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Web search request failed: {e}") from e

    try:
        data = response.json()
    except ValueError as e:
        raise RuntimeError(f"Failed to parse search API response: {e}") from e

    organic_results = data.get("organic_results", [])

    if not organic_results:
        return "No results found."
    
    formatted_results = []

    for result in organic_results[:max_results]:
        title = result.get("title", "No title")
        snippet = result.get("snippet", "No snippet available")
        link = result.get("link", "No link")

        domain = link.split("/")[2] if "://" in link else link

        numbers = re.findall(
            r'\d+\.?\d*%?|\$?\d+\.?\d*\s?(?:billion|million|B|M)?',
            snippet
        )

        formatted_results.append({
            "title": title,
            "key_stats": numbers,
            "source": domain
        })

    return formatted_results