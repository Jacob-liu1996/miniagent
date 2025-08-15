# MiniAgent 学习指南

## 🎯 学习目标

通过这个最小化的实现，你将掌握：

1. **智能代理的核心原理**
2. **ReAct（推理-行动）模式**
3. **工具调用机制**
4. **LLM集成方法**
5. **异步编程实践**

## 📖 代码学习路径

### 第一阶段：理解数据结构 (`schema.py`)

```python
# 核心概念
Message   # 消息类型：用户、助手、工具
Memory    # 记忆系统：保存对话历史
AgentState # 代理状态：空闲、运行中、完成
```

**关键点：**
- Message类设计了完整的对话流
- Memory管理对话历史和上下文
- 状态管理确保执行流程可控

### 第二阶段：工具系统 (`tools.py`)

```python
class BaseTool(ABC):
    """所有工具的基类"""
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """统一的执行接口"""
        pass
```

**学习重点：**
1. **抽象接口设计**：所有工具都有统一的`execute`方法
2. **OpenAI函数格式**：`to_function_def()`转换为LLM可理解的格式
3. **具体实现**：Python执行、文件操作、命令行执行

### 第三阶段：LLM接口 (`llm.py`)

```python
class SimpleLLM:
    async def chat(self, messages, system_prompt=None, tools=None):
        """与语言模型交互的核心方法"""
```

**核心机制：**
- 构建符合OpenAI API的请求格式
- 处理工具调用响应
- 解析结构化输出

### 第四阶段：代理核心 (`agent.py`)

这是整个系统的核心，实现了ReAct模式：

```python
async def run(self, user_input: str):
    while self.state == AgentState.RUNNING:
        # Think: 分析当前状态，选择行动
        should_continue = await self.think()
        
        # Act: 执行选定的工具
        if should_continue:
            await self.act()
```

**关键流程：**

1. **Think阶段**：
   - 将对话历史发送给LLM
   - LLM分析需要执行什么工具
   - 返回工具调用指令

2. **Act阶段**：
   - 解析工具调用参数
   - 执行具体工具
   - 将结果添加到对话历史

## 🔍 关键设计模式

### 1. 策略模式（Strategy Pattern）
```python
# 不同的工具实现不同的策略
PythonExecutor  # 代码执行策略
FileEditor      # 文件操作策略  
BashExecutor    # 命令行策略
```

### 2. 观察者模式的变种
```python
# Memory系统观察并记录所有交互
self.memory.add_message(message)
```

### 3. 工厂模式的简化版
```python
# ToolCollection管理工具实例
self.tools.execute_tool(name, **kwargs)
```

## 🚀 实际运行流程示例

以"在当前目录创建hello.txt文件"为例：

### 步骤1：用户输入
```
用户: "在当前目录创建一个hello.txt文件，内容是Hello World"
```

### 步骤2：Think阶段
```python
# 代理发送给LLM的消息
messages = [
    {"role": "user", "content": "在当前目录创建一个hello.txt文件，内容是Hello World"}
]

# LLM返回工具调用
tool_calls = [{
    "id": "call_123",
    "type": "function", 
    "function": {
        "name": "file_editor",
        "arguments": '{"action": "write", "path": "hello.txt", "content": "Hello World"}'
    }
}]
```

### 步骤3：Act阶段
```python
# 执行文件编辑工具
result = await tools.execute_tool(
    "file_editor", 
    action="write", 
    path="hello.txt", 
    content="Hello World"
)
# 结果: ToolResult(success=True, output="文件已写入: hello.txt")
```

### 步骤4：结果反馈
```python
# 将工具执行结果添加到对话历史
memory.add_message(Message.tool_message(
    content="文件已写入: hello.txt",
    tool_call_id="call_123"
))
```

## 🔧 扩展练习

### 练习1：添加新工具
创建一个计算器工具：

```python
class Calculator(BaseTool):
    name = "calculator"
    description = "执行数学计算"
    parameters = {
        "type": "object",
        "properties": {
            "expression": {"type": "string", "description": "数学表达式"}
        },
        "required": ["expression"]
    }
    
    async def execute(self, expression: str, **kwargs) -> ToolResult:
        try:
            result = eval(expression)  # 生产环境中需要更安全的实现
            return ToolResult(success=True, output=str(result))
        except Exception as e:
            return ToolResult(success=False, error=str(e))
```

### 练习2：自定义系统提示词
```python
math_prompt = """
你是一个数学助手，专门帮助用户解决数学问题。
当用户询问计算相关问题时，使用calculator工具。
对于复杂问题，可以使用python_execute工具编写程序求解。
"""
```

### 练习3：添加记忆持久化
```python
class PersistentMemory(Memory):
    def save_to_file(self, filename: str):
        """保存对话历史到文件"""
        pass
    
    def load_from_file(self, filename: str):
        """从文件加载对话历史"""
        pass
```


## 📚 进阶学习资源

1. **ReAct论文**：了解推理-行动模式的理论基础
2. **OpenAI Function Calling**：深入理解工具调用机制
3. **LangChain Agent**：学习更复杂的代理框架
4. **AutoGen**：多代理协作的高级实现

## 💡 核心要点总结

1. **ReAct是核心**：Think（思考）+ Act（行动）的循环
2. **工具是能力**：通过工具扩展代理的能力边界
3. **记忆是智能**：上下文管理决定了对话的连贯性
4. **抽象是关键**：统一的接口让系统易于扩展
5. **异步是必须**：现代AI应用离不开异步编程

通过这个最小化实现，你已经掌握了构建智能代理的核心技能！