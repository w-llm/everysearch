"""
web_search.py

Placeholder for future internet search capability.
Keeping this as its own module means cli.py never needs to change
its dispatch logic when this becomes a real implementation —
just fill in `search_web`.
"""

from typing import Iterator
from .local_search import SearchResult


def search_web(term: str, **kwargs) -> Iterator[SearchResult]:
    """
    Future: query a web search API/service and yield SearchResult-like
    objects (or a dedicated WebResult dataclass).
    """
    raise NotImplementedError(
        "Web search is not implemented yet. Coming in a future version of everysearch."
    )
