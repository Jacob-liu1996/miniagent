"""
MiniAgent 主运行文件
"""
import asyncio
from mini_agent import MiniAgent
from mini_agent.llm import SimpleLLM


async def main():
    """主函数"""
    # 从环境变量获取API密钥
    # api_key = os.getenv("OPENAI_API_KEY")
    api_key = "your api key"
    if not api_key:
        print("❌ 请设置环境变量 OPENAI_API_KEY")
        print("   export OPENAI_API_KEY='你的API密钥'")
        return
    
    # 创建LLM实例
    llm = SimpleLLM(
        api_key=api_key,
        model="gpt-4o-mini"  # 使用更便宜的模型
    )
    
    # 创建代理
    agent = MiniAgent(
        llm=llm,
        name="MiniAgent",
        max_steps=10
    )
    
    print("🤖 MiniAgent 已启动!")
    print("💡 该Agent支持以下功能:")
    print("   - Python代码执行")
    print("   - 文件读写操作")
    print("   - 命令行执行")
    print("\n例如，你可以输入:")
    print("   '在当前目录创建一个hello.txt文件，内容是Hello World'")
    print("   '列出当前目录的所有文件'")
    print("   '写一个Python程序计算1到100的和'")
    
    # 交互循环
    while True:
        try:
            user_input = input("\n请输入你的任务 (输入 'quit' 退出): ")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 再见!")
                break
            
            if not user_input.strip():
                continue
            
            # 执行任务
            result = await agent.run(user_input)
            print(f"\n📋 执行结果:\n{result}")
            
        except KeyboardInterrupt:
            print("\n👋 程序被中断，再见!")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")


if __name__ == "__main__":
    asyncio.run(main())