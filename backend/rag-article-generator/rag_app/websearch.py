from langchain_community.tools.tavily_search import TavilySearchResults
from .config import TAVILY_K

def get_web_search_tool(k: int = TAVILY_K):
    """
    Return a TavilySearchResults tool instance.
    Requires env var TAVILY_API_KEY at runtime.
    """
    return TavilySearchResults(k=k)
