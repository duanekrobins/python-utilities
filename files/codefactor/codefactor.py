"""

Developer: Duane Robinson
Last Modified: 2024-11-26 12:52:53
Description: This script uses libraries like os, shutil, ast, hashlib; includes function `log_action`: Logs actions to the console and a log file.; includes function `backup_file`: Creates a backup of the specified file.; includes function `analyze_file_functionality`: Analyzes the provided Python file to determine its purpose and functionality.; includes function `add_header_and_comments`: Adds a meaningful header and comments to the file.; includes function `rename_and_save_file`: Renames the file to a new name and saves it.; includes function `validate_output`: Validates the processed file to ensure headers and comments are properly added.; includes function `process_file`: Processes a single file.; includes function `process_directory`: Prompts for directory and processes all eligible Python files..

"""

# Importing necessary libraries.
"""
# Function `log_action`: Logs actions to the console and a log file.
Developer: Duane Robinson
# Function `backup_file`: Creates a backup of the specified file.
Last Modified: 2024-11-26
# Function `analyze_file_functionality`: Analyzes the provided Python file to determine its purpose and functionality.
Description: Processes Python source files to add headers, generate comments, rename based on functionality,
# Function `add_header_and_comments`: Adds a meaningful header and comments to the file.
             and validate all outputs. Prevents naming conflicts using unique identifiers.
# Function `rename_and_save_file`: Renames the file to a new name and saves it.
"""
# Function `validate_output`: Validates the processed file to ensure headers and comments are properly added.

# Function `process_file`: Processes a single file.
import os
# Function `process_directory`: Prompts for directory and processes all eligible Python files.
import shutil
import ast
import hashlib
from datetime import datetime

# Constants
DEVELOPER_NAME = "Duane Robinson"
LOG_FILE_NAME = "processing_log.txt"
BACKUP_SUFFIX = "_backup"

def log_action(action, log_file_path):
    """Logs actions to the console and a log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"{timestamp} - {action}"
    print(message)
    with open(log_file_path, "a") as log:
        log.write(message + "\n")

def backup_file(filepath, log_file_path):
    """Creates a backup of the specified file."""
    backup_path = f"{filepath}{BACKUP_SUFFIX}"
    try:
        shutil.copy(filepath, backup_path)
        log_action(f"Created backup for {filepath} at {backup_path}.", log_file_path)
        return backup_path
    except Exception as e:
        log_action(f"Failed to create backup for {filepath}: {str(e)}", log_file_path)
        return None

def analyze_file_functionality(filepath, log_file_path):
    """Analyzes the provided Python file to determine its purpose and functionality."""
    with open(filepath, "r") as file:
        source_code = file.read()

    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        log_action(f"Syntax error in {filepath}: {e}", log_file_path)
        return "This script could not be fully analyzed due to syntax issues.", "syntax_error_script.py", []

    description_parts = []
    comments = []
    primary_actions = []
    imports = [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)]

    if imports:
        description_parts.append(f"uses libraries like {', '.join(imports)}")
        comments.append("# Importing necessary libraries.")
        if "pandas" in imports or "openpyxl" in imports:
            primary_actions.append("excel")
        if "os" in imports:
            primary_actions.append("files")
        if "xml" in imports:
            primary_actions.append("xml")

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            docstring = ast.get_docstring(node) or "No description available."
            description_parts.append(f"includes function `{node.name}`: {docstring}")
            comments.append(f"# Function `{node.name}`: {docstring}")
            if "parse" in node.name.lower():
                primary_actions.append("parse")
            if "process" in node.name.lower():
                primary_actions.append("process")
            if "update" in node.name.lower():
                primary_actions.append("update")
        elif isinstance(node, ast.ClassDef):
            docstring = ast.get_docstring(node) or "No description available."
            description_parts.append(f"defines class `{node.name}`: {docstring}")
            comments.append(f"# Class `{node.name}`: {docstring}")

    if not description_parts:
        description_parts.append("performs general operations")

    description = "This script " + "; ".join(description_parts) + "."
    content_hash = hashlib.md5(source_code.encode()).hexdigest()[:8]
    concise_name = "_".join(set(primary_actions)) + f"_{content_hash}.py"

    return description, concise_name, comments

def add_header_and_comments(filepath, file_description, comments, log_file_path):
    """Adds a meaningful header and comments to the file."""
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()

        header = f"""\"\"\"\n
Developer: {DEVELOPER_NAME}
Last Modified: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Description: {file_description}\n
\"\"\"\n\n"""

        updated_lines = [header]
        for i, line in enumerate(lines):
            comment = comments[i] if i < len(comments) else None
            updated_lines.append(f"{comment}\n{line}" if comment else line)

        with open(filepath, "w") as f:
            f.writelines(updated_lines)

        log_action(f"Added header and comments to {filepath}.", log_file_path)
    except Exception as e:
        log_action(f"Failed to modify {filepath}: {str(e)}", log_file_path)

def rename_and_save_file(filepath, new_name, log_file_path):
    """Renames the file to a new name and saves it."""
    directory = os.path.dirname(filepath)
    new_path = os.path.join(directory, new_name)
    try:
        shutil.copy(filepath, new_path)
        log_action(f"Copied {filepath} to {new_path}.", log_file_path)
    except Exception as e:
        log_action(f"Failed to copy {filepath} to {new_name}: {str(e)}", log_file_path)

def validate_output(filepath, log_file_path):
    """Validates the processed file to ensure headers and comments are properly added."""
    with open(filepath, "r") as file:
        content = file.read()

    if "Description:" not in content or "[Explain what this line does]" in content:
        log_action(f"Validation failed for {filepath}: Missing description or placeholders remain.", log_file_path)
    else:
        log_action(f"Validation passed for {filepath}.", log_file_path)

def process_file(filepath, log_file_path):
    """Processes a single file."""
    log_action(f"Processing file: {filepath}", log_file_path)

    if not backup_file(filepath, log_file_path):
        log_action(f"Skipping processing for {filepath} due to backup failure.", log_file_path)
        return

    file_description, new_name, comments = analyze_file_functionality(filepath, log_file_path)

    add_header_and_comments(filepath, file_description, comments, log_file_path)
    rename_and_save_file(filepath, new_name, log_file_path)
    validate_output(filepath, log_file_path)

def process_directory(directory):
    """Prompts for directory and processes all eligible Python files."""
    log_file_path = os.path.join(directory, LOG_FILE_NAME)

    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        return

    log_action(f"Starting processing in directory: {directory}", log_file_path)
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                process_file(filepath, log_file_path)
    log_action("Processing complete.", log_file_path)

if __name__ == "__main__":
    directory = input("Enter the directory to process: ").strip()
    process_directory(directory)
