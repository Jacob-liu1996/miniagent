"""可选的匿名 Parallel Search MCP 工具，使用 Streamable HTTP。"""

import json
from contextlib import asynccontextmanager
from datetime import timedelta
from typing import Any, AsyncIterator, Dict
from uuid import uuid4

from pydantic import PrivateAttr

from mini_agent.tools import BaseTool, ToolCollection, ToolResult

PARALLEL_MCP_URL = "https://search.parallel.ai/mcp"
USER_AGENT = "miniagent/1.0.0 (Parallel Search MCP)"


class ParallelTool(BaseTool):
    """将服务器提供的工具 schema 和执行结果转换为 MiniAgent 格式。"""

    _session: Any = PrivateAttr()
    _remote_name: str = PrivateAttr()
    _session_id: str = PrivateAttr()
    _active: bool = PrivateAttr(default=True)

    async def execute(self, **kwargs: Any) -> ToolResult:
        """调用 MCP 工具；保留文本、结构化输出及服务器错误。"""
        if not self._active:
            return ToolResult(success=False, error="Parallel MCP connection is closed")
        try:
            arguments = dict(kwargs, session_id=self._session_id)
            result = await self._session.call_tool(self._remote_name, arguments)
            text = "\n".join(
                block.text for block in result.content if block.type == "text"
            )
            if not text and result.structuredContent is not None:
                text = json.dumps(result.structuredContent, ensure_ascii=False)
            if result.isError:
                return ToolResult(success=False, error=text or "Parallel MCP error")
            return ToolResult(success=True, output=text)
        except Exception as exc:
            return ToolResult(success=False, error=str(exc))


@asynccontextmanager
async def parallel_search(
    tools: ToolCollection, timeout: float = 60.0
) -> AsyncIterator[None]:
    """在上下文内注册搜索/抓取工具，退出时关闭连接并恢复原工具。

    需要 Python 3.10+ 和 ``pip install '.[parallel]'``。每个上下文对应一个
    会话，不读取 API key 或 OAuth 配置。连接及发现失败会向调用者抛出异常；
    工具调用失败返回 ToolResult。取消操作继续向上传播。
    """
    from mcp import ClientSession
    from mcp.client.streamable_http import streamablehttp_client

    if timeout <= 0:
        raise ValueError("timeout must be positive")
    registered: Dict[str, ParallelTool] = {}
    previous: Dict[str, BaseTool] = {}
    session_id = uuid4().hex
    async with streamablehttp_client(
        PARALLEL_MCP_URL,
        headers={"User-Agent": USER_AGENT},
        timeout=timeout,
        sse_read_timeout=timeout,
    ) as (read, write, _):
        async with ClientSession(
            read, write, read_timeout_seconds=timedelta(seconds=timeout)
        ) as session:
            await session.initialize()
            discovered = await session.list_tools()
            available = {tool.name: tool for tool in discovered.tools}
            if not {"web_search", "web_fetch"}.issubset(available):
                raise RuntimeError("Parallel MCP must provide web_search and web_fetch")
            try:
                for remote_name in ("web_search", "web_fetch"):
                    remote = available[remote_name]
                    tool = ParallelTool(
                        name="parallel_" + remote_name,
                        description=remote.description or remote_name,
                        parameters=remote.inputSchema,
                    )
                    tool._session = session
                    tool._remote_name = remote_name
                    tool._session_id = session_id
                    if tool.name in tools.tools:
                        previous[tool.name] = tools.tools[tool.name]
                    registered[tool.name] = tool
                    tools.register_tool(tool)
                yield
            finally:
                for name, tool in registered.items():
                    tool._active = False
                    if tools.tools.get(name) is tool:
                        if name in previous:
                            tools.tools[name] = previous[name]
                        else:
                            del tools.tools[name]
