"""
剪辑配置数据结构定义
基于70个视频学习成果
"""

from dataclasses import dataclass
from typing import Optional, Dict, List


@dataclass
class TransitionConfig:
    """转场配置"""
    type: str  # crossfade, cut, creative_mask
    duration: float  # 转场时长（秒）


@dataclass
class ColorGradingConfig:
    """调色配置"""
    enabled: bool
    style: str  # cinematic, high_contrast, bw, vintage
    lut_file: Optional[str] = None
    boost_saturation: float = 1.0


@dataclass
class MusicConfig:
    """音乐配置"""
    category: str  # 史诗, 武侠, 嘻哈, 电子等
    bpm_range: List[int]  # [min, max]
    mood: Optional[str] = None


@dataclass
class EffectsConfig:
    """特效配置"""
    light_effects: bool = False
    particle_effects: bool = False
    blur_effects: bool = False


@dataclass
class ShotSelectionConfig:
    """镜头选择配置"""
    quality_threshold: float = 0.7
    prefer_wide_shots: bool = False
    prefer_action_shots: bool = False
    low_angle_priority: bool = False


@dataclass
class EditingProfile:
    """完整的剪辑配置"""
    name: str
    description: str
    target_duration: int  # 目标时长（秒）
    shot_duration: float  # 每个镜头时长（秒）
    slow_motion_speed: float  # 慢镜头速度（0.6-1.0）
    transition: TransitionConfig
    color_grading: ColorGradingConfig
    music: MusicConfig
    visual_impact_target: float  # 目标视觉冲击力（1-10分）
    shot_selection: ShotSelectionConfig
    effects: Optional[EffectsConfig] = None
