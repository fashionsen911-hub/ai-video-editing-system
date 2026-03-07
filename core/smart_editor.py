"""
智能剪辑引擎
基于配置自动剪辑视频
"""

from pathlib import Path
from typing import List, Optional, Tuple
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from moviepy.editor import VideoFileClip, concatenate_videoclips
import numpy as np
import cv2

from core.config_loader import ConfigLoader
from configs.editing_profiles import EditingProfile


class SmartEditor:
    """智能剪辑引擎"""

    def __init__(self, config_profile: str = "通用"):
        self.loader = ConfigLoader()
        self.profile = self.loader.get_profile(config_profile)

    def analyze_video_quality(self, video_path: str) -> float:
        """分析视频质量（清晰度+亮度）"""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"无法打开视频文件: {video_path}")
        try:
            # 采样5帧
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            sample_indices = np.linspace(0, total_frames - 1, 5, dtype=int)

            sharpness_scores = []
            brightness_scores = []

            for idx in sample_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = cap.read()
                if not ret:
                    continue

                # 清晰度（拉普拉斯方差）
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                laplacian = cv2.Laplacian(gray, cv2.CV_64F)
                sharpness = laplacian.var()
                sharpness_scores.append(sharpness)

                # 亮度
                brightness = np.mean(gray)
                brightness_scores.append(brightness)

            # 归一化评分
            avg_sharpness = np.mean(sharpness_scores)
            avg_brightness = np.mean(brightness_scores)

            # 清晰度权重0.7，亮度权重0.3
            sharpness_norm = min(avg_sharpness / 500, 1.0)
            brightness_norm = 1.0 - abs(avg_brightness - 127) / 127

            return sharpness_norm * 0.7 + brightness_norm * 0.3
        finally:
            cap.release()

    def select_best_clips(self, video_paths: List[str]) -> List[Tuple[str, float]]:
        """选择最佳片段"""
        clips_with_scores = []

        for path in video_paths:
            score = self.analyze_video_quality(path)
            if score >= self.profile.shot_selection.quality_threshold:
                clips_with_scores.append((path, score))

        # 按质量排序
        clips_with_scores.sort(key=lambda x: x[1], reverse=True)
        return clips_with_scores

    def edit_video(self, input_videos: List[str], output_path: str,
                   music_path: Optional[str] = None) -> str:
        """智能剪辑主流程"""

        # 1. 选择最佳片段
        best_clips = self.select_best_clips(input_videos)

        if not best_clips:
            raise ValueError("没有符合质量要求的视频片段")

        # 2. 加载视频并裁剪
        video_clips = []
        current_duration = 0
        target = self.profile.target_duration

        for video_path, score in best_clips:
            if current_duration >= target:
                break

            try:
                clip = VideoFileClip(video_path)
            except Exception as e:
                print(f"警告: 无法加载视频 {video_path}: {e}")
                continue

            # 应用慢镜头
            if self.profile.slow_motion_speed != 1.0:
                from moviepy.video.fx.speedx import speedx
                clip = clip.fx(speedx, self.profile.slow_motion_speed)

            # 计算需要的时长
            needed = min(self.profile.shot_duration, target - current_duration)

            # 从中间裁剪（避免开头结尾不稳定）
            start = max(0, (clip.duration - needed) / 2)
            clip = clip.subclip(start, start + needed)

            video_clips.append(clip)
            current_duration += needed

        # 3. 合并视频
        if not video_clips:
            raise ValueError("没有可用的视频片段")

        final = concatenate_videoclips(video_clips, method="compose")

        # 4. 添加音乐
        if music_path:
            from moviepy.editor import AudioFileClip
            audio = AudioFileClip(music_path)
            audio = audio.subclip(0, min(audio.duration, final.duration))
            final = final.set_audio(audio)

        # 5. 导出
        final.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            fps=30,
            preset='medium'
        )

        # 清理
        for clip in video_clips:
            clip.close()
        final.close()

        return output_path


if __name__ == "__main__":
    # 测试
    editor = SmartEditor("风光片")
    print(f"使用配置: {editor.profile.name}")
    print(f"目标时长: {editor.profile.target_duration}秒")
