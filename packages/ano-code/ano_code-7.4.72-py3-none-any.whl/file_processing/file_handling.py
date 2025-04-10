import os
import time
import requests
from transformers import GPT2Tokenizer
from yaspin import yaspin
from ai_assistant.llm_cli import groq_client
from ai_assistant.prompt_llm import AIAssistant
from ai_assistant.consts import COMMANDS
import tiktoken
import pathspec
import asyncio

import argparse
import fnmatch
from pathlib import Path


MAX_FILE_READ_BYTES = 10000 # Limit file size read to prevent memory issues and huge LLM prompts
BINARY_EXTENSIONS = { # Set of common binary file extensions to skip reading/commenting
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.tif', '.tiff',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.zip', '.tar', '.gz', '.rar', '.7z',
    '.mp3', '.wav', '.ogg', '.mp4', '.avi', '.mov', '.wmv',
    '.exe', '.dll', '.so', '.dylib', '.class', '.jar',
    '.pyc', '.pyo', '.o', '.a', '.lib',
    '.sqlite', '.db', '.mdb',
    '.woff', '.woff2', '.ttf', '.otf', '.eot',
    '.lockb', # Example: bun.lockb
    '.lock', # Example: yarn.lock (often large, low info content for LLM)
    '.bin', '.dat',
}
DEFAULT_IGNORE_PATTERNS = [
    "node_modules", ".git", "__pycache__", ".venv", "venv", "dist", "build",
    "*.pyc", "*.pyo", "*.egg-info", ".DS_Store", "*.lock", "*.log", ".env*",
    "coverage", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".idea", ".vscode",
]

def parse_gitignore(gitignore_path):
    try:
        with open(gitignore_path, 'r', encoding='utf-8') as gitignore_file:
            patterns = gitignore_file.read().splitlines()
            return pathspec.PathSpec.from_lines('gitwildmatch', patterns)
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error reading .gitignore: {e}")
        return None

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except Exception as e:
        return None

# Count tokens using the appropriate tokenizer
def count_tokens(text):
    encoding = tiktoken.get_encoding("cl100k_base")  # Adjust this for your LLM
    tokens = encoding.encode(text)
    return len(tokens)

# Read folder content and respect .gitignore
def read_file_content(file_path: str):
    # gitignore_path = os.path.join(directory, '.gitignore')
    # spec = parse_gitignore(gitignore_path)

    # extensions = {".py", ".js", ".go", ".ts", ".tsx", ".jsx", ".dart", ".php", "Dockerfile", ".yml"}
    combined_content = ""

    # for root, dirs, files in os.walk(directory):
    #     if spec:
    #         dirs[:] = [d for d in dirs if not spec.match_file(os.path.join(root, d))]
    #     for filename in files:
    #         file_path = os.path.join(root, filename)
    #         if spec and spec.match_file(file_path):
    #             continue
    #         if not filename.endswith(tuple(extensions)):
    #             continue
    try:
        with open(file_path, 'r', encoding='utf-8') as f_content:
            f_c = f_content.read()
            # Check if the file is empty
            if not f_c.strip():
                print(f"Skipping empty file: {file_path}")
                pass
                # Check if the file is too large
            if os.path.getsize(file_path) > 10 * 1024 * 1024:  # 10 MB limit
                print(f"Skipping large file: {file_path}")
                pass
            # Check if the file is a binary file
            if b'\0' in f_c:
                print(f"Skipping binary file: {file_path}")
                pass
            # Check if the file is a symlink
            if os.path.islink(file_path):   
                print(f"Skipping symlink: {file_path}")
                pass
            # Check if the file is a directory
            if os.path.isdir(file_path):
                print(f"Skipping directory: {file_path}")
                pass
            # Check if the file is a socket
            if os.path.isfile(file_path) and os.path.is_socket(file_path):
                print(f"Skipping socket: {file_path}")
                pass
            # Check if the file is a FIFO
            if os.path.isfile(file_path) and os.path.is_fifo(file_path):
                print(f"Skipping FIFO: {file_path}")
                pass
            # Check if the file is a character device
            if os.path.isfile(file_path) and os.path.is_char_device(file_path):
                print(f"Skipping character device: {file_path}")
                pass
            # Check if the file is a block device
            if os.path.isfile(file_path) and os.path.is_block_device(file_path):
                print(f"Skipping block device: {file_path}")
                pass
            comment_dir(file_path, f_c)
    except Exception as e:
            print(f"Could not read file {file_path}: {e}")
    return combined_content


