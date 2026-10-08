"""验证可选 MCP 工具与 MiniAgent 的原生调用路径。"""

import asyncio
from contextlib import asynccontextmanager
from datetime import timedelta
from types import SimpleNamespace

import pytest

pytest.importorskip("mcp")
from mcp.types import CallToolResult, TextContent, Tool

from mini_agent import MiniAgent
from mini_agent.llm import LLMResponse
from mini_agent.parallel_search import PARALLEL_MCP_URL, USER_AGENT, parallel_search
from mini_agent.tools import PythonExecutor, ToolCollection


@pytest.fixture
def server(monkeypatch):
    """记录传输参数和真实 SDK 数据类型；不丢弃 URL 或请求头。"""
    state = SimpleNamespace(calls=[], closed=False, error=None, result=None)
    schema = {"type": "object", "properties": {"urls": {"type": "array"}}}
    state.tools = [
        Tool(name=name, description="Remote " + name, inputSchema=schema)
        for name in ("web_search", "web_fetch")
    ]

    @asynccontextmanager
    async def transport(url, **kwargs):
        state.url = url
        state.transport = kwargs
        try:
            yield ("read", "write", None)
        finally:
            state.closed = True

    class Session:
        def __init__(self, read, write, **kwargs):
            assert (read, write) == ("read", "write")
            state.session = kwargs

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def initialize(self):
            state.initialized = True

        async def list_tools(self):
            assert state.initialized
            return SimpleNamespace(tools=state.tools)

        async def call_tool(self, name, arguments):
            state.calls.append((name, arguments))
            if state.error:
                raise state.error
            return state.result or CallToolResult(
                content=[
                    TextContent(type="text", text="https://docs.python.org/3/"),
                    TextContent(type="text", text="TaskGroup waits for its tasks."),
                ]
            )

    monkeypatch.setattr("mcp.client.streamable_http.streamablehttp_client", transport)
    monkeypatch.setattr("mcp.ClientSession", Session)
    return state


async def test_agent_dispatch_and_transport(server):
    """模型选择 -> agent.act -> ToolCollection -> MCP -> 模型收到来源与摘录。"""

    class ScriptedLLM:
        async def chat(self, messages, system_prompt=None, tools=None):
            if not any(message["role"] == "tool" for message in messages):
                definition = next(
                    t for t in tools if t["function"]["name"] == "parallel_web_search"
                )
                assert (
                    definition["function"]["parameters"] == server.tools[0].inputSchema
                )
                return LLMResponse(
                    content="搜索官方文档",
                    tool_calls=[
                        {
                            "id": "search-1",
                            "function": {
                                "name": "parallel_web_search",
                                "arguments": '{"objective":"TaskGroup",'
                                '"search_queries":["Python TaskGroup documentation"]}',
                            },
                        }
                    ],
                )
            assert "https://docs.python.org/3/" in messages[-1]["content"]
            assert "TaskGroup waits" in messages[-1]["content"]
            return LLMResponse(content="TaskGroup waits for its tasks.")

    agent = MiniAgent(ScriptedLLM())
    defaults = dict(agent.tools.tools)
    async with parallel_search(agent.tools, timeout=12):
        summary = await agent.run("Explain TaskGroup")
        assert "TaskGroup waits" in summary
        search_session = server.calls[0][1]["session_id"]
        result = await agent.tools.execute_tool(
            "parallel_web_fetch",
            urls=["https://docs.python.org/3/"],
            session_id="other",
        )
        assert result.success
        assert server.calls[-1][1]["session_id"] == search_session
        assert server.calls[-1][0] == "web_fetch"
    assert agent.tools.tools == defaults
    assert server.closed
    assert server.url == PARALLEL_MCP_URL
    assert server.transport == {
        "headers": {"User-Agent": USER_AGENT},
        "timeout": 12,
        "sse_read_timeout": 12,
    }
    assert server.session["read_timeout_seconds"] == timedelta(seconds=12)


async def test_errors_structured_output_and_cancellation(server):
    tools = ToolCollection()
    async with parallel_search(tools):
        server.result = CallToolResult(
            content=[], structuredContent={"results": ["source"]}
        )
        result = await tools.execute_tool("parallel_web_fetch", urls=[])
        assert result.success and '"source"' in result.output
        server.result = CallToolResult(
            content=[TextContent(type="text", text="rate limit")], isError=True
        )
        result = await tools.execute_tool("parallel_web_search")
        assert not result.success and result.error == "rate limit"
        server.error = TimeoutError("timed out")
        result = await tools.execute_tool("parallel_web_search")
        assert not result.success and result.error == "timed out"
        server.error = asyncio.CancelledError()
        with pytest.raises(asyncio.CancelledError):
            await tools.execute_tool("parallel_web_search")
    assert server.closed
    assert "parallel_web_search" not in tools.tools


async def test_restore_existing_tool_on_exception(server):
    tools = ToolCollection()
    original = PythonExecutor(name="parallel_web_search")
    tools.register_tool(original)
    with pytest.raises(ValueError, match="body failed"):
        async with parallel_search(tools):
            saved = tools.tools["parallel_web_search"]
            raise ValueError("body failed")
    assert tools.tools["parallel_web_search"] is original
    assert server.closed
    assert not (await saved.execute()).success


async def test_discovery_failure_leaves_collection_unchanged(server):
    tools = ToolCollection()
    defaults = dict(tools.tools)
    server.tools = []
    with pytest.raises(RuntimeError, match="must provide"):
        async with parallel_search(tools):
            pytest.fail("missing tools must fail before registration")
    assert tools.tools == defaults
    assert server.closed


async def test_invalid_timeout(server):
    with pytest.raises(ValueError, match="positive"):
        async with parallel_search(ToolCollection(), timeout=0):
            pytest.fail("zero timeout must be rejected")


async def test_does_not_remove_user_replacement(server):
    tools = ToolCollection()
    replacement = PythonExecutor(name="parallel_web_search")
    async with parallel_search(tools):
        tools.register_tool(replacement)
    assert tools.tools["parallel_web_search"] is replacement
