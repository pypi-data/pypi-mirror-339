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

def generate_project_structure(root_dir: str, ignore_patterns: list[str]) -> list[str]:
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
        dirnames[:] = [d for d in dirnames if not should_ignore(d, ignore_patterns)]
        # Filter ignored files
        filenames = [f for f in filenames if not should_ignore(f, ignore_patterns)]

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
