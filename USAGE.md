# 智能剪辑配置系统使用指南

## 快速开始

### 1. 查看可用配置

```bash
python3 /Users/gs/ai-video-system/cli/edit_video.py --list-profiles
```

### 2. 使用配置剪辑视频

```bash
# 风光片配置（25秒，慢镜头0.75x，淡入淡出）
python3 /Users/gs/ai-video-system/cli/edit_video.py \
  --input /Users/gs/Videos/待剪辑/video1.mp4 /Users/gs/Videos/待剪辑/video2.mp4 \
  --output /Users/gs/Movies/Videos/AI_Output/风光片.mp4 \
  --profile 风光片

# 人物视频配置（14秒，慢镜头0.6x，快切）
python3 /Users/gs/ai-video-system/cli/edit_video.py \
  --input /Users/gs/Videos/待剪辑/*.mp4 \
  --output /Users/gs/Movies/Videos/AI_Output/人物视频.mp4 \
  --profile 人物视频

# 卡点视频配置（8秒，无慢镜头，硬切）
python3 /Users/gs/ai-video-system/cli/edit_video.py \
  --input /Users/gs/Videos/待剪辑/*.mp4 \
  --output /Users/gs/Movies/Videos/AI_Output/卡点视频.mp4 \
  --profile 卡点视频
```

### 3. 自定义参数

```bash
# 自定义时长和慢镜头速度
python3 /Users/gs/ai-video-system/cli/edit_video.py \
  --input /Users/gs/Videos/待剪辑/*.mp4 \
  --output /Users/gs/Movies/Videos/AI_Output/自定义.mp4 \
  --profile 通用 \
  --duration 20 \
  --slow-motion 0.8
```

## 配置详解

基于70个视频学习成果的专业级配置：

| 配置类型 | 时长 | 镜头时长 | 慢镜头 | 转场 | 音乐BPM | 目标冲击力 |
|---------|------|---------|--------|------|---------|-----------|
| 风光片 | 25秒 | 3秒 | 0.75x | 淡入淡出 | 60-80 | 8.0分 |
| 人物视频 | 14秒 | 2秒 | 0.6x | 快切 | 80-120 | 8.5分 |
| 卡点视频 | 8秒 | 0.5秒 | 1.0x | 硬切 | 120-160 | 6.5分 |
| 转场特效 | 12秒 | 1.5秒 | 0.7x | 创意遮罩 | 90-110 | 7.5分 |
| 混剪 | 12秒 | 1.5秒 | 0.65x | 淡入淡出 | 70-90 | 9.0分 |
| 通用 | 18秒 | 2秒 | 0.7x | 淡入淡出 | 70-100 | 7.4分 |

## 系统特性

- ✅ 自动视频质量分析（清晰度+亮度）
- ✅ 智能片段选择（只选择高质量片段）
- ✅ 自动音乐匹配（从素材库选择）
- ✅ 配置驱动的剪辑流程
- ✅ M1硬件加速支持

## 工作原理

1. **质量分析**：分析每个视频的清晰度和亮度
2. **片段选择**：选择质量评分 ≥ 0.7 的片段
3. **慢镜头**：应用配置的慢镜头速度
4. **裁剪合并**：按目标时长裁剪并合并
5. **音乐匹配**：从素材库自动选择音乐
6. **导出**：输出1080p 30fps视频

## 故障排除

### 问题：找不到音乐
确保素材库存在：`/Users/gs/3·素材库/3、音乐/`

### 问题：视频质量评分过低
降低质量阈值或使用更高质量的源视频

### 问题：处理速度慢
系统已启用硬件加速，处理30秒视频约需5分钟
