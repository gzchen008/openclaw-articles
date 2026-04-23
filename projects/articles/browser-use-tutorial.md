# Browser Use：AI Agent 浏览器自动化神器，让 AI 像人类一样上网

> 🌐 **一句话总结**：Browser Use 是一个专为 AI Agent 设计的浏览器自动化工具，让你的 AI 能够像人类一样浏览网页、填写表单、点击按钮、获取信息。

---

## 🔥 为什么值得关注？

想象一下：你只需要给 AI 一句话指令，它就能自动帮你完成复杂的网页操作——从查询天气、填写求职申请，到帮你网购下单。

**Browser Use** 就是这样一个神器：
- ✅ **专为 AI 优化**：比普通自动化工具快 3-5 倍
- ✅ **支持所有主流 AI**：Claude Code、Cursor、Codex、OpenAI、Gemini、Ollama 本地模型等
- ✅ **开源免费**：核心功能完全免费
- ✅ **生产就绪**：支持云端部署，自动处理认证、Cookie、代理等

---

## 📦 安装教程（5 分钟搞定）

### 1. 环境准备

需要 Python 3.11+，推荐使用 `uv` 进行环境管理：

```bash
# 安装 uv
pip install uv

# 创建虚拟环境
uv venv --python 3.12
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
```

### 2. 安装 Browser Use

```bash
# 安装 browser-use 包
uv pip install browser-use

# 安装 Chromium 浏览器
uvx browser-use install
```

### 3. 配置 API Key

创建 `.env` 文件，添加你的 AI 模型 API Key：

```bash
touch .env
```

根据你想用的模型，添加对应的配置：

**方案 A：使用 Browser Use 官方模型（推荐新手）**
```env
BROWSER_USE_API_KEY=your_api_key_here
```
👉 注册获取 API Key：https://cloud.browser-use.com/new-api-key （新用户送 $10 额度）

**方案 B：使用 OpenAI**
```env
OPENAI_API_KEY=sk-your-key-here
```

**方案 C：使用 Anthropic Claude**
```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**方案 D：使用本地 Ollama 模型（完全免费）**
```bash
# 先安装 Ollama，然后拉取模型
ollama pull llama3.1:8b
```
无需 API Key，完全本地运行！

---

## 🚀 第一个 Agent 程序

创建一个 Python 文件 `first_agent.py`：

```python
import asyncio
from browser_use import Agent, Browser, ChatBrowserUse

async def example():
    # 初始化浏览器
    browser = Browser()
    
    # 使用 Browser Use 官方模型（速度快，价格低）
    llm = ChatBrowserUse()
    
    # 创建 Agent
    agent = Agent(
        task="Find the number of stars of the browser-use repo on GitHub",
        llm=llm,
        browser=browser,
    )
    
    # 运行 Agent
    history = await agent.run()
    print("Task completed!")
    return history

if __name__ == "__main__":
    asyncio.run(example())
```

运行：
```bash
python first_agent.py
```

你会看到 AI 自动打开浏览器，访问 GitHub，搜索 browser-use 仓库，并返回 star 数量！🎉

---

## 🎯 实战示例

### 示例 1：使用 OpenAI GPT-4o

```python
from browser_use import Agent, ChatOpenAI
import asyncio

async def search_news():
    llm = ChatOpenAI(model="gpt-4o")
    
    agent = Agent(
        task="Go to Hacker News and find the top 3 trending tech articles",
        llm=llm
    )
    
    result = await agent.run()
    print(result)

asyncio.run(search_news())
```

### 示例 2：使用 Claude Sonnet

```python
from browser_use import Agent, ChatAnthropic
import asyncio

async def fill_form():
    llm = ChatAnthropic(model="claude-sonnet-4-0")
    
    agent = Agent(
        task="Go to example.com/contact and fill out the contact form with name 'John Doe', email 'john@example.com', and message 'Hello, interested in your product'",
        llm=llm
    )
    
    await agent.run()

asyncio.run(fill_form())
```

### 示例 3：使用本地 Ollama（完全免费）

```python
from browser_use import Agent, ChatOllama
import asyncio

async def local_agent():
    llm = ChatOllama(model="llama3.1:8b")
    
    agent = Agent(
        task="Search for the current weather in Beijing",
        llm=llm
    )
    
    await agent.run()

asyncio.run(local_agent())
```

### 示例 4：带视觉能力的 Agent（看懂网页截图）

```python
from browser_use import Agent, ChatOpenAI
import asyncio

