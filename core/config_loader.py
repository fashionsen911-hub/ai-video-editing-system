"""
配置加载器
负责加载和验证剪辑配置
"""

import json
from pathlib import Path
from typing import Dict, Optional
import sys

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from configs.editing_profiles import (
    EditingProfile, TransitionConfig, ColorGradingConfig,
    MusicConfig, EffectsConfig, ShotSelectionConfig
)


class ConfigLoader:
    """配置加载器"""

    def __init__(self, config_file: Optional[str] = None):
        if config_file is None:
            config_file = Path(__file__).parent.parent / "configs" / "standard_profiles.json"

        self.config_file = Path(config_file)
        self.profiles: Dict[str, EditingProfile] = {}
        self._load_profiles()

    def _load_profiles(self):
        """加载所有配置"""
        with open(self.config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for profile_name, profile_data in data.items():
            self.profiles[profile_name] = self._parse_profile(profile_data)

    def _parse_profile(self, data: Dict) -> EditingProfile:
        """解析配置数据"""
        transition = TransitionConfig(**data['transition'])
        color_grading = ColorGradingConfig(**data['color_grading'])
        music = MusicConfig(**data['music'])
        shot_selection = ShotSelectionConfig(**data['shot_selection'])

        effects = None
        if data.get('effects'):
            effects = EffectsConfig(**data['effects'])

        return EditingProfile(
            name=data['name'],
            description=data['description'],
            target_duration=data['target_duration'],
            shot_duration=data['shot_duration'],
            slow_motion_speed=data['slow_motion_speed'],
            transition=transition,
            color_grading=color_grading,
            music=music,
            visual_impact_target=data['visual_impact_target'],
            shot_selection=shot_selection,
            effects=effects
        )

    def get_profile(self, profile_name: str) -> EditingProfile:
        """获取指定配置"""
        if profile_name not in self.profiles:
            print(f"配置 '{profile_name}' 不存在，使用通用配置")
            profile_name = "通用"

        return self.profiles[profile_name]

    def list_profiles(self) -> Dict[str, str]:
        """列出所有配置"""
        return {
            name: profile.description
            for name, profile in self.profiles.items()
        }

    def validate_profile(self, profile: EditingProfile) -> bool:
        """验证配置有效性"""
        if profile.target_duration <= 0:
            return False
        if profile.shot_duration <= 0:
            return False
        if not (0.1 <= profile.slow_motion_speed <= 2.0):
            return False
        if not (0 <= profile.visual_impact_target <= 10):
            return False
        return True


if __name__ == "__main__":
    # 测试配置加载
    loader = ConfigLoader()

    print("可用配置:")
    for name, desc in loader.list_profiles().items():
        print(f"  {name}: {desc}")

    print("\n风光片配置详情:")
    profile = loader.get_profile("风光片")
    print(f"  名称: {profile.name}")
    print(f"  目标时长: {profile.target_duration}秒")
    print(f"  镜头时长: {profile.shot_duration}秒")
    print(f"  慢镜头速度: {profile.slow_motion_speed}x")
    print(f"  转场类型: {profile.transition.type}")
    print(f"  音乐BPM: {profile.music.bpm_range}")
    print(f"  目标冲击力: {profile.visual_impact_target}分")
