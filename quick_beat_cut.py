#!/usr/bin/env python3
"""快速卡点剪辑"""
import sys
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def quick_beat_cut(video_files, output, music, duration=8, clip_duration=0.5):
    """快速卡点剪辑"""
    print(f"🎬 卡点剪辑：{len(video_files)}个视频 → {duration}秒")
    
    clips = []
    total = 0
    
    for vf in video_files:
        video = VideoFileClip(vf)
        # 从每个视频中间取片段
        start = video.duration / 3
        while total < duration and start < video.duration - clip_duration:
            clip = video.subclip(start, start + clip_duration)
            clips.append(clip)
            total += clip_duration
            start += video.duration / 5
            if total >= duration:
                break
        video.close()
        if total >= duration:
            break
    
    # 合并
    final = concatenate_videoclips(clips[:int(duration/clip_duration)], method="compose")
    
    # 添加音乐
    if music:
        audio = AudioFileClip(music).subclip(0, final.duration)
        final = final.set_audio(audio)
    
    # 导出
    final.write_videofile(output, codec='libx264', audio_codec='aac', fps=30)
    print(f"✅ 完成：{output}")

if __name__ == "__main__":
    videos = sys.argv[1:-2]
    output = sys.argv[-2]
    music = sys.argv[-1]
    quick_beat_cut(videos, output, music)
