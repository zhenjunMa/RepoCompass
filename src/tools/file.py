import os
import shlex
import subprocess
from pathlib import Path

from agents import function_tool

@function_tool()
def tree(path: str) -> str:
    """Fetch struct for the path, use 'tree' command

    Args:
        path: The path to execute this function.
    """

    return filtered_tree(path)

@function_tool()
def read_file(file_name: str) -> str:
    """Fetch content for the file

    Args:
        file_name: The absolute path for target file.
    """

    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()

    return content

def filtered_tree(directory):
    """
    Executes a filtered tree command in the specified directory, retaining folders, .md files, and files without extensions.

    Parameters:
        directory (str/Path): The path to the target directory.

    Returns:
        str: The output of the command.
    """

    directory = Path(directory).resolve()
    if not directory.exists() or not directory.is_dir():
        raise ValueError(f"Directory does not exist or is not a valid directory: {directory}")

    cmd = f"tree -F {shlex.quote(str(directory))} | grep -E '/$|\\.md$|^[^.]*$' | sed 's/^\\.$//'"

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env={**os.environ, "LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8"}
        )
        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        error_msg = f"Command execution failed (code {e.returncode}):\n"
        error_msg += f"Error message: {e.stderr.strip() if e.stderr else 'None'}"
        raise RuntimeError(error_msg) from e