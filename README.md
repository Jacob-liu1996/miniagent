# MiniAgent

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-black.svg)

一个轻量级的智能代理框架，实现完整的 ReAct（推理-行动）模式

[✨ 特性](#特性) • [📦 安装](#安装) • [🚀 快速开始](#快速开始) • [📚 文档](#文档) • [🤝 贡献](#贡献)

</div>

---

## 📖 项目简介

MiniAgent 是一个轻量级的智能代理框架，实现了完整的 ReAct（推理-行动）模式和工具调用机制。项目采用简洁的架构设计，用约400行代码提供了智能代理的核心功能。这个项目旨在帮助开发者快速理解智能代理的核心概念和实现原理，并提供一个可扩展的基础平台。

## ✨ 特性

- 🧠 **ReAct模式**: 完整实现推理-行动循环
- 🔧 **工具系统**: 可扩展的插件式工具架构
- ⚡ **异步编程**: 基于现代Python异步框架
- 📦 **轻量级**: 仅约400行核心代码，依赖极简
- 🎓 **教育友好**: 清晰的代码结构，丰富的注释和示例
- 🔌 **易扩展**: 简单易用的工具开发接口

## 📦 安装

### 环境要求

- Python 3.8+
- OpenAI API Key

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/Jacob-liu1996/miniagent.git
   cd miniagent
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **设置API密钥**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

## 🚀 快速开始

### 交互模式

```bash
python main_mini.py
```

### 运行示例

```bash
python examples.py
```

### 基础用法

```python
import asyncio
from mini_agent import MiniAgent, SimpleLLM

async def main():
    # 创建LLM实例
    llm = SimpleLLM(api_key="your-api-key", model="gpt-4o-mini")
    
    # 创建代理
    agent = MiniAgent(llm=llm, name="MyAgent")
    
    # 执行任务
    result = await agent.run("在当前目录创建一个hello.txt文件")
    print(result)

asyncio.run(main())
```

## 🏗️ 核心架构

```
mini_agent/
├── schema.py          # 数据结构定义 (Message, Memory, AgentState)
├── tools.py           # 工具系统 (BaseTool, 具体工具实现)
├── llm.py             # LLM接口 (SimpleLLM)
├── agent.py           # 智能代理核心 (MiniAgent)
└── __init__.py        # 模块导出
```

### 核心组件

1. **Message & Memory**: 消息和记忆系统
2. **BaseTool**: 工具基类和具体工具实现
3. **SimpleLLM**: 简化的语言模型接口
4. **MiniAgent**: 核心代理类，实现ReAct模式

## 💡 使用示例

### 支持的任务类型

<details>
<summary>📁 文件操作</summary>

- "列出当前目录的所有文件"
- "创建一个名为test.txt的文件，内容是Hello World"
- "读取config.json文件的内容"

</details>

<details>
<summary>🐍 Python代码执行</summary>

- "用Python计算1到100的和"
- "生成一个1到10的随机数列表"
- "创建一个函数计算圆的面积"

</details>

<details>
<summary>⚡ 命令行操作</summary>

- "查看当前系统的Python版本"
- "列出所有正在运行的进程"
- "创建一个新目录"

</details>

<details>
<summary>📊 数据处理</summary>

- "清洗文本文件中的空行和多余空格"
- "统计文件中单词的数量"
- "将CSV数据转换为JSON格式"

</details>

## 🔧 核心原理解析

### ReAct 执行循环

MiniAgent 使用 ReAct（推理-行动）模式：

```python
while self.state == AgentState.RUNNING and self.current_step < self.max_steps:
    # Think: 分析当前状态，选择工具
    should_continue = await self.think()
    
    # Act: 执行选定的工具
    if should_continue:
        await self.act()
```

### 工具调用流程

1. **工具注册**: 每个工具实现`BaseTool`接口
2. **函数定义**: 工具转换为OpenAI函数调用格式
3. **LLM选择**: 语言模型根据任务选择合适工具
4. **工具执行**: 代理执行工具并获取结果
5. **结果反馈**: 将结果添加到对话历史中

### 内置工具

| 工具名称 | 功能描述 | 参数 |
|---------|---------|------|
| `python_execute` | 执行Python代码 | `code`: 要执行的代码 |
| `file_editor` | 文件操作 | `action`: read/write/list<br>`path`: 文件路径<br>`content`: 文件内容(写入时) |
| `bash_execute` | 执行命令行 | `command`: 要执行的命令 |

## 🔨 扩展开发

### 添加新工具

```python
from mini_agent.tools import BaseTool, ToolResult

class MyCustomTool(BaseTool):
    name = "my_tool"
    description = "我的自定义工具"
    parameters = {
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "参数1"}
        },
        "required": ["param1"]
    }
    
    async def execute(self, param1: str, **kwargs) -> ToolResult:
        # 实现你的逻辑
        return ToolResult(success=True, output="执行成功")

# 注册工具
agent.tools.register_tool(MyCustomTool())
```

### 自定义系统提示词

```python
custom_prompt = """
你是一个专门处理数据分析的AI助手。
当用户询问数据相关问题时，优先使用Python工具进行分析。
"""

agent = MiniAgent(llm=llm, system_prompt=custom_prompt)
```

## 📚 文档

- 📋 [项目文件清单](PROJECT_FILES.md)
- 📖 [学习指南](LEARNING_GUIDE.md)
- 🤝 [贡献指南](CONTRIBUTING.md)

## 🎯 学习价值

MiniAgent 保留了智能代理系统的核心概念：

1. **ReAct模式**: 思考-行动循环
2. **工具抽象**: 统一的工具接口
3. **记忆系统**: 对话历史管理
4. **状态管理**: 代理执行状态
5. **异步编程**: 现代Python异步模式

## 🤝 贡献

我们欢迎各种形式的贡献！请查看 [贡献指南](CONTRIBUTING.md) 了解详细信息。

### 贡献方式

- 🐛 报告 Bug
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交代码修复
- ⭐ 给项目点星星

### 开发设置

```bash
# 克隆仓库
git clone https://github.com/Jacob-liu1996/miniagent.git
cd miniagent

# 安装依赖
pip install -r requirements.txt

# 运行测试
python test_mini.py
```

## 📄 许可证

本项目基于 [MIT License](LICENSE) 开源。

## 🌟 Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=Jacob-liu1996/miniagent&type=Date)](https://star-history.com/#Jacob-liu1996/miniagent&Date)

---

<div align="center">

**如果这个项目对你有帮助，请给它一个 ⭐️**

Made with ❤️ by MiniAgent Contributors

</div>