"""
MiniAgent 简单测试
"""
import asyncio
from mini_agent import MiniAgent
from mini_agent.tools import PythonExecutor, FileEditor, BashExecutor


async def test_tools():
    """测试工具功能"""
    print("=== 测试工具功能 ===")
    
    # 测试Python执行工具
    python_tool = PythonExecutor()
    result = await python_tool.execute(code="print('Hello from Python tool!')")
    print(f"Python工具测试: {result}")
    
    # 测试文件编辑工具
    file_tool = FileEditor()
    result = await file_tool.execute(action="write", path="test.txt", content="测试内容")
    print(f"文件工具测试: {result}")
    
    result = await file_tool.execute(action="read", path="test.txt")
    print(f"文件读取测试: {result}")
    
    # 测试Bash工具
    bash_tool = BashExecutor()
    result = await bash_tool.execute(command="echo 'Hello from bash!'")
    print(f"Bash工具测试: {result}")


async def test_agent_without_llm():
    """测试代理功能（不依赖真实LLM）"""
    print("\n=== 测试代理结构 ===")
    
    # 创建一个模拟的LLM（不实际调用API）
    class MockLLM:
        async def chat(self, messages, system_prompt=None, tools=None):
            from mini_agent.llm import LLMResponse
            return LLMResponse(content="这是模拟响应，实际使用需要真实的API密钥")
    
    # 创建代理
    mock_llm = MockLLM()
    agent = MiniAgent(mock_llm, name="TestAgent")
    
    print(f"代理名称: {agent.name}")
    print(f"工具数量: {len(agent.tools.tools)}")
    print(f"可用工具: {list(agent.tools.tools.keys())}")
    print(f"初始状态: {agent.state}")


async def main():
    """主测试函数"""
    print("🧪 MiniAgent 功能测试")
    print("注意: 这个测试不需要API密钥，只测试基础功能")
    
    await test_tools()
    await test_agent_without_llm()
    
    print("\n✅ 基础功能测试完成!")
    print("💡 要测试完整功能，请运行 main_mini.py 并设置 OPENAI_API_KEY")


if __name__ == "__main__":
    asyncio.run(main())