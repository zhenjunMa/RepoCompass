from agents import function_tool
from gitingest import ingest_async

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