import requests
import os

def search_web(query: str, num_results: int = 5) -> str:
    """
    Perform a Google search using SerpAPI and return formatted results.
    """
    api_key = os.getenv("SERPAPI_API_KEY")

    if not api_key:
        raise ValueError("SERPAPI_API_KEY not found in environment variables.")
    
    url = "https://serpapi.com/search"

    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": num_results
    }

    response = requests.get(url=url, params=params)
    response.raise_for_status()

    data = response.json()

    organic_results = data.get("organic_results", [])

    if not organic_results:
        return "No results found."
    
    formatted_results = []

    for result in organic_results[:num_results]:
        title = result.get("title", "No title")
        snippet = result.get("snippet", "No snippet available")
        link = result.get("link", "No link")

        formatted_results.append(
            f"Title: {title}\n"
            f"Snippet: {snippet}\n"
            f"Source: {link}\n"
        )

    return "\n---\n".join(formatted_results)