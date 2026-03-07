#!/bin/bash

echo "🎬 智能剪辑配置系统 - 安装脚本"
echo "================================"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装"
    exit 1
fi

echo "✓ Python版本: $(python3 --version)"

# 创建必要目录
echo ""
echo "📁 创建目录结构..."
mkdir -p /Users/gs/ai-video-system/{configs,core,services,cli,temp}
mkdir -p /Users/gs/Movies/Videos/AI_Output

# 安装Python依赖
echo ""
echo "📦 安装Python依赖..."
pip3 install -r /Users/gs/ai-video-system/requirements.txt

# 检查FFmpeg
echo ""
if command -v ffmpeg &> /dev/null; then
    echo "✓ FFmpeg已安装: $(ffmpeg -version | head -n1)"
else
    echo "⚠️  未找到FFmpeg，建议安装: brew install ffmpeg"
fi

# 检查素材库
echo ""
if [ -d "/Users/gs/3·素材库" ]; then
    echo "✓ 素材库目录存在"
else
    echo "⚠️  素材库目录不存在: /Users/gs/3·素材库"
fi

echo ""
echo "✅ 安装完成！"
echo ""
echo "使用方法:"
echo "  python3 /Users/gs/ai-video-system/cli/edit_video.py --list-profiles"
echo "  python3 /Users/gs/ai-video-system/cli/edit_video.py --input video.mp4 --output result.mp4 --profile 风光片"
