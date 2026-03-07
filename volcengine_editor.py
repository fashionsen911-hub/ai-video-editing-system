#!/usr/bin/env python3
"""
火山方舟增强的智能剪辑系统
"""

import os
import glob
import json
import base64
import requests
import librosa
import numpy as np
from scipy.signal import find_peaks
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from moviepy.video.fx import all as vfx
import cv2


class VolcengineEnhancedEditor:
    def __init__(self):
        self.api_key = os.getenv("VOLCENGINE_API_KEY")
        if not self.api_key:
            raise ValueError("请设置环境变量 VOLCENGINE_API_KEY")
        self.api_url = "https://ark.cn-beijing.volces.com/api/v3/responses"
        self.model = "doubao-seed-2-0-pro-260215"

    def analyze_frame_with_volcengine(self, image_path):
        """使用火山方舟分析视频帧"""
        with open(image_path, 'rb') as f:
            image_base64 = base64.b64encode(f.read()).decode('utf-8')

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "input": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{image_base64}"
                        },
                        {
                            "type": "input_text",
                            "text": """作为专业视频剪辑师，请简洁分析：
1. 是否有人物？人物重要性（1-10分）
2. 情绪氛围（一个词）
3. 建议镜头时长（秒）
4. 剪辑位置（开场/中段/结尾）

请用JSON格式回复：
{"has_person": true/false, "person_importance": 0-10, "emotion": "词", "duration": 秒数, "position": "位置"}"""
                        }
                    ]
                }
            ]
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=60)
            if response.status_code == 200:
                result = response.json()
                for output in result.get("output", []):
                    if output.get("type") == "message":
                        for content in output.get("content", []):
                            if content.get("type") == "output_text":
                                text = content.get("text")
                                # 尝试提取JSON
                                import re
                                json_match = re.search(r'\{[^}]+\}', text)
                                if json_match:
                                    return json.loads(json_match.group())
                                return {"raw_text": text}
        except Exception as e:
            print(f"  ⚠️  火山方舟分析失败: {e}")
            return None

    def extract_key_frame(self, video_path, output_path):
        """提取视频关键帧"""
        cap = cv2.VideoCapture(video_path)

        # 取中间帧
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames // 2)

        ret, frame = cap.read()
        if ret:
            # 缩小图片加速上传
            frame = cv2.resize(frame, (800, 450))
            cv2.imwrite(output_path, frame)

        cap.release()
        return ret

    def analyze_music_beats(self, music_path, duration=30):
        """分析音乐节拍"""
        y, sr = librosa.load(music_path, sr=22050, duration=duration)
        rms = librosa.feature.rms(y=y, hop_length=512)[0]
        rms_times = librosa.times_like(rms, sr=sr, hop_length=512)

        peaks, _ = find_peaks(rms, height=np.percentile(rms, 90), distance=40)
        return list(rms_times[peaks])

    def create_intelligent_video(self, input_dir, output_path, music_path, slow_speed=0.6):
        """创建智能剪辑视频"""
        print("=" * 60)
        print("🚀 火山方舟增强智能剪辑系统")
        print("=" * 60)
        print()

        # 1. 分析音乐
        print("🎵 分析音乐节拍...")
        beats = self.analyze_music_beats(music_path)
        print(f"  检测到 {len(beats)} 个主要节拍")

        # 2. 分析所有视频
        print()
        print("🎬 使用火山方舟分析视频...")

        video_files = []
        for ext in ['*.mp4', '*.mov', '*.MOV']:
            video_files.extend(glob.glob(os.path.join(input_dir, ext)))

        video_analysis = {}
        temp_dir = "/tmp/volcengine_frames"
        os.makedirs(temp_dir, exist_ok=True)

        for video_path in video_files:
            name = os.path.basename(video_path)
            code = None
            for c in ['C037', 'C038', 'C039', 'C041', 'C042', 'C045', 'C048']:
                if c in name:
                    code = c
                    break

            if not code:
                continue

            print(f"\n  分析 {code}...")

            # 提取关键帧
            frame_path = os.path.join(temp_dir, f"{code}.jpg")
            if self.extract_key_frame(video_path, frame_path):
                # 火山方舟分析
                analysis = self.analyze_frame_with_volcengine(frame_path)
                if analysis:
                    video_analysis[code] = {
                        'path': video_path,
                        'analysis': analysis
                    }
                    print(f"    {analysis}")

        # 3. 根据分析结果排序镜头
        print()
        print("📋 生成剪辑方案...")

        # 人物镜头优先
        person_shots = []
        scene_shots = []

        for code, data in video_analysis.items():
            analysis = data['analysis']
            if analysis.get('has_person') or analysis.get('person_importance', 0) > 5:
                person_shots.append((code, data))
            else:
                scene_shots.append((code, data))

        # 按重要性排序
        person_shots.sort(key=lambda x: x[1]['analysis'].get('person_importance', 0), reverse=True)

        print(f"  人物镜头: {[s[0] for s in person_shots]}")
        print(f"  景物镜头: {[s[0] for s in scene_shots]}")

        # 4. 创建卡点方案
        shot_plan = []

        # 人物镜头卡在前面的节拍
        for i, (code, data) in enumerate(person_shots[:2]):
            if i < len(beats):
                start = beats[i] if i > 0 else 0.0
                end = beats[i+1] if i+1 < len(beats) else start + 3.0
                shot_plan.append({
                    'start': start,
                    'end': end,
                    'code': code,
                    'data': data
                })

        # 景物镜头循环
        scene_idx = 0
        for i in range(len(person_shots), min(len(beats), 12)):
            if scene_idx >= len(scene_shots):
                break

            code, data = scene_shots[scene_idx % len(scene_shots)]
            start = beats[i]
            end = beats[i+1] if i+1 < len(beats) else 30.0

            shot_plan.append({
                'start': start,
                'end': end,
                'code': code,
                'data': data
            })
            scene_idx += 1

        print()
        print("🎬 剪辑方案：")
        for i, plan in enumerate(shot_plan, 1):
            duration = plan['end'] - plan['start']
            analysis = plan['data']['analysis']
            emotion = analysis.get('emotion', '未知')
            print(f"  {i}. {plan['start']:.2f}s → {plan['code']} ({emotion}) - {duration:.1f}秒")

        # 5. 剪辑视频
        print()
        print("✂️  开始剪辑...")

        clips = []
        original_clips = []  # 保存原始clip引用

        for plan in shot_plan:
            video_path = plan['data']['path']
            target_duration = plan['end'] - plan['start']

            clip = VideoFileClip(video_path, audio=False)
            original_clips.append(clip)

            slow_clip = clip.fx(vfx.speedx, slow_speed)

            if slow_clip.duration >= target_duration:
                start = (slow_clip.duration - target_duration) / 2
                subclip = slow_clip.subclip(start, start + target_duration)
            else:
                subclip = slow_clip

            if len(clips) > 0:
                subclip = subclip.crossfadein(0.3)

            clips.append(subclip)

        # 6. 合并和导出
        print("🔗 合并镜头...")
        final_video = concatenate_videoclips(clips, method="compose")

        if final_video.duration > 30:
            final_video = final_video.subclip(0, 30)

        print("🎵 添加音乐...")
        audio = AudioFileClip(music_path)
        if audio.duration > final_video.duration:
            audio = audio.subclip(0, final_video.duration)
        audio = audio.audio_fadeout(2.0)
        final_video = final_video.set_audio(audio)

        print()
        print("🚀 导出视频...")
        final_video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            fps=30,
            preset='medium',
            bitrate='8M',
            threads=4
        )

        # 清理
        for clip in clips:
            clip.close()
        final_video.close()
        audio.close()

        print()
        print("=" * 60)
        print(f"✅ 完成！")
        print(f"📁 输出: {output_path}")
        print("=" * 60)


if __name__ == "__main__":
    editor = VolcengineEnhancedEditor()

    input_dir = "/Users/gs/Videos/待剪辑"
    output_path = "/Users/gs/Movies/Videos/AI_Output/volcengine_enhanced.mp4"
    music_path = "/Users/gs/3·素材库/3、音乐/古风/陈阿晓 - 烟雨小镇(纯音乐）.mp3"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    editor.create_intelligent_video(input_dir, output_path, music_path, slow_speed=0.6)
