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

## 💡 快速体验

MiniAgent 支持多种任务类型：

- **📁 文件操作**：创建、读取、编辑文件
- **🐍 Python代码**：执行Python程序和计算
- **⚡ 命令行**：运行系统命令
- **📊 数据处理**：清洗和转换数据

**示例对话**：
```
用户: "在当前目录创建一个hello.txt文件，内容是Hello World"
代理: 执行文件创建任务...
结果: ✅ 文件创建成功
```

更多示例请查看 [examples.py](examples.py)

## 📚 文档导航

### 🚀 新手必读
- **[README.md](README.md)** - 项目介绍（当前页面）
- **[examples.py](examples.py)** - 使用示例
- **[main_mini.py](main_mini.py)** - 交互模式

### 📖 深入学习
- **[学习指南](docs/learning-guide.md)** - 深入理解架构和原理
- **[项目结构](docs/project-structure.md)** - 完整文件说明

### 🔧 开发相关
- **[贡献指南](CONTRIBUTING.md)** - 参与开发
- **[部署指南](docs/deployment.md)** - GitHub部署
- **[安全策略](SECURITY.md)** - 安全最佳实践
- **[更新日志](CHANGELOG.md)** - 版本历史

## 🎯 核心特色

- **🧠 ReAct模式** - 完整的推理-行动循环
- **🔧 可扩展** - 插件式工具系统
- **📦 轻量级** - 仅400行核心代码
- **🎓 易学习** - 清晰的代码和丰富文档

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