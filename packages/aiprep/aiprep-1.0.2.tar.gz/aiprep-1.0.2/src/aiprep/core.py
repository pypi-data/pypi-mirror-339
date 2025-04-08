"""Core functionality for the aiprep package."""

import glob
import os

import pyperclip
import subprocess


def combine_files(file_list):
    combined_content = []
    for file_path in file_list:
        if not os.path.isfile(file_path):
            print(f"Warning: {file_path} is not a valid file. Skipping.")
            continue
        combined_content.append(f"{file_path}:\n```")
        with open(file_path, "r") as f:
            combined_content.append(f.read())
        combined_content.append("```\n")
    return "\n".join(combined_content)


def deblock_file(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: {file_path} is not a valid file.")
        return
    with open(file_path, "r") as f:
        content = f.read()
    updated_content = content.replace("```", "``")
    with open(file_path, "w") as f:
        f.write(updated_content)
    print(f"Updated {file_path}: triple backticks changed to double backticks.")


def reblock_file(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: {file_path} is not a valid file.")
        return
    with open(file_path, "r") as f:
        content = f.read()
    updated_content = content.replace("``", "```")
    with open(file_path, "w") as f:
        f.write(updated_content)
    print(f"Updated {file_path}: double backticks changed to triple backticks.")


def copy_to_clipboard(content):
    try:
        pyperclip.copy(content)
    except pyperclip.PyperclipException:
        try:
            process = subprocess.Popen(
                ["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE
            )
            process.communicate(input=content.encode("utf-8"))
        except Exception as e:
            print(f"Error copying to clipboard: {e}")


def recursive_glob(pattern, root_dir="."):
    """Recursively find files matching pattern from root_dir.

    Args:
        pattern: Glob pattern to match (e.g. "*.py")
        root_dir: Starting directory (defaults to current dir)

    Returns:
        List of matching file paths
    """
    if not isinstance(pattern, str):
        raise TypeError("pattern must be a string")

    matches = []
    try:
        for entry in os.walk(root_dir):
            dirpath = entry[0]
            full_pattern = os.path.join(dirpath, pattern)
            matches.extend(glob.glob(full_pattern))
    except (OSError, TypeError) as e:
        raise ValueError(f"Invalid directory or pattern: {e}") from e

    return matches
