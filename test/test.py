import subprocess


def execute_tree_command(path='.'):
    try:
        # 执行 tree 命令，并使用 subprocess 捕获输出
        result = subprocess.run(['tree', path], capture_output=True, text=True)

        # 打印并返回结果
        if result.returncode == 0:  # 检查命令是否成功执行
            return result.stdout  # 返回命令输出结果
        else:
            return f"错误：{result.stderr}"  # 返回错误信息
    except FileNotFoundError:
        return "错误：系统中未找到 tree 命令，请确保已安装该工具。"
    except Exception as e:
        return f"未知错误：{str(e)}"

if __name__ == '__main__':
    print(execute_tree_command('/Users/user/workspace/'))