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
]

# --- Helper Functions ---

def should_ignore(name: str, ignore_patterns: list[str]) -> bool:
    """Checks if a file/folder name matches any ignore pattern."""
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(name, pattern):
            return True
    # Also ignore hidden files/folders starting with '.' unless explicitly allowed
    # (e.g. .github is often kept, but handled by topdown=True filtering)
    # Note: .git is already explicitly ignored above.
    # if name.startswith('.'):
    #     return True # Uncomment this line if you want to ignore ALL hidden items
    return False

# --- Core Structure Generation ---

def generate_project_structure(root_dir: str, ignore_patterns: list[str]=DEFAULT_IGNORE_PATTERNS) -> list[str]:
    """
    Generates the project structure as a list of formatted strings.
    """
    structure_lines = []
    root_dir_abs = os.path.abspath(root_dir)
    root_name = os.path.basename(root_dir_abs)

    # Add the root directory name itself
    structure_lines.append(f"{root_name}/")


    item_count = 0

    for dirpath, dirnames, filenames in os.walk(root_dir_abs, topdown=True):
        # --- Filtering ---
        # Filter ignored directories *in place*. This prevents os.walk from descending
        # into them because we are using topdown=True.
        dirnames[:] = [d for d in dirnames if not should_ignore(d, DEFAULT_IGNORE_PATTERNS)]
        # Filter ignored files
        filenames = [f for f in filenames if not should_ignore(f, DEFAULT_IGNORE_PATTERNS)]

        # Sort for consistent order
        dirnames.sort()
        filenames.sort()

        # --- Calculate Level and Indentation ---
        # Get the path relative to the starting root directory
        relative_dirpath = os.path.relpath(dirpath, root_dir_abs)
        # Calculate depth level
        level = 0 if relative_dirpath == '.' else relative_dirpath.count(os.sep) + 1
        # Indentation uses '│  ' for levels, but not for the connector part
        indent = '│  ' * (level - 1) if level > 0 else ''

        # Combine directories and files for processing
        entries = dirnames + filenames

        for i, name in enumerate(entries):
            item_count += 1
            is_last = (i == len(entries) - 1)
            # Determine connector based on position
            connector = '└── ' if is_last else '├── '

            # Check if it's a directory (we know this because it's in dirnames)
            is_dir = name in dirnames

            # Format the display name (add '/' suffix for directories)
            display_name = name + ('/' if is_dir else '')

            # Construct the line
            line = f"{indent}{connector}{display_name}"
            structure_lines.append(line)


    return structure_lines