async def vision_agent():
    llm = ChatOpenAI(model="gpt-4o")
    
    agent = Agent(
        task="Go to a product page and tell me what colors are available for the main product",
        llm=llm,
        use_vision=True  # 启用视觉能力
    )
    
    await agent.run()

asyncio.run(vision_agent())
```

---

## 🛠️ CLI 命令行工具

Browser Use 还提供了超方便的 CLI 工具，快速调试和原型开发：

```bash
# 打开网页
browser-use open https://github.com

# 查看当前页面可点击元素
browser-use state

# 点击元素（按索引）
browser-use click 5

# 输入文字
browser-use type "Hello World"

# 截图保存
browser-use screenshot page.png

# 关闭浏览器
browser-use close
```

CLI 会保持浏览器会话，可以在多个命令之间保持状态，非常适合快速测试！

---

## 🤖 支持的 AI 模型

| 提供商 | 推荐模型 | 特点 |
|--------|---------|------|
| **Browser Use** | `ChatBrowserUse()` | 官方优化模型，最快最便宜 |
| **OpenAI** | `gpt-4o`, `o3` | 准确性高 |
| **Anthropic** | `claude-sonnet-4-0` | 推理能力强 |
| **Google** | `gemini-flash-latest` | 速度快 |
| **Ollama** | `llama3.1:8b` | 完全免费本地运行 |
| **Azure** | `gpt-5.1-codex` | 企业级 |
| **AWS Bedrock** | Claude via Bedrock | 云原生 |
| **Groq** | Llama 4 | 超高速度 |
| **DeepSeek** | deepseek-chat | 国产大模型 |

💰 **Browser Use 官方模型价格**（每 1M tokens）：
- 输入：$0.20
- 输出：$2.00
- 新用户赠送 $10 额度！

---

## 🚀 生产环境部署

对于生产环境，Browser Use 提供了 `@sandbox` 装饰器，自动处理：
- ✅ 浏览器基础设施
- ✅ 内存管理
- ✅ 代理轮换
- ✅ 反检测指纹
- ✅ 高并发执行

```python
import asyncio
from browser_use import Browser, sandbox, ChatBrowserUse
from browser_use.agent.service import Agent

@sandbox(cloud_profile_id='your-profile-id')
async def production_task(browser: Browser):
    agent = Agent(
        task="Your authenticated task",
        browser=browser,
        llm=ChatBrowserUse(),
    )
    await agent.run()

if __name__ == "__main__":
    asyncio.run(production_task())
```

---

## 💡 进阶技巧

### 1. 使用模板快速开始

```bash
# 生成默认模板
uvx browser-use init --template default

# 可用模板：
# - default: 最小化配置
# - advanced: 完整配置选项
# - tools: 自定义工具扩展示例
```

### 2. 添加自定义工具

```python
from browser_use import Agent, Tools

# 创建工具集
tools = Tools()

@tools.action(description='Save data to a file')
def save_to_file(filename: str, content: str) -> str:
    with open(filename, 'w') as f:
        f.write(content)
    return f"Saved to {filename}"

# Agent 使用自定义工具
agent = Agent(
    task="Find top 10 GitHub repos and save to repos.txt",
    llm=llm,
    tools=tools,
)
```

### 3. 处理登录状态

```python
from browser_use import Browser, BrowserConfig

# 使用真实浏览器配置（复用已有登录状态）
browser = Browser(
    config=BrowserConfig(
        chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    )
)
```

---

## 🔗 相关链接

- **GitHub**: https://github.com/browser-use/browser-use
- **官方文档**: https://docs.browser-use.com
- **云服务**: https://cloud.browser-use.com
- **示例代码**: https://github.com/browser-use/browser-use/tree/main/examples

---

## 📝 总结

Browser Use 是目前最成熟的 AI Agent 浏览器自动化方案之一：

1. **对新手友好**：5 分钟安装，一行代码运行
2. **对专业用户强大**：支持自定义工具、生产级部署
3. **成本可控**：从免费本地模型到高性价比云服务
4. **生态完善**：CLI、Python SDK、云原生支持一应俱全

无论你是想自动化日常网页操作，还是构建复杂的 AI Agent 工作流，Browser Use 都值得一试！

---

*如果这篇文章对你有帮助，欢迎点赞收藏转发！有问题可以在评论区留言交流 🙌*