# Prompt the LLM
def prompt(path: str, cmd: str, m_tokens: int):
    loader = yaspin, 350,
    assistant = AIAssistant(groq_client)
    result = assistant.run_assistant(path, cmd)
    return result



def comment_dir(item_path: str):
    content = "No file content, this is not a file"
    
    more_details =""" \n\n Path: '${item_paths}'
    Brief Comment:"""
    cmd = COMMANDS["comment_path"]
    command = "${cmd} ${more_details}"
    prompt(item_path,command, 30)

def comment_file_content(item_path: str, file_content: str):
    content = "No file content, this is not a file"
    if file_content != "":
        content = file_content
    more_details =""" \n\n Path: '${item_paths}'
    File_content: '${file_content}'
    Brief Comment:"""
    cmd = COMMANDS["comment_path"]
    command = "${cmd} ${more_details}"
    prompt(item_path, 30, command)


# Send generated documentation to an API
def send_to_api(api_url, code_doc, repo_id):
    payload = {"code_doc": code_doc, "repo_id": repo_id}
    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            print(f"Successfully sent documentation to API for repo_id '{repo_id}'.")
        else:
            print(f"Failed to send documentation for repo_id '{repo_id}'. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error sending to API: {e}")

import os
import argparse
import fnmatch

# --- Configuration ---

# Default patterns/names to ignore
DEFAULT_IGNORE_PATTERNS = [
    "bin",
    "include",
    "lib",
    "lib64",
    "pyvenv.conf",
    "auto-code-env",
    "node_modules",
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "dist",
    "build",
    "*.pyc",
    "*.pyo",
    "*.egg-info",
    ".DS_Store",
    "*.lock",        # e.g., package-lock.json, yarn.lock, bun.lockb
    "*.log",
    ".env*",         # .env, .env.local, etc.
    "coverage",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".idea",          # JetBrains IDE metadata
    ".vscode",        # VS Code metadata
    "target",         # Rust build directory
    "*.o",            # Compiled object files
    "*.a",            # Static libraries
    "*.so",           # Shared libraries (Linux)
    "*.dll",          # Shared libraries (Windows)
    "*.dylib",        # Shared libraries (macOS)
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.tif', '.tiff',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.zip', '.tar', '.gz', '.rar', '.7z',
    '.mp3', '.wav', '.ogg', '.mp4', '.avi', '.mov', '.wmv',
    '.exe', '.dll', '.so', '.dylib', '.class', '.jar',
    '.pyc', '.pyo', '.o', '.a', '.lib',
    '.sqlite', '.db', '.mdb',
    '.woff', '.woff2', '.ttf', '.otf', '.eot',
    '.lockb', # Example: bun.lockb
    '.lock', # Example: yarn.lock (often large, low info content for LLM)
    '.bin', '.dat',
]

# --- Helper Functions ---

def should_ignore(name: str, ignore_patterns: list[str]) -> bool:
    """Checks if a file/folder name matches any ignore pattern."""
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(name, pattern):
            return True
        if pattern.__contains__(name):
            return False
    # Also ignore hidden files/folders starting with '.' unless explicitly allowed
    # (e.g. .github is often kept, but handled by topdown=True filtering)
    # Note: .git is already explicitly ignored above.
    # if name.startswith('.'):
    #     return True # Uncomment this line if you want to ignore ALL hidden items
    return False

# --- Core Structure Generation ---

      



# --- Helper Functions ---

def should_ignore(name: str, ignore_patterns: list[str]) -> bool:
    """Checks if a file/folder name matches any ignore pattern."""
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(name, pattern):
            return True
    # Optional: Uncomment to ignore all hidden files/folders (starting with '.')
    # if name.startswith('.'):
    #    return True
    return False

# --- Core Recursive JSON Structure Generation ---

