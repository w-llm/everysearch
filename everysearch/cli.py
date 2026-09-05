"""
cli.py

Command-line interface for everysearch.
"""

import argparse
import os
import sys

from . import __version__
from .local_search import search_filesystem, validate_directory

# Visual indicators
DIR_ICON = "📁"
FILE_ICON = "📄"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="everysearch",
        description="Fast file and directory search from the command line.",
    )
    parser.add_argument(
        "term",
        help="Search term to look for in file/directory names.",
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
        "-v", "--version",
        action="version",
        version=f"everysearch {__version__}",
    )
    return parser


def print_result(result, base_dir: str) -> None:
    icon = DIR_ICON if result.is_dir else FILE_ICON
    rel_path = os.path.relpath(result.path, base_dir)
    print(f"  {icon}  {rel_path}")


def run(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.dirs_only and args.files_only:
        print("Error: --dirs-only and --files-only cannot be used together.", file=sys.stderr)
        return 1

    target_dir = os.path.abspath(args.directory)

    error = validate_directory(target_dir)
    if error:
        print(error, file=sys.stderr)
        return 1

    print(f"Searching for '{args.term}' in: {target_dir}\n")

    count = 0
    try:
        for result in search_filesystem(
            term=args.term,
            root=target_dir,
            case_sensitive=args.case_sensitive,
        ):
            if args.dirs_only and not result.is_dir:
                continue
            if args.files_only and result.is_dir:
                continue

            print_result(result, target_dir)
            count += 1

    except KeyboardInterrupt:
        print("\nSearch interrupted by user.", file=sys.stderr)
        return 130

    print(f"\n{count} result(s) found.")
    return 0


def main() -> None:
    sys.exit(run())


if __name__ == "__main__":
    main()
