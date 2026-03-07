"""
效果应用器
应用转场、调色、特效
"""

from pathlib import Path
from typing import List, Optional
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip
from moviepy.video.fx.all import fadein, fadeout
import random

from configs.editing_profiles import EditingProfile


class EffectsApplier:
    """效果应用器"""

    def __init__(self, profile: EditingProfile, materials_dir: str = "/Users/gs/3·素材库"):
        self.profile = profile
        self.materials_dir = Path(materials_dir)

    def apply_transitions(self, clips: List[VideoFileClip]) -> List[VideoFileClip]:
        """应用转场效果"""
        transition_type = self.profile.transition.type
        duration = self.profile.transition.duration

        if transition_type == "crossfade" and duration > 0:
            # 淡入淡出
            processed = []
            for i, clip in enumerate(clips):
                if i == 0:
                    clip = clip.fx(fadein, duration)
                if i == len(clips) - 1:
                    clip = clip.fx(fadeout, duration)
                processed.append(clip)
            return processed

        elif transition_type == "cut":
            # 硬切，无需处理
            return clips

        else:
            # 其他转场类型暂时使用淡入淡出
            return self.apply_transitions(clips)

    def apply_color_grading(self, clip: VideoFileClip) -> VideoFileClip:
        """应用调色"""
        if not self.profile.color_grading.enabled:
            return clip

        style = self.profile.color_grading.style

        if style == "cinematic":
            # 电影感：降低饱和度，增加对比度
            return clip.fx(lambda c: c.fx(lambda frame: frame * 0.95))

        elif style == "high_contrast":
            # 高对比度
            boost = self.profile.color_grading.boost_saturation
            return clip.fx(lambda c: c.fx(lambda frame: frame * boost))

        elif style == "bw":
            # 黑白
            return clip.fx(lambda c: c.fx(lambda frame: frame.mean(axis=2, keepdims=True).repeat(3, axis=2)))

        return clip

    def find_music(self) -> Optional[str]:
        """从素材库查找音乐"""
        music_dir = self.materials_dir / "3、音乐"

        if not music_dir.exists():
            return None

        category = self.profile.music.category

        # 映射类别到目录
        category_map = {
            "史诗": "古风",
            "武侠": "古风",
            "嘻哈": "电子",
            "电子": "电子",
            "通用": "情感"
        }

        target_dir = music_dir / category_map.get(category, "情感")

        if target_dir.exists():
            music_files = list(target_dir.glob("*.mp3")) + list(target_dir.glob("*.wav"))
            if music_files:
                return str(random.choice(music_files))

        return None

    def find_transition_effect(self) -> Optional[str]:
        """从素材库查找转场素材"""
        transition_dir = self.materials_dir / "2、转场"

        if not transition_dir.exists():
            return None

        transition_files = list(transition_dir.glob("*.mp4"))
        if transition_files:
            return str(random.choice(transition_files))

        return None


if __name__ == "__main__":
    from core.config_loader import ConfigLoader

    loader = ConfigLoader()
    profile = loader.get_profile("风光片")
    applier = EffectsApplier(profile)

    music = applier.find_music()
    print(f"找到音乐: {music}")
