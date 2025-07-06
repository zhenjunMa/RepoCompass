from datetime import datetime

from agents import function_tool
from git import Repo
from gitingest import ingest_async
from src.config import PROJECT_ROOT

@function_tool()
async def tree(path: str) -> str:
    """Fetch struct for the path

    Args:
        path: The path to execute this function.
    """
    result = ingest_async(path, exclude_patterns="*.css,*.js,*.rs,*.ts,*.wasm,*.toml,*.java,*.py,*.c,*.go,*.env,*.json,*.yaml,*.yml,*.sh,*.proto,*.sum,*.mod,*.mk,*.conf")
    _, directory_struct, _ = await result
    return directory_struct

@function_tool()
def read_file(file_name: str) -> str:
    """Fetch content for the file

    Args:
        file_name: The absolute path for target file.
    """

    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()

    return content

@function_tool()
def get_current_time() -> str:
    """
    Fetches the current system time in ISO 8601 format.

    Returns:
        str: Current timestamp in ISO format (YYYY-MM-DDTHH:MM:SS.microseconds)
        Example: "2023-10-15T14:30:45.123456"
    """
    return datetime.now().isoformat()

@function_tool()
def git_clone_repo(repo_url: str) -> str:
    """
    download repo to local path

    Args:
        repo_url: the url for repo to be analyzed

    Returns:
        the local path for the repo
    """
    project_local_path = PROJECT_ROOT / repo_url.split("/")[-1]
    print("start to download the repo to:" + project_local_path.as_posix())
    if project_local_path.exists() is False:
        Repo.clone_from(repo_url, project_local_path, depth=10)
    else:
        print("repo is existed, so begin to analyze directly...")
    return project_local_path