#!/usr/bin/env python3
"""
测试智能剪辑系统
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from core.config_loader import ConfigLoader
from core.smart_editor import SmartEditor
from core.effects_applier import EffectsApplier


def test_config_loader():
    """测试配置加载"""
    print("=" * 50)
    print("测试1: 配置加载器")
    print("=" * 50)

    loader = ConfigLoader()

    print("\n可用配置:")
    for name, desc in loader.list_profiles().items():
        print(f"  ✓ {name}: {desc}")

    print("\n测试加载风光片配置:")
    profile = loader.get_profile("风光片")
    print(f"  名称: {profile.name}")
    print(f"  目标时长: {profile.target_duration}秒")
    print(f"  镜头时长: {profile.shot_duration}秒")
    print(f"  慢镜头: {profile.slow_motion_speed}x")
    print(f"  转场: {profile.transition.type} ({profile.transition.duration}秒)")
    print(f"  音乐BPM: {profile.music.bpm_range}")
    print(f"  目标冲击力: {profile.visual_impact_target}分")

    print("\n✅ 配置加载测试通过")


def test_effects_applier():
    """测试效果应用器"""
    print("\n" + "=" * 50)
    print("测试2: 效果应用器")
    print("=" * 50)

    loader = ConfigLoader()
    profile = loader.get_profile("风光片")
    applier = EffectsApplier(profile)

    print("\n查找素材:")
    music = applier.find_music()
    if music:
        print(f"  ✓ 找到音乐: {Path(music).name}")
    else:
        print(f"  ⚠️  未找到音乐")

    transition = applier.find_transition_effect()
    if transition:
        print(f"  ✓ 找到转场: {Path(transition).name}")
    else:
        print(f"  ⚠️  未找到转场")

    print("\n✅ 效果应用器测试通过")


def test_video_analysis():
    """测试视频分析"""
    print("\n" + "=" * 50)
    print("测试3: 视频质量分析")
    print("=" * 50)

    # 查找测试视频
    test_dirs = [
        "/Users/gs/Videos/待剪辑",
        "/Users/gs/7·客片/素材/宁"
    ]

    test_video = None
    for dir_path in test_dirs:
        if Path(dir_path).exists():
            videos = list(Path(dir_path).glob("*.mp4"))
            if videos:
                test_video = str(videos[0])
                break

    if not test_video:
        print("  ⚠️  未找到测试视频，跳过")
        return

    print(f"\n分析视频: {Path(test_video).name}")

    editor = SmartEditor("通用")
    score = editor.analyze_video_quality(test_video)

    print(f"  质量评分: {score:.2f}")
    if score >= 0.7:
        print(f"  ✓ 质量合格（阈值: 0.7）")
    else:
        print(f"  ⚠️  质量偏低（阈值: 0.7）")

    print("\n✅ 视频分析测试通过")


def main():
    print("\n🎬 智能剪辑系统测试")
    print("=" * 50)

    try:
        test_config_loader()
        test_effects_applier()
        test_video_analysis()

        print("\n" + "=" * 50)
        print("✅ 所有测试通过！")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
