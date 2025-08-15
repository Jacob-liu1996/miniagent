"""
工具系统实现
"""
import os
import subprocess
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel


class ToolResult(BaseModel):
    """工具执行结果"""
    success: bool = True
    output: str = ""
    error: str = ""


class BaseTool(ABC, BaseModel):
    """工具基类"""
    name: str
    description: str
    parameters: Dict[str, Any]
    
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """执行工具"""
        pass
    
    def to_function_def(self) -> Dict[str, Any]:
        """转换为OpenAI函数调用格式"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }


class PythonExecutor(BaseTool):
    """Python代码执行工具"""
    name: str = "python_execute"
    description: str = "执行Python代码并返回结果"
    parameters: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "要执行的Python代码"
            }
        },
        "required": ["code"]
    }
    
    async def execute(self, code: str, **kwargs) -> ToolResult:
        try:
            # 简化版本：使用exec执行代码
            local_vars = {}
            global_vars = {"__builtins__": __builtins__}
            
            # 捕获输出
            import io
            import sys
            old_stdout = sys.stdout
            sys.stdout = mystdout = io.StringIO()
            
            try:
                exec(code, global_vars, local_vars)
                output = mystdout.getvalue()
            finally:
                sys.stdout = old_stdout
            
            return ToolResult(success=True, output=output)
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class FileEditor(BaseTool):
    """文件编辑工具"""
    name: str = "file_editor"
    description: str = "查看、创建和编辑文件"
    parameters: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["read", "write", "list"],
                "description": "操作类型：read(读取), write(写入), list(列出目录)"
            },
            "path": {
                "type": "string",
                "description": "文件或目录路径"
            },
            "content": {
                "type": "string",
                "description": "写入时的文件内容"
            }
        },
        "required": ["action", "path"]
    }
    
    async def execute(self, action: str, path: str, content: str = "", **kwargs) -> ToolResult:
        try:
            if action == "read":
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return ToolResult(success=True, output=content)
            
            elif action == "write":
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return ToolResult(success=True, output=f"文件已写入: {path}")
            
            elif action == "list":
                if os.path.isdir(path):
                    files = os.listdir(path)
                    output = "\n".join(files)
                    return ToolResult(success=True, output=output)
                else:
                    return ToolResult(success=False, error="路径不是目录")
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class BashExecutor(BaseTool):
    """命令行执行工具"""
    name: str = "bash_execute"
    description: str = "执行bash命令"
    parameters: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "要执行的bash命令"
            }
        },
        "required": ["command"]
    }
    
    async def execute(self, command: str, **kwargs) -> ToolResult:
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return ToolResult(success=True, output=result.stdout)
            else:
                return ToolResult(success=False, error=result.stderr)
                
        except subprocess.TimeoutExpired:
            return ToolResult(success=False, error="命令执行超时")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class ToolCollection:
    """工具集合管理"""
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        
        # 注册默认工具
        self.register_tool(PythonExecutor())
        self.register_tool(FileEditor())
        self.register_tool(BashExecutor())
    
    def register_tool(self, tool: BaseTool):
        """注册工具"""
        self.tools[tool.name] = tool
    
    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """获取所有工具的函数定义"""
        return [tool.to_function_def() for tool in self.tools.values()]
    
    async def execute_tool(self, name: str, **kwargs) -> ToolResult:
        """执行指定工具"""
        if name not in self.tools:
            return ToolResult(success=False, error=f"工具 {name} 不存在")
        
        tool = self.tools[name]
        return await tool.execute(**kwargs)