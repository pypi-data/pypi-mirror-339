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

# Main function with rate limiting


def should_ignore(name: str, ignore_patterns: list[str] = DEFAULT_IGNORE_PATTERNS) -> bool:
    """Checks if a file/folder name matches any ignore pattern."""
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(name, pattern):
            return True
    return False




def generate_structure(root_dir: str, ignore_patterns: list[str]) -> str:
    """
    Generates the project structure string with comments based on
    directory paths or file content.
    """
    structure = []
    root_dir_abs = os.path.abspath(root_dir)
    root_name = os.path.basename(root_dir_abs)

    # --- Comment for Root Directory ---
    root_comment = ""
    try:
        # Use root_name + '/' for consistency with path format
        root_comment = comment_dir(root_name + '/')
    except Exception as e:
            print(f"\n[Warning] Failed to get LLM comment for root dir '{root_name}/': {e}")
            root_comment = "[LLM Error]"
    else:
        root_comment = f"[Placeholder Dir Comment: {root_name}/]"

    structure.append(f"{root_name}/" + (f" # {root_comment}" if root_comment else ""))


    item_count = 0

    for dirpath, dirnames, filenames in os.walk(root_dir_abs, topdown=True):
        # --- Filtering ---
        dirnames[:] = [d for d in dirnames if not should_ignore(d, ignore_patterns)]
        filenames = [f for f in filenames if not should_ignore(f, ignore_patterns)]
        dirnames.sort()
        filenames.sort()

        # --- Calculate Level and Prefix ---
        relative_dirpath = os.path.relpath(dirpath, root_dir_abs)
        level = 0 if relative_dirpath == '.' else relative_dirpath.count(os.sep) + 1
        indent = '│  ' * level

        items = dirnames + filenames

        for i, name in enumerate(items):
            item_count += 1
            if item_count % 10 == 0:
                print(f"Processing item {item_count}...", end='\r', flush=True)

            is_last = (i == len(items) - 1)
            connector = '└── ' if is_last else '├── '

            # --- Determine Paths and Type ---
            full_path = os.path.join(dirpath, name)
            is_dir = os.path.isdir(full_path) # More reliable than checking 'name in dirnames' after filtering

            if relative_dirpath == '.':
                relative_path = name
            else:
                relative_path = os.path.join(relative_dirpath, name).replace(os.sep, '/')

            display_name = name + ('/' if is_dir else '')
            llm_path_context = relative_path + ('/' if is_dir else '')

            # --- Get Comment (Conditional Logic) ---
            comment = ""
            try:
                if is_dir:
                    comment = comment_dir(llm_path_context)
                else: # It's a file
                    try:
                        content = read_file_content(llm_path_context)
                        comment = comment_file_content(llm_path_context, content)
                    except FileNotFoundError:
                        comment = "[Error: File not found during read]"
                        

            except Exception as e: # Catch errors during LLM calls
                print(f"\n[Warning] Failed to get LLM comment for '{llm_path_context}': {e}")
                comment = "[LLM Error]"
        else: # Not using LLM, use placeholders
            if is_dir:
                # comment = comment_dir(llm_path_context)
                print(llm_path_context)
                
            else:
                # content = read_file_content(llm_path_context)
                print(llm_path_context)
                # comment = comment_file_content(content, llm_path_context)
            # --- Append to Structure ---
        line = f"{indent}{connector}{display_name}"
        if comment: # Only add comment if it's not empty
            line += f" # {comment}"
        structure.append(line)

    print(f"\nTraversal complete. Processed {item_count} items.", flush=True)
    return "\n".join(structure)


generate_structure("./", ["__pycache__", ".venv", "venv", "dist", "build", ".DS_Store", "*.lock", "*.log", ".env*", "coverage", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".idea", ".vscode"])
