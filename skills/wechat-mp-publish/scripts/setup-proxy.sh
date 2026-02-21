#!/bin/bash
# 快速配置微信公众号代理的环境变量脚本

echo "🔧 微信公众号代理配置"
echo "====================="
echo ""

# 提示输入服务器 IP
echo "请输入你的代理服务器地址（如：http://115.191.30.195/wechat）："
read -p "代理地址: " PROXY_URL

if [ -z "$PROXY_URL" ]; then
    echo "❌ 代理地址不能为空"
    exit 1
fi

# 检测当前 shell
SHELL_TYPE=""
if [ -n "$ZSH_VERSION" ]; then
    SHELL_TYPE="zsh"
    CONFIG_FILE="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_TYPE="bash"
    CONFIG_FILE="$HOME/.bashrc"
else
    echo "❌ 不支持的 shell 类型"
    exit 1
fi

echo ""
echo "📋 配置信息："
echo "  Shell 类型: $SHELL_TYPE"
echo "  配置文件: $CONFIG_FILE"
echo "  代理地址: $PROXY_URL"
echo ""
echo "使用方式："
echo "  原微信 API: https://api.weixin.qq.com/cgi-bin/token"
echo "  换成代理:   ${PROXY_URL}/cgi-bin/token"
echo ""
echo "  规律：把 https://api.weixin.qq.com 替换成 $PROXY_URL 即可"
echo ""

# 添加环境变量到配置文件
echo "✅ 添加环境变量..."

# 检查是否已存在配置
if grep -q "WECHAT_USE_PROXY" "$CONFIG_FILE"; then
    echo "⚠️  检测到已有配置，将更新..."
    # 更新现有配置
    sed -i.bak "s|export WECHAT_USE_PROXY=.*|export WECHAT_USE_PROXY=true|" "$CONFIG_FILE"
    sed -i.bak "s|export WECHAT_PROXY_URL=.*|export WECHAT_PROXY_URL=\"$PROXY_URL\"|" "$CONFIG_FILE"
else
    # 添加新配置
    echo "" >> "$CONFIG_FILE"
    echo "# 微信公众号代理配置" >> "$CONFIG_FILE"
    echo "export WECHAT_USE_PROXY=true" >> "$CONFIG_FILE"
    echo "export WECHAT_PROXY_URL=\"$PROXY_URL\"" >> "$CONFIG_FILE"
fi

echo "✅ 配置已添加到 $CONFIG_FILE"
echo ""

# 询问是否立即生效
read -p "是否立即生效？(y/n): " NOW_EFFECT

if [ "$NOW_EFFECT" = "y" ] || [ "$NOW_EFFECT" = "Y" ]; then
    echo "🔄 重新加载配置..."
    source "$CONFIG_FILE"
    echo "✅ 配置已生效！"
else
    echo "⚠️  请手动执行以下命令使配置生效："
    echo "  source $CONFIG_FILE"
fi

echo ""
echo "🎉 配置完成！"
echo ""
echo "📝 使用方法："
echo "  cd /Users/cgz/.openclaw/workspace/skills/wechat-mp-publish/scripts"
echo "  python3 wechat_publisher.py list"
echo ""
echo "🔧 如需关闭代理："
echo "  export WECHAT_USE_PROXY=false"
echo ""
echo "🧪 测试代理："
echo "  curl http://115.191.30.195/health"
echo "  curl \"http://115.191.30.195/wechat/cgi-bin/token?grant_type=client_credential&appid=test&secret=test\""