def generate_json_structure(
    current_path: str,
) -> dict | None:
    """
    Recursively builds a dictionary representing the directory structure.
    Returns None if the item itself should be ignored.
    """
    if should_ignore(current_path.name, DEFAULT_IGNORE_PATTERNS):
        return None

    if current_path.is_file():
        return {"name": current_path.name, "type": "file"}
    elif current_path.is_dir():
        # Base structure for a directory
        dir_structure = {"name": current_path.name, "type": "directory", "children": []}
        try:
            # Iterate through items, sort alphabetically for consistency
            sorted_contents = sorted(current_path.iterdir(), key=lambda p: p.name.lower())

            for item in sorted_contents:
                child_structure = generate_json_structure(item)
                # Only add child if it wasn't ignored
                if child_structure:
                    dir_structure["children"].append(child_structure)

        except OSError as e:
            # Could add an error node, or just skip if unreadable
            print(f"Warning: Could not access {current_path}. Reason: {e.strerror}", flush=True)
            # Optionally add an error node:
            # dir_structure["children"].append({"name": f"[Error accessing {current_path.name}]", "type": "error", "details": e.strerror})

        return dir_structure
    else:
        # Handle other types like symlinks if necessary, or ignore them
        # print(f"Warning: Skipping item of unknown type: {current_path}")
        return None



