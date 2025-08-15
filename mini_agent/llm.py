"""
LLM接口实现
"""
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from pydantic import BaseModel


class LLMResponse(BaseModel):
    """LLM响应结果"""
    content: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None


class SimpleLLM:
    """简化的LLM接口"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini", base_url: str = "https://api.openai.com/v1"):
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model
    
    async def chat(
        self, 
        messages: List[Dict[str, Any]], 
        system_prompt: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> LLMResponse:
        """发送聊天请求"""
        
        # 构建消息列表
        chat_messages = []
        
        # 添加系统消息
        if system_prompt:
            chat_messages.append({"role": "system", "content": system_prompt})
        
        # 添加对话历史
        chat_messages.extend(messages)
        
        # 构建请求参数
        request_params = {
            "model": self.model,
            "messages": chat_messages,
            "temperature": 0.7,
        }
        
        # 如果有工具，添加工具调用参数
        if tools:
            request_params["tools"] = tools
            request_params["tool_choice"] = "auto"
        
        try:
            # 调用OpenAI API
            response = await self.client.chat.completions.create(**request_params)
            
            message = response.choices[0].message
            
            # 解析响应
            result = LLMResponse()
            result.content = message.content
            
            # 解析工具调用
            if message.tool_calls:
                result.tool_calls = []
                for tool_call in message.tool_calls:
                    result.tool_calls.append({
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        }
                    })
            
            return result
            
        except Exception as e:
            print(f"LLM调用错误: {e}")
            return LLMResponse(content=f"LLM调用失败: {str(e)}")