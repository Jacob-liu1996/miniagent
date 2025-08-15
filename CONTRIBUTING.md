# 贡献指南

感谢你对 MiniAgent 项目的关注！我们欢迎各种形式的贡献，包括但不限于：

- 🐛 报告 Bug
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交代码修复
- 🧪 编写测试用例
- 📚 翻译文档

## 📋 目录

- [行为准则](#行为准则)
- [开始贡献](#开始贡献)
- [报告问题](#报告问题)
- [功能请求](#功能请求)
- [代码贡献](#代码贡献)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [Pull Request 流程](#pull-request-流程)

## 🤝 行为准则

参与此项目即表示你同意遵守我们的行为准则。我们致力于为所有人提供友好、安全和包容的环境。

### 我们的承诺

- 使用友好和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

## 🚀 开始贡献

### 开发环境设置

1. **Fork 仓库**
   ```bash
   # 在 GitHub 上 fork 项目仓库
   ```

2. **克隆你的 fork**
   ```bash
   git clone https://github.com/your-username/mini-agent.git
   cd mini-agent
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements_mini.txt
   ```

4. **设置上游仓库**
   ```bash
   git remote add upstream https://github.com/original-owner/mini-agent.git
   ```

5. **运行测试**
   ```bash
   python test_mini.py
   ```

## 🐛 报告问题

在报告 Bug 之前，请：

1. **搜索现有 Issues** - 确保问题尚未被报告
2. **使用最新版本** - 确认问题在最新版本中仍然存在
3. **提供详细信息** - 包含复现步骤、环境信息等

### Bug 报告模板

```markdown
## Bug 描述
简洁清晰地描述这个 bug

## 复现步骤
1. 进入 '...'
2. 点击 '....'
3. 滚动到 '....'
4. 看到错误

## 期望行为
清晰简洁地描述你期望发生什么

## 实际行为
清晰简洁地描述实际发生了什么

## 环境信息
- 操作系统: [例如 iOS]
- Python 版本: [例如 3.9]
- 项目版本: [例如 1.0.0]

## 附加信息
添加任何其他关于问题的上下文信息、截图等
```

## 💡 功能请求

我们欢迎新功能建议！请：

1. **搜索现有 Issues** - 确保功能尚未被请求
2. **详细描述** - 解释为什么需要这个功能
3. **提供用例** - 描述具体的使用场景

### 功能请求模板

```markdown
## 功能描述
简洁清晰地描述你想要的功能

## 问题背景
这个功能请求是否与某个问题相关？请描述

## 解决方案
清晰简洁地描述你想要实现的解决方案

## 替代方案
清晰简洁地描述你考虑过的任何替代解决方案或功能

## 附加信息
添加任何其他关于功能请求的上下文信息或截图
```

## 🔧 代码贡献

### 贡献流程

1. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **进行更改**
   - 编写代码
   - 添加/更新测试
   - 更新文档

3. **运行测试**
   ```bash
   python test_mini.py
   ```

4. **提交更改**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **推送到你的 fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **创建 Pull Request**

### 代码贡献类型

#### 🐛 Bug 修复
- 修复现有功能中的错误
- 改进错误处理
- 性能优化

#### ✨ 新功能
- 添加新的工具类
- 扩展现有功能
- 改进用户体验

#### 📚 文档改进
- 修正文档错误
- 添加使用示例
- 改进代码注释

#### 🧪 测试
- 添加单元测试
- 改进测试覆盖率
- 添加集成测试

## 📏 代码规范

### Python 代码风格

我们遵循 PEP 8 标准，建议使用以下工具：

```bash
# 代码格式化
pip install black
black .

# 代码检查
pip install flake8
flake8 .

# 类型检查
pip install mypy
mypy .
```

### 代码质量要求

1. **类型提示** - 为函数参数和返回值添加类型提示
2. **文档字符串** - 为类和函数添加清晰的文档字符串
3. **错误处理** - 适当的异常处理和错误信息
4. **测试覆盖** - 为新功能编写测试用例

### 示例代码风格

```python
from typing import Optional, Dict, Any
from pydantic import BaseModel

class ExampleTool(BaseTool):
    """示例工具类
    
    这是一个工具类的示例，展示了标准的代码风格。
    
    Attributes:
        name: 工具名称
        description: 工具描述
    """
    
    name: str = "example_tool"
    description: str = "这是一个示例工具"
    
    async def execute(self, param: str, **kwargs) -> ToolResult:
        """执行工具逻辑
        
        Args:
            param: 输入参数
            **kwargs: 额外参数
            
        Returns:
            ToolResult: 执行结果
            
        Raises:
            ValueError: 当参数无效时抛出
        """
        try:
            # 实现逻辑
            result = self._process_param(param)
            return ToolResult(success=True, output=result)
        except Exception as e:
            return ToolResult(success=False, error=str(e))
    
    def _process_param(self, param: str) -> str:
        """处理参数的私有方法"""
        if not param:
            raise ValueError("参数不能为空")
        return param.upper()
```

## 📝 提交规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

### 提交消息格式

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### 提交类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式修改
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

### 示例

```bash
feat(tools): add web scraping tool
fix(agent): resolve memory leak in conversation history
docs(readme): update installation instructions
test(tools): add unit tests for file editor
```

## 🔄 Pull Request 流程

### PR 检查清单

在提交 PR 之前，请确保：

- [ ] 代码遵循项目的代码规范
- [ ] 所有测试都通过
- [ ] 添加了必要的测试用例
- [ ] 更新了相关文档
- [ ] 提交消息符合规范
- [ ] PR 描述清晰明了

### PR 模板

```markdown
## 变更描述
简洁清晰地描述这个 PR 的变更内容

## 变更类型
- [ ] Bug 修复
- [ ] 新功能
- [ ] 重大变更
- [ ] 文档更新

## 测试
- [ ] 通过现有测试
- [ ] 添加新测试
- [ ] 手动测试完成

## 检查清单
- [ ] 代码遵循项目规范
- [ ] 自我审查了代码
- [ ] 代码有适当的注释
- [ ] 更新了相关文档
- [ ] 变更不会产生新的警告
```

### 审查过程

1. **自动检查** - CI 会自动运行测试和代码检查
2. **代码审查** - 维护者会审查你的代码
3. **反馈处理** - 根据反馈进行必要的修改
4. **合并** - 审查通过后会被合并到主分支

## 🎯 开发指南

### 项目结构

```
mini_agent/
├── mini_agent/          # 核心模块
│   ├── __init__.py     # 模块导出
│   ├── agent.py        # 代理核心
│   ├── llm.py          # LLM 接口
│   ├── schema.py       # 数据结构
│   └── tools.py        # 工具系统
├── examples.py         # 使用示例
├── test_mini.py        # 测试文件
└── main_mini.py        # 主程序
```

### 核心概念

1. **Agent** - 智能代理的核心类
2. **Tool** - 工具的抽象基类
3. **Memory** - 对话记忆管理
4. **LLM** - 语言模型接口

### 常见任务

#### 添加新工具

1. 继承 `BaseTool` 类
2. 实现 `execute` 方法
3. 定义工具的 schema
4. 添加测试用例
5. 更新文档

#### 修改核心逻辑

1. 在 `agent.py` 中进行修改
2. 确保向后兼容性
3. 添加相应测试
4. 更新示例代码

## ❓ 获取帮助

如果你有任何问题，可以：

1. **查看文档** - 检查现有文档是否有答案
2. **搜索 Issues** - 查看是否有类似问题
3. **创建 Issue** - 描述你的问题
4. **参与讨论** - 在 GitHub Discussions 中参与讨论

## 🙏 致谢

感谢所有为 MiniAgent 项目做出贡献的开发者！

---

**记住：每一个贡献都很重要，无论大小！** 🌟