def get_files_and_content(directory_path, encoding='utf-8', recursive=True):
    """
    Scans a directory for files, reads their content, and returns a list of dictionaries.

    Args:
        directory_path (str): The path to the directory to scan.
        encoding (str): The encoding to use when reading files. Defaults to 'utf-8'.
                      Common alternatives: 'latin-1', 'cp1252'.
        recursive (bool): Whether to scan subdirectories. Defaults to True.

    Returns:
        list: A list of dictionaries, where each dictionary represents a file
              and contains 'filepath' and either 'content' or 'error'.
              Returns an empty list if the directory doesn't exist or isn't accessible.
    """
    file_data = []

    # Ensure the directory exists
    if not os.path.isdir(directory_path):
        print(f"Error: Directory not found or is not a directory: {directory_path}", file=sys.stderr)
        return []

    print(f"Scanning directory: {directory_path} (Recursive: {recursive})", file=sys.stderr)

    if recursive:
        # Use os.walk for recursive scanning
        for dirpath, _, filenames in os.walk(directory_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                # Make sure it's actually a file (os.walk should only yield files, but double-check)
                if not os.path.isfile(file_path):
                    continue

                file_info = {'filepath': os.path.relpath(file_path, directory_path)} # Use relative path for cleaner output
                try:
                    # Try reading the file content with specified encoding
                    # Using errors='ignore' is a pragmatic choice to avoid crashing on decode errors,
                    # but it means some characters might be lost or replaced silently.
                    # For more control, you might use 'replace' or implement more complex error handling.
                    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                        file_info['content'] = f.read()
                    print(f"  Read: {file_info['filepath']}", file=sys.stderr)
                except PermissionError:
                    file_info['error'] = 'Permission denied'
                    print(f"  Error reading {file_info['filepath']}: Permission denied", file=sys.stderr)
                except UnicodeDecodeError as e:
                    # This might still happen if errors='strict' (default) was used
                    file_info['error'] = f'Encoding error ({encoding}): {e}'
                    print(f"  Error reading {file_info['filepath']}: Encoding error ({encoding})", file=sys.stderr)
                except OSError as e:
                    # Catch potential OS-level errors (e.g., file too large, invalid handle)
                    file_info['error'] = f'OS error reading file: {e}'
                    print(f"  Error reading {file_info['filepath']}: OS error - {e}", file=sys.stderr)
                except Exception as e:
                    # Catch any other unexpected errors during file read
                    file_info['error'] = f'Could not read file: {e}'
                    print(f"  Error reading {file_info['filepath']}: {e}", file=sys.stderr)
                file_data.append(file_info)
    else:
        # Scan only the top-level directory
        try:
            for item_name in os.listdir(directory_path):
                item_path = os.path.join(directory_path, item_name)
                if os.path.isfile(item_path):
                    file_info = {'filepath': os.path.relpath(item_path, directory_path)} # Use relative path
                    try:
                        with open(item_path, 'r', encoding=encoding, errors='ignore') as f:
                            file_info['content'] = f.read()
                        print(f"  Read: {file_info['filepath']}", file=sys.stderr)
                    except PermissionError:
                        file_info['error'] = 'Permission denied'
                        print(f"  Error reading {file_info['filepath']}: Permission denied", file=sys.stderr)
                    except UnicodeDecodeError as e:
                        file_info['error'] = f'Encoding error ({encoding}): {e}'
                        print(f"  Error reading {file_info['filepath']}: Encoding error ({encoding})", file=sys.stderr)
                    except OSError as e:
                         file_info['error'] = f'OS error reading file: {e}'
                         print(f"  Error reading {file_info['filepath']}: OS error - {e}", file=sys.stderr)
                    except Exception as e:
                        file_info['error'] = f'Could not read file: {e}'
                        print(f"  Error reading {file_info['filepath']}: {e}", file=sys.stderr)
                    file_data.append(file_info)
        except PermissionError:
             print(f"Error: Permission denied for listing directory: {directory_path}", file=sys.stderr)
             return [] # Return empty list as we couldn't list the dir
        except Exception as e:
             print(f"Error listing directory {directory_path}: {e}", file=sys.stderr)
             return []

    print(f"Finished scanning. Found {len(file_data)} files.", file=sys.stderr)
    return file_data






def modify_file_content(file_path, new_content, encoding='utf-8', create_dirs=True):
    """
    Overwrites the content of a specified file with new content.

    Args:
        file_path (str): The full path to the file to modify.
        new_content (str): The new string content to write to the file.
        encoding (str): The encoding to use when writing the file. Defaults to 'utf-8'.
        create_dirs (bool): If True, automatically create parent directories
                            if they don't exist. Defaults to True.

    Returns:
        bool: True if the file was successfully written, False otherwise.

    Raises:
        TypeError: If new_content is not a string.
        # Specific OS/IO errors might still propagate if not caught explicitly below
    """
    if not isinstance(new_content, str):
        # Ensure content is a string, as required by f.write() in text mode
        print(f"Error: new_content for '{file_path}' must be a string, not {type(new_content)}.", file=sys.stderr)
        # Optionally raise TypeError("new_content must be a string") instead of returning False
        return False

    try:
        # Optional: Create parent directories if requested and needed
        if create_dirs:
            parent_dir = os.path.dirname(file_path)
            # Check if parent_dir is not empty (e.g., for files in the current dir)
            # and if it doesn't exist
            if parent_dir and not os.path.exists(parent_dir):
                try:
                    os.makedirs(parent_dir)
                    print(f"Info: Created directory '{parent_dir}' for file '{file_path}'.", file=sys.stderr)
                except OSError as e:
                    print(f"Error: Could not create directory '{parent_dir}' for file '{file_path}': {e}", file=sys.stderr)
                    return False # Cannot proceed if directory creation fails

        # Open the file in write mode ('w').
        # This TRUNCATES the file if it exists or CREATES it if it doesn't.
        # Use 'utf-8' encoding by default, crucial for non-ASCII text.
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(new_content)
        # print(f"Successfully wrote content to '{file_path}'.", file=sys.stderr) # Optional success message
        return True

    except PermissionError:
        print(f"Error: Permission denied when trying to write to '{file_path}'.", file=sys.stderr)
        return False
    except IsADirectoryError:
         print(f"Error: The path '{file_path}' points to a directory, not a file.", file=sys.stderr)
         return False
    except FileNotFoundError:
        # This typically happens if create_dirs is False and the directory doesn't exist,
        # or if the path is fundamentally invalid.
         print(f"Error: File or directory not found for path '{file_path}'. Check the path.", file=sys.stderr)
         return False
    except OSError as e:
        # Catch other potential OS-level errors (e.g., disk full, invalid argument)
        print(f"Error: An OS error occurred while writing to '{file_path}': {e}", file=sys.stderr)
        return False
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Error: An unexpected error occurred while modifying '{file_path}': {e}", file=sys.stderr)
        return False

# --- Example Usage ---
if __name__ == "__main__":
    # Create a dummy file for testing
    test_dir = "temp_test_modify"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    file_to_modify = os.path.join(test_dir, "my_test_file.txt")
    initial_content = "This is the original content.\nLine 2."

    # --- Test Case 1: Create and write initial content ---
    print(f"\n--- Test Case 1: Writing initial content to '{file_to_modify}' ---")
    if modify_file_content(file_to_modify, initial_content):
        print(f"Initial content written successfully.")
        try:
            with open(file_to_modify, 'r', encoding='utf-8') as f:
                print(f"Current content:\n---\n{f.read()}---")
        except Exception as e:
             print(f"Could not read back file: {e}")
    else:
        print(f"Failed to write initial content.")


    # --- Test Case 2: Modify existing file ---
    print(f"\n--- Test Case 2: Modifying content of '{file_to_modify}' ---")
    new_content = "This is the NEW content.\nIt completely replaced the old one."
    if modify_file_content(file_to_modify, new_content):
        print(f"Content modified successfully.")
        try:
            with open(file_to_modify, 'r', encoding='utf-8') as f:
                print(f"Current content:\n---\n{f.read()}---")
        except Exception as e:
             print(f"Could not read back file: {e}")
    else:
        print(f"Failed to modify content.")

    # --- Test Case 3: Write to a file in a non-existent directory (with create_dirs=True) ---
    print(f"\n--- Test Case 3: Writing to a new file in a new directory ---")
    new_dir_file = os.path.join(test_dir, "subdir", "another_file.log")
    log_content = "Log entry 1\nLog entry 2"
    if modify_file_content(new_dir_file, log_content, create_dirs=True):
         print(f"Successfully wrote to '{new_dir_file}'.")
         try:
            with open(new_dir_file, 'r', encoding='utf-8') as f:
                print(f"Current content:\n---\n{f.read()}---")
         except Exception as e:
             print(f"Could not read back file: {e}")
    else:
        print(f"Failed to write to '{new_dir_file}'.")

    # --- Test Case 4: Attempt to write to a file in a non-existent directory (with create_dirs=False) ---
    print(f"\n--- Test Case 4: Attempting write with create_dirs=False ---")
    no_create_file = os.path.join(test_dir, "no_subdir", "fail_file.txt")
    if not modify_file_content(no_create_file, "This should fail", create_dirs=False):
        print(f"Successfully caught expected failure for '{no_create_file}'.")
    else:
         print(f"Error: Unexpectedly succeeded writing to '{no_create_file}'.")


    # --- Test Case 5: Attempt to write non-string content ---
    print(f"\n--- Test Case 5: Attempting write with non-string content ---")
    non_string_file = os.path.join(test_dir, "bad_content.txt")
    if not modify_file_content(non_string_file, ["list", "is", "not", "string"]):
        print(f"Successfully caught expected failure for non-string content.")
    else:
         print(f"Error: Unexpectedly succeeded writing non-string content to '{non_string_file}'.")



def delete_file(file_path):
    """
    Deletes a specified file.

    Args:
        file_path (str): The full path to the file to delete.

    Returns:
        bool: True if the file was successfully deleted, False otherwise.
              Returns False if the file didn't exist initially or if the
              path pointed to a directory.
    """
    # 1. Check if the path exists and is a file
    if not os.path.isfile(file_path):
        # Path doesn't exist or it's not a file (e.g., it's a directory)
        if os.path.exists(file_path):
            # It exists, but it's not a file
            print(f"Error: Path '{file_path}' exists but is not a regular file (likely a directory). Cannot delete.", file=sys.stderr)
        else:
            # It doesn't exist at all
            print(f"Error: File not found at '{file_path}'. Cannot delete.", file=sys.stderr)
        return False # Cannot proceed

    # 2. Attempt to delete the file
    try:
        os.remove(file_path)
        # print(f"Successfully deleted file: '{file_path}'", file=sys.stderr) # Optional success message
        return True # Deletion successful

    except PermissionError:
        print(f"Error: Permission denied. Cannot delete '{file_path}'.", file=sys.stderr)
        return False
    except OSError as e:
        # Catch other potential OS-level errors during removal
        # (e.g., file in use on Windows, filesystem errors)
        print(f"Error: OS error deleting file '{file_path}': {e}", file=sys.stderr)
        return False
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Error: An unexpected error occurred deleting '{file_path}': {e}", file=sys.stderr)
        return False
