# 微信公众号配置指南

## 前置条件

- ✅ 已认证的订阅号或服务号
- ✅ 公众号管理员权限

## 配置步骤

### 1. 获取 AppID 和 AppSecret

1. 登录微信公众平台：https://mp.weixin.qq.com
2. 进入「设置与开发」→「基本配置」
3. 复制以下信息：
   - **AppID (应用ID)**
   - **AppSecret (应用密钥)** - 点击"重置"后显示，仅显示一次

### 2. 配置 IP 白名单

1. 在「基本配置」页面找到「IP白名单」
2. 添加你的服务器 IP 地址
3. 如果是本地测试，添加本机公网 IP

**获取本机公网 IP：**
```bash
curl -s ifconfig.me
```

### 3. 配置服务器回调（可选）

如果需要接收发布状态通知：

1. 在「基本配置」→「服务器配置」点击「修改配置」
2. 填写：
   - **URL**: `https://your-domain.com/wechat/callback`
   - **Token**: 自定义一个字符串
   - **EncodingAESKey**: 随机生成
   - **消息加解密方式**: 安全模式（推荐）

3. 服务器需要实现验证接口：

```python
# Flask 示例
from flask import Flask, request
import hashlib

app = Flask(__name__)

@app.route('/wechat/callback', methods=['GET', 'POST'])
def wechat_callback():
    if request.method == 'GET':
        # 验证
        token = 'YOUR_TOKEN'
        data = request.args
        signature = data.get('signature')
        timestamp = data.get('timestamp')
        nonce = data.get('nonce')
        echostr = data.get('echostr')
        
        # 验证签名
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = ''.join(tmp_list)
        tmp_str = hashlib.sha1(tmp_str.encode()).hexdigest()
        
        if tmp_str == signature:
            return echostr
        return ''
    
    if request.method == 'POST':
        # 接收事件推送
        xml_data = request.data
        # 解析 XML 处理发布状态
        # ...
        return 'success'
```

### 4. 在 OpenClaw 中配置凭证

**方式一：环境变量**

```bash
# 在 ~/.zshrc 或 ~/.bashrc 中添加
export WECHAT_APPID="wx1234567890abcdef"
export WECHAT_SECRET="your_secret_here"
```

**方式二：OpenClaw 配置文件**

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "env": {
    "WECHAT_APPID": "wx1234567890abcdef",
    "WECHAT_SECRET": "your_secret_here"
  }
}
```

**方式三：.env 文件**

创建 `~/.openclaw/.env`：

```
WECHAT_APPID=wx1234567890abcdef
WECHAT_SECRET=your_secret_here
```

### 5. 验证配置

运行测试命令：

```bash
cd /Users/cgz/.openclaw/workspace/skills/wechat-mp-publish

# 测试获取 token
python scripts/wechat_publisher.py list
```

如果返回草稿列表（可能为空），说明配置成功！

## 常见问题

### Q: 提示 "调用 IP 不在白名单中"

**A:** 确认服务器公网 IP 已添加到公众号后台的 IP 白名单。

### Q: 提示 "AppSecret 错误"

**A:** 重新生成 AppSecret，确保复制时没有多余空格。

### Q: 未认证订阅号能用吗？

**A:** 可以创建草稿，但不能通过 API 发布。需要：
1. API 创建草稿
2. 手动登录公众号后台发布

### Q: 每天能发多少篇文章？

**A:** 
- 订阅号：1 条/天（群发），发布无限制
- 服务号：4 条/月（群发），发布无限制

**发布 vs 群发：**
- 发布：文章出现在历史消息，不推送
- 群发：推送到粉丝聊天列表

## 安全建议

1. **不要把凭证提交到 Git**
   ```bash
   # 添加到 .gitignore
   echo ".env" >> .gitignore
   echo "*secret*" >> .gitignore
   ```

2. **定期更换 AppSecret**
   - 建议每 3-6 个月更换一次

3. **限制 IP 白名单**
   - 只添加必要的服务器 IP
   - 本地测试完成后删除测试 IP
