# Parallel 网页搜索与内容提取

MiniAgent 可以通过可选的 `BaseTool` 集成使用
[Parallel Search MCP](https://docs.parallel.ai/integrations/mcp/search-mcp)。
它通过 Streamable HTTP 连接 `https://search.parallel.ai/mcp`，提供
`parallel_web_search` 和 `parallel_web_fetch`，使用服务器返回的参数 schema。
原有的 Python、文件和 Bash 工具保持不变。

## 安装

此可选集成需要 **Python 3.10+**；MiniAgent 核心的 Python 要求不变。
在仓库根目录安装：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install '.[parallel]'
```

Parallel 匿名端点无需 API key，不读取本地凭据。免费额度有速率限制，适用于
探索和轻量使用；匿名搜索使用服务器管理的 `fast` 模式。LLM 推理单独计费，
下面的代理示例仍需要 `OPENAI_API_KEY`。

## 在代理中启用

```python
import asyncio
import os

from mini_agent import MiniAgent, SimpleLLM
from mini_agent.parallel_search import parallel_search


async def main():
    agent = MiniAgent(
        SimpleLLM(api_key=os.environ["OPENAI_API_KEY"], model="gpt-4o-mini"),
        system_prompt=(
            "你是研究助手。使用 parallel_web_search 搜索网页，"
            "必要时使用 parallel_web_fetch 提取内容。回答时附上来源 URL。"
        ),
    )
    async with parallel_search(agent.tools):
        print(await agent.run("查找 Python asyncio TaskGroup 的官方文档并解释用途"))


asyncio.run(main())
```

将代码保存为 `parallel_example.py`，设置 `OPENAI_API_KEY` 后运行
`python parallel_example.py`。工具只在 `async with` 内可用；整个 `agent.run`
必须在该上下文内执行。每个上下文使用一个稳定的搜索会话标识，退出时关闭连接
并恢复同名的已有工具。不要在多个并发代理之间共享同一个工具集合。

## 直接调用（不需要 LLM key）

```python
import asyncio

from mini_agent.parallel_search import parallel_search
from mini_agent.tools import ToolCollection


async def main():
    tools = ToolCollection()
    async with parallel_search(tools, timeout=60):
        search = await tools.execute_tool(
            "parallel_web_search",
            objective="查找 Python asyncio TaskGroup 官方文档",
            search_queries=["Python asyncio TaskGroup documentation"],
        )
        print(search.output if search.success else search.error)
        page = await tools.execute_tool(
            "parallel_web_fetch",
            urls=["https://docs.python.org/3/library/asyncio-task.html"],
            objective="TaskGroup 的用途",
        )
        print(page.output if page.success else page.error)


asyncio.run(main())
```

`ToolResult.output` 保留服务器文本（包括来源 URL 和摘录），服务器错误或调用异常
通过 `success=False` 和 `error` 返回。连接或工具发现失败会抛出异常；取消不会
转换成普通工具错误。`timeout`（秒，默认 60）限制 HTTP 读取和 MCP 响应等待。
此集成仅支持 Streamable HTTP，不使用 stdio 或 OAuth。

## 测试

```bash
python -m pip install pytest pytest-asyncio
python -m pytest tests/test_parallel_search.py
```

测试使用模拟 MCP 会话和脚本化 LLM，验证工具注册、代理调用、输出、错误及清理。
它们不调用付费 LLM，也不依赖在线搜索结果。
