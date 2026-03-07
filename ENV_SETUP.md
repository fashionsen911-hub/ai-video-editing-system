# 环境变量配置指南

## 设置方法

### 方法1：使用.env文件（推荐）

1. 复制模板文件：
```bash
cp .env.example .env
```

2. 编辑.env文件，填入你的API key：
```bash
nano .env
```

3. 在Python代码中加载（已集成）：
```python
from dotenv import load_dotenv
load_dotenv()
```

### 方法2：直接设置环境变量

```bash
# 临时设置（当前终端有效）
export VOLCENGINE_API_KEY='your-key-here'
export ANTHROPIC_API_KEY='your-key-here'

# 永久设置（添加到~/.zshrc）
echo 'export VOLCENGINE_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

## 需要的API Key

### 火山方舟（必需，用于视频分析）
- 变量名：`VOLCENGINE_API_KEY`
- 获取地址：https://console.volcengine.com/ark

### Claude API（可选，用于AI策划）
- 变量名：`ANTHROPIC_API_KEY`
- 获取地址：https://console.anthropic.com

## 验证配置

```bash
python3 -c "import os; print('VOLCENGINE_API_KEY:', 'OK' if os.getenv('VOLCENGINE_API_KEY') else 'NOT SET')"
```
