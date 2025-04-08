"""Command-line interface for aiprep."""

import sys

from .core import (
    combine_files,
    copy_to_clipboard,
    deblock_file,
    reblock_file,
    recursive_glob,
)


def print_help():
    print(
        """Usage: aiprep [OPTIONS] <file1> <file2> ... <fileN>
Options:
  -h, --help            Show this help message and exit.
  -c, --combine         Combine the content of files into a clipboard-friendly format with codeblocks.
  -d, --deblock         Change all triple backticks (```) to double backticks (``) in the specified files.
  -r, --reblock         Change all double backticks (``) to triple backticks (```) in the specified files.
  --recursive           Recursively include files matching the given glob patterns.

Examples:
  aiprep -c file1 file2 file3
  aiprep -c --recursive "*.py"
  aiprep -d file1 file2
  aiprep -r file1 file2
"""
    )


def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    option = sys.argv[1]
    args = sys.argv[2:]

    recursive = False
    if "--recursive" in args:
        recursive = True
        args.remove("--recursive")

    files = []

    if recursive:
        if not args:
            print("Error: --recursive requires at least one pattern.")
            sys.exit(1)
        # Each argument is treated as a glob pattern
        for pattern in args:
            matched = recursive_glob(pattern)
            if matched:
                files.extend(matched)
            else:
                print(f"Warning: {pattern} matched no files. Skipping.")
    else:
        files = args

    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for f in files:
        if f not in seen:
            deduped.append(f)
            seen.add(f)
    files = deduped

    if option in ("-h", "--help"):
        print_help()
        sys.exit(0)
    elif option in ("-c", "--combine"):
        if not files:
            print("Error: No files provided for combining.")
            sys.exit(1)
        combined_content = combine_files(files)
        copy_to_clipboard(combined_content)
        print("Combined content copied to clipboard.")
        print("Files copied:")
        for f in files:
            print(f"  - {f}")
    elif option in ("-d", "--deblock"):
        if not files:
            print("Error: No files provided for deblocking.")
            sys.exit(1)
        for file in files:
            deblock_file(file)
    elif option in ("-r", "--reblock"):
        if not files:
            print("Error: No files provided for reblocking.")
            sys.exit(1)
        for file in files:
            reblock_file(file)
    else:
        print(f"Error: Unknown option '{option}'.")
        print_help()
        sys.exit(1)
