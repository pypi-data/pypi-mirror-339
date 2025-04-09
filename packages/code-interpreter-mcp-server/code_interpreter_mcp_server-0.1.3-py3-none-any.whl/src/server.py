from mcp.server.fastmcp import FastMCP
import traceback


mcp = FastMCP("code-interpreter",dependencies=["mcp[cli]","pandas", "openpyxl"])


@mcp.tool()
def execute_python_code(code_string: str) -> dict:
    """
    执行作为字符串传入的 Python 代码，并返回执行后的本地作用域。

    参数:
        code_string (str): 包含要执行的 Python 代码的字符串。

    返回:
        dict: 如果代码成功执行，返回一个包含执行后本地作用域中所有变量及其值的字典,如果执行过程中发生错误，返回包含错误类型和堆栈跟踪的字符串。

    安全警告:
        执行任意字符串代码存在固有风险。请确保 code_string 来自可信来源。
    """

    # 创建用于执行代码的本地和全局作用域字典
    local_scope = {}
    # 注意：为了安全起见，可以限制全局作用域中可用的内容
    # 例如：global_scope = {"__builtins__": safe_builtins}
    # 这里为了简单演示，我们使用默认的内置函数
    global_scope = {"__builtins__": __builtins__}

    try:
        # 使用 exec 执行代码字符串
        # 代码将在 global_scope 和 local_scope 定义的上下文中执行
        exec(code_string, global_scope, local_scope)
        # 返回执行后本地作用域的内容
        return local_scope
    except Exception as e:
        # 如果执行过程中出现任何异常
        error_message = f"执行代码时发生错误:\n{traceback.format_exc()}"
        # 返回错误信息字符串
        return {"error_message": error_message}
    
if __name__ == "__main__":
    mcp.run()    