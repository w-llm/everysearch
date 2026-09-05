"""
cli.py

Command-line interface for everysearch.
"""

import argparse
import os
import sys

from . import __version__
from .local_search import search_filesystem, validate_directory
from .web_search import check_username

# Visual indicators
DIR_ICON = "📁"
FILE_ICON = "📄"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="everysearch",
        description="Fast file/directory search, plus social media username lookup.",
    )
    parser.add_argument(
        "term",
        nargs="?",
        default=None,
        help="Search term to look for in file/directory names (not needed with --social).",
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to search in (default: current directory).",
    )
    parser.add_argument(
        "-c", "--case-sensitive",
        action="store_true",
        help="Perform a case-sensitive search.",
    )
    parser.add_argument(
        "--dirs-only",
        action="store_true",
        help="Only show matching directories.",
    )
    parser.add_argument(
        "--files-only",
        action="store_true",
        help="Only show matching files.",
    )
    parser.add_argument(
        "--social",
        metavar="USERNAME",
