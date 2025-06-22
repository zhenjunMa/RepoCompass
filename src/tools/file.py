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

    with open(file_name, 'r', encoding='utf-8') as file:  # 'r' 代表读取模式，encoding 用于处理文件编码
        content = file.read()  # 读取整个文件内容

    return content

def filtered_tree(directory):
    """
    在指定目录执行过滤后的 tree 命令，保留文件夹、.md 文件和无后缀文件

    参数:
        directory (str/Path): 目标目录路径

    返回:
        str: 命令输出结果
    """
    # 确保目录存在
    directory = Path(directory).resolve()
    if not directory.exists() or not directory.is_dir():
        raise ValueError(f"目录不存在或不是有效目录: {directory}")

    # 构建命令 (安全处理路径)
    cmd = f"tree -F {shlex.quote(str(directory))} | grep -E '/$|\\.md$|^[^.]*$' | sed 's/^\\.$//'"

    try:
        # 执行命令并捕获输出
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            # 设置环境确保使用UTF-8编码
            env={**os.environ, "LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8"}
        )
        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        # 处理可能的错误
        error_msg = f"命令执行失败 (code {e.returncode}):\n"
        error_msg += f"错误信息: {e.stderr.strip() if e.stderr else '无'}"
        raise RuntimeError(error_msg) from e