# aiprep

## Overview

The `aiprep` script is a versatile tool designed to streamline interactions with AI tools. It allows you to combine multiple files into a single, formatted output that is ready to paste into an AI prompt. The script handles filenames and code block delimiters (``backticks``) to ensure proper formatting, preserving the context and structure of your files when interacting with AI tools.

A key feature of this script is its ability to reformat markdown-style code blocks. This ensures that the pasted content renders properly within AI tools, avoiding issues like losing the code block formatting or having markdown render incorrectly in responses.

## Features

- Combine multiple files into a single, clipboard-ready output.
- Format the output with filenames and ``backticks`` for code blocks.
- Recursively collect files matching patterns with `--recursive`.
- Remove or re-add ``backticks`` to ensure correct rendering in AI prompts and responses.
- Skip invalid files with a warning, ensuring smooth processing.

## Why Modify Codeblocks?

When pasting formatted content into AI tools, the rendered markdown can sometimes interfere with the interaction:
- If markdown is left unprocessed, code blocks might not render correctly when AI responds.
- By removing and re-adding code block delimiters (``backticks``), the script ensures that your input retains the correct format and structure. This allows the AI to display and interpret code blocks correctly without inadvertently rendering markdown in its output.

The `--deblock` and `--reblock` options allow you to address this issue:
- `-d`, `--deblock`: Replace triple backticks with double backticks (```) to prevent markdown rendering in AI outputs.
- `-r`, `--reblock`: Restore triple backticks after processing to re-enable proper code block formatting.

## Installation

1. Ensure Python 3 is installed on your system.
2. Install `xclip` for clipboard functionality:
   ```bash
   sudo apt-get install xclip
   ```
3. Download or clone the script into your preferred directory.
4. Make the script executable:
   ```bash
   chmod +x aiprep
   ```

## Usage

Run the script with the desired functionality using the following options:

### Options
- `-c`, `--combine`: Combine multiple files into a single clipboard-friendly format with filenames and codeblocks.
- `-d`, `--deblock`: Replace triple backticks with double backticks (```) in the specified files.
- `-r`, `--reblock`: Replace double backticks (```) with triple backticks in the specified files.
- `--recursive`: Recursively include files matching the given glob patterns.
- `-h`, `--help`: Show usage instructions.

### Examples

#### Combine Files into Clipboard
```bash
./aiprep -c file1.py file2.py file3.py
```

#### Recursively Combine All ```.py``` Files
```bash
./aiprep -c --recursive "*.py"
```

This combines the content of all Python files in the current directory and subdirectories, formats them with filenames and triple backticks, and copies the result to your clipboard.

#### Modify Codeblocks
Replace triple backticks with double backticks:
```bash
./aiprep -d file1.md file2.md
```

Restore double backticks to triple backticks:
```bash
./aiprep -r file1.md file2.md
```

#### Help
```bash
./aiprep -h
```

### Expected Output (Copied to Clipboard)

For `-c`, the combined output will have the following format:

file1.py:
```text
<contents of file1.py>
```

file2.py:
```text
<contents of file2.py>
```

file3.py:
```text
<contents of file3.py>
```


## Notes

- Ensure all specified files exist. Non-existent or invalid file paths will be skipped with a warning.
- Use the `--deblock` and `--reblock` options carefully to handle code block rendering issues when interacting with AI tools.
- `--recursive` works with glob patterns (e.g., `"*.py"`) to collect matching files in all directories.

## Purpose

This script is designed to optimize workflows for loading multiple source code files into AI tools. By preparing files in a clipboard-ready format and ensuring proper rendering of code blocks, it eliminates common issues with markdown formatting in AI responses, allowing you to focus on content rather than formatting.

## License

Feel free to use, modify, and distribute this script as needed. No restrictions apply.
