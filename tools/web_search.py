
from typing import Dict, List

from crewai.tools import BaseTool
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup


def _search_web(query: str, max_results: int = 6) -> List[Dict]:
    """Return a list of {title, href, snippet}. No API key needed."""
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results, region='wt-wt', safesearch='moderate'):
            results.append({
                "title": r.get("title"),
                "href": r.get("href"),
                "snippet": r.get("body"),
            })
    return results


def _fetch_url(url: str, max_chars: int = 8000) -> str:
    """Fetch a URL and return a lightly cleaned text (truncated)."""
    try:
        resp = requests.get(url, timeout=12, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        # Remove script/style
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        text = " ".join(soup.get_text(separator=" ").split())
        return text[:max_chars]
    except Exception as e:
        return f"[fetch_error] {e}"


class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = "Search DuckDuckGo and return {title, href, snippet} results."

    def _run(self, query: str, max_results: int = 6) -> List[Dict]:
        return _search_web(query=query, max_results=max_results)


class FetchUrlTool(BaseTool):
    name: str = "fetch_url"
    description: str = "Fetch a URL and return cleaned article text (best effort)."

    def _run(self, url: str, max_chars: int = 8000) -> str:
        return _fetch_url(url=url, max_chars=max_chars)
