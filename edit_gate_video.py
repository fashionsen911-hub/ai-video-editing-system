#!/usr/bin/env python3
"""韩城城门视频剪辑脚本 - 最小化实现"""
import json
import os
from pathlib import Path
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from moviepy.video.fx.all import fadein, fadeout
import numpy as np

def apply_speed_curve(clip, curve_type):
    """应用曲线变速"""
    curves = {
        "pulse": 1.0,
        "slow_motion": 0.6,
        "smooth_slow": 0.75,
        "dynamic": 0.8
    }
    return clip.speedx(curves.get(curve_type, 1.0))

def process_clip(video_path, start, duration, speed_curve, transition):
    """处理单个片段"""
    video = VideoFileClip(video_path)
    clip = video.subclip(start, start + duration)
    clip = apply_speed_curve(clip, speed_curve)

    # 应用转场
    if transition == "crossfade":
        clip = clip.fx(fadein, 0.5).fx(fadeout, 0.5)

    return clip.copy()

def apply_transitions(clips, transitions):
    """应用转场效果 - 已在process_clip中处理"""
    return clips

def select_music(music_dir, keywords):
    """选择音乐文件"""
    music_files = list(Path(music_dir).glob("*.mp3"))
    for keyword in keywords:
        for f in music_files:
            if keyword.lower() in f.name.lower():
                return str(f)
    return str(music_files[0]) if music_files else None

def main():
    # 加载配置
    config_path = Path(__file__).parent / "gate_edit_config.json"
    with open(config_path) as f:
        config = json.load(f)

    print("🎬 开始剪辑韩城城门视频...")

    # 处理视频片段
    clips = []
    transitions = []

    for clip_config in config["clips"]:
        video_path = Path(config["input_dir"]) / clip_config["file"]
        print(f"处理: {clip_config['file']}")

        clip = process_clip(
            str(video_path),
            clip_config["start"],
            clip_config["duration"],
            clip_config["speed_curve"],
            clip_config.get("transition")
        )
        clips.append(clip)
        transitions.append(clip_config.get("transition"))

    # 应用转场
    clips = apply_transitions(clips, transitions)

    # 合并视频
    print("合并片段...")
    final_video = concatenate_videoclips(clips, method="compose")

    # 添加音乐
    if config["music"]["auto_select"]:
        music_path = select_music(config["music_dir"], config["music"]["keywords"])
        if music_path:
            print(f"添加音乐: {Path(music_path).name}")
            audio = AudioFileClip(music_path).subclip(0, final_video.duration)
            final_video = final_video.set_audio(audio)

    # 导出
    output_path = config["output_path"]
    os.makedirs(Path(output_path).parent, exist_ok=True)
    print(f"导出到: {output_path}")

    final_video.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=30,
        preset="medium",
        bitrate="8M"
    )

    print("✅ 剪辑完成！")

if __name__ == "__main__":
    main()
