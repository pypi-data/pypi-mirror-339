import argparse
import os
import re
from pathlib import Path
from typing import List, Optional
import pyperclip

IMPORTANT_FILES: List[str] = ['.vue', '.js', '.py', '.sql']
EXCLUDE_DIRS: List[str] = [
    'node_modules', '__pycache__', '.venv', 'site-packages',
    'dist', 'build', '.git', '.eggs', 'migrations', 'tests',
    'aggregators', 'charts'
]
PROMPT_HEADER: str = "You're very a senior developer with experience in Python/FastAPI/Vuetify. Here are the important parts of my project with their content:"

def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Generate a prompt from project files."
    )
    parser.add_argument(
        '--filter',
        type=str,
        default='',
        help="Filter files by a case-insensitive pattern (pattern1|pattern2)."
    )
    parser.add_argument(
        '--exclude',
        type=str,
        default='',
        help="Exclude directories/files matching pattern (pattern1|pattern2)."
    )
    parser.add_argument(
        '--file',
        action='store_true',
        help="Output prompt to a file instead of clipboard."
    )
    return parser.parse_args()

def should_exclude_path(path: str, exclude_pattern: Optional[str]) -> bool:
    """
    Determine if a path should be excluded based on exclude pattern.

    Args:
        path: Path string to check
        exclude_pattern: Regular expression pattern for exclusion

    Returns:
        bool: True if path should be excluded
    """
    if not exclude_pattern:
        # Use default exclusions if no pattern provided
        return any(exclude_dir in path for exclude_dir in EXCLUDE_DIRS)

    compiled_pattern = re.compile(exclude_pattern, re.IGNORECASE)
    return bool(compiled_pattern.search(path))

def get_filtered_files(directory: Path, filter_pattern: Optional[str],
                      exclude_pattern: Optional[str]) -> List[Path]:
    """
    Retrieve a list of important files from the directory, filtered by patterns.

    Args:
        directory: The root directory to search
        filter_pattern: Regex pattern to include files
        exclude_pattern: Regex pattern to exclude directories/files

    Returns:
        List[Path]: List of filtered file paths
    """
    filtered_files = []
    compiled_filter = re.compile(filter_pattern, re.IGNORECASE) if filter_pattern else None

    for root, dirs, files in os.walk(directory):
        # Convert to string for pattern matching
        root_str = str(root)

        # Exclude directories in-place
        dirs[:] = [d for d in dirs if not should_exclude_path(os.path.join(root_str, d),
                                                             exclude_pattern)]

        for file in files:
            file_path = Path(root) / file
            full_path_str = str(file_path)

            # Check if file has an important extension
            if file_path.suffix not in IMPORTANT_FILES:
                continue

            # Skip if path should be excluded
            if should_exclude_path(full_path_str, exclude_pattern):
                continue

            # Apply filter if provided
            if compiled_filter and not compiled_filter.search(full_path_str):
                continue

            filtered_files.append(file_path)

    return filtered_files

def read_file_content(file_path: Path) -> Optional[str]:
    """Read the content of a file."""
    try:
        with file_path.open('r', encoding='utf-8') as file:
            content = file.read()
            return content
    except (IOError, UnicodeDecodeError) as e:
        print(f"Warning: Failed to read {file_path}: {e}")
        return None

def generate_prompt(directory: Path, filter_pattern: Optional[str] = None,
                   exclude_pattern: Optional[str] = None) -> str:
    """
    Generate a prompt string containing the contents of filtered files.

    Args:
        directory: The root directory of the project
        filter_pattern: Pattern to include files
        exclude_pattern: Pattern to exclude directories/files

    Returns:
        str: The generated prompt
    """
    prompt_lines = [PROMPT_HEADER]
    files = get_filtered_files(directory, filter_pattern, exclude_pattern)

    for file_path in files:
        relative_path = file_path.relative_to(directory)
        prompt_lines.append(f"\n- {relative_path}\n")
        content = read_file_content(file_path)
        if content is not None:
            file_extension = file_path.suffix.lstrip('.')
            prompt_lines.append(f"```{file_extension}\n{content}\n```")
            print(f"Added {relative_path} to the prompt.")

    return "\n".join(prompt_lines)

def main() -> None:
    args = parse_arguments()
    project_root = Path(__file__).parent.resolve()
    prompt = generate_prompt(project_root, args.filter, args.exclude)

    if args.file:
        output_file = project_root / "generated_prompt.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(prompt)
        print(f"The prompt has been saved to: {output_file}")
    else:
        try:
            pyperclip.copy(prompt)
            print("The prompt has been copied to your clipboard.")
        except pyperclip.PyperclipException as e:
            print(f"Error: Could not copy to clipboard. {e}")
            print("Please use the '--file' flag for output to a file in a headless environment.")

if __name__ == "__main__":
    main()
