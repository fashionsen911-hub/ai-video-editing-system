# 智能剪辑配置系统

基于70个视频学习成果的专业级剪辑配置系统

## 功能特点

- ✅ 6种专业配置模板（风光片、人物视频、卡点视频、转场特效、混剪、通用）
- ✅ 智能视频质量分析
- ✅ 自动音乐匹配
- ✅ 配置驱动的剪辑流程
- ✅ 支持自定义参数

## 快速开始

### 1. 安装依赖

```bash
bash /Users/gs/ai-video-system/setup.sh
```

### 2. 查看可用配置

```bash
python3 /Users/gs/ai-video-system/cli/edit_video.py --list-profiles
```

### 3. 剪辑视频

```bash
# 使用风光片配置
python3 /Users/gs/ai-video-system/cli/edit_video.py \
  --input video1.mp4 video2.mp4 \
  --output result.mp4 \
  --profile 风光片

# 使用自定义参数
python3 /Users/gs/ai-video-system/cli/edit_video.py \
  --input video1.mp4 video2.mp4 \
  --output result.mp4 \
  --profile 通用 \
  --duration 20 \
  --slow-motion 0.7
```

## 配置说明

### 风光片配置
- 时长: 25秒
- 镜头时长: 3秒
- 慢镜头: 0.75x
- 转场: 淡入淡出
- 音乐: 60-80 BPM 史诗
- 目标冲击力: 8.0分

### 人物视频配置
- 时长: 14秒
- 镜头时长: 2秒
- 慢镜头: 0.6x
- 转场: 快切
- 音乐: 80-120 BPM 武侠
- 目标冲击力: 8.5分

### 卡点视频配置
- 时长: 8秒
- 镜头时长: 0.5秒
- 慢镜头: 1.0x（无）
- 转场: 硬切
- 音乐: 120-160 BPM 嘻哈
- 目标冲击力: 6.5分

## 测试

```bash
python3 /Users/gs/ai-video-system/test_pipeline.py
```
