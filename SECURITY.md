# 安全策略

## 支持的版本

我们目前支持以下版本的安全更新：

| 版本 | 支持状态 |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## 报告漏洞

我们非常重视 MiniAgent 项目的安全性。如果你发现了安全漏洞，请按照以下步骤进行报告：

### 私人报告

**请不要在公开的 GitHub Issues 中报告安全漏洞。**

请通过以下方式私下报告安全问题：

1. **发送邮件**: 将详细信息发送至 [your-email@example.com]
2. **GitHub Security**: 使用 GitHub 的私人漏洞报告功能

### 报告内容

请在报告中包含以下信息：

- 漏洞的详细描述
- 重现步骤
- 潜在的影响范围
- 建议的修复方案（如果有）
- 你的联系信息

### 响应时间

我们承诺：

- **24小时内**: 确认收到你的报告
- **48小时内**: 提供初步评估
- **1周内**: 提供详细的修复计划
- **必要时**: 发布安全补丁

### 负责任的披露

我们遵循负责任的披露原则：

1. **给我们时间**: 在公开披露之前，请给我们合理的时间来修复问题
2. **协调发布**: 我们会与你协调漏洞的公开时间
3. **致谢**: 除非你希望保持匿名，否则我们会在修复公告中感谢你的贡献

## 安全最佳实践

### 对于用户

使用 MiniAgent 时，请遵循以下安全最佳实践：

#### API 密钥管理
- **永远不要** 在代码中硬编码 API 密钥
- 使用环境变量存储敏感信息
- 定期轮换 API 密钥
- 限制 API 密钥的权限范围

```bash
# 正确的方式
export OPENAI_API_KEY="your-api-key"

# 错误的方式 - 不要这样做
llm = SimpleLLM(api_key="sk-...")
```

#### 代码执行安全
- **谨慎使用** Python 执行器工具
- 在隔离环境中运行不可信代码
- 限制文件系统访问权限
- 监控代码执行的资源使用

#### 网络安全
- 使用 HTTPS 连接
- 验证 SSL 证书
- 在防火墙后运行生产实例
- 定期更新依赖项

### 对于开发者

如果你在基于 MiniAgent 开发应用，请考虑：

#### 输入验证
```python
# 验证用户输入
def validate_user_input(user_input: str) -> bool:
    # 检查输入长度
    if len(user_input) > 1000:
        return False
    
    # 检查危险命令
    dangerous_patterns = ['rm -rf', 'del /f', '__import__']
    for pattern in dangerous_patterns:
        if pattern in user_input.lower():
            return False
    
    return True
```

#### 沙箱环境
- 在容器中运行代理
- 限制文件系统访问
- 设置资源限制（CPU、内存）
- 使用只读文件系统

#### 日志和监控
- 记录所有工具执行
- 监控异常活动
- 设置告警机制
- 定期审查日志

## 已知限制

### 当前版本的安全限制

1. **代码执行**: Python 执行器没有沙箱保护
2. **文件访问**: 文件编辑器可以访问整个文件系统
3. **命令执行**: Bash 执行器可以运行任意系统命令
4. **内存限制**: 没有内存使用限制

### 风险缓解

在生产环境中使用时，请采取额外的安全措施：

1. **容器化部署**
   ```dockerfile
   # 使用非特权用户
   USER 1000:1000
   
   # 只读根文件系统
   --read-only
   
   # 禁用网络（如果不需要）
   --network=none
   ```

2. **资源限制**
   ```python
   # 设置执行超时
   agent = MiniAgent(llm=llm, max_steps=10)
   
   # 监控执行时间
   import asyncio
   try:
       result = await asyncio.wait_for(
           agent.run(user_input), 
           timeout=60.0
       )
   except asyncio.TimeoutError:
       print("执行超时")
   ```

## 依赖项安全

我们定期审查和更新依赖项：

- 使用 `pip audit` 检查已知漏洞
- 关注依赖项的安全公告
- 及时更新到安全版本

### 检查依赖项安全

```bash
# 检查已知漏洞
pip audit

# 更新到最新版本
pip install --upgrade openai pydantic
```

## 安全版本历史

### v1.0.0
- 初始版本
- 基础的输入验证
- 环境变量配置支持

## 联系信息

如果你有安全相关的问题或建议，请联系：

- **安全邮箱**: [security@example.com]
- **维护者**: [maintainer@example.com]

---

**感谢你帮助保持 MiniAgent 的安全！** 🔒