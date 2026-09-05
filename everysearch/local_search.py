"""
local_search.py

Filesystem search engine for everysearch.
Uses os.walk for speed and streams results as they're found.
"""

import os
from dataclasses import dataclass
from typing import Iterator, Optional


@dataclass
class SearchResult:
    path: str
    is_dir: bool
    name: str


def search_filesystem(
    term: str,
    root: str,
    case_sensitive: bool = False,
) -> Iterator[SearchResult]:
    """
    Walk `root` looking for files/dirs whose name contains `term`.
    Yields SearchResult objects lazily so the caller can print as it goes.
    Permission errors and broken symlinks are skipped, never raised.
    """
    if not case_sensitive:
        term = term.lower()

    def onerror(os_error):
        # Called by os.walk when it can't descend into a directory.
        # We swallow it (permission denied, etc.) instead of crashing.
        pass

    for dirpath, dirnames, filenames in os.walk(root, onerror=onerror, followlinks=False):
        # Check directories
        for dname in dirnames:
            candidate = dname if case_sensitive else dname.lower()
            if term in candidate:
                full_path = os.path.join(dirpath, dname)
                yield SearchResult(path=full_path, is_dir=True, name=dname)

        # Check files
        for fname in filenames:
            candidate = fname if case_sensitive else fname.lower()
            if term in candidate:
                full_path = os.path.join(dirpath, fname)
                yield SearchResult(path=full_path, is_dir=False, name=fname)


def validate_directory(path: str) -> Optional[str]:
    """
    Returns an error message string if the path is invalid, else None.
    """
    if not os.path.exists(path):
        return f"Error: path does not exist: {path}"
    if not os.path.isdir(path):
        return f"Error: path is not a directory: {path}"
    if not os.access(path, os.R_OK):
        return f"Error: no read permission for: {path}"
    return None
