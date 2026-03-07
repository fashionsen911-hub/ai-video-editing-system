#!/usr/bin/env python3
"""
命令行剪辑工具
"""

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.smart_editor import SmartEditor
from core.effects_applier import EffectsApplier
from core.config_loader import ConfigLoader


def main():
    parser = argparse.ArgumentParser(description="智能视频剪辑工具")
    parser.add_argument("--input", nargs="+", help="输入视频文件")
    parser.add_argument("--output", help="输出文件路径")
    parser.add_argument("--profile", default="通用", help="配置类型")
    parser.add_argument("--duration", type=int, help="自定义时长")
    parser.add_argument("--slow-motion", type=float, help="自定义慢镜头速度")
    parser.add_argument("--list-profiles", action="store_true", help="列出所有配置")

    args = parser.parse_args()

    # 列出配置
    if args.list_profiles:
        loader = ConfigLoader()
        print("\n可用配置:")
        for name, desc in loader.list_profiles().items():
            print(f"  {name}: {desc}")
        return

    # 检查必需参数
    if not args.input or not args.output:
        parser.error("--input 和 --output 是必需的（除非使用 --list-profiles）")
        return

    # 创建编辑器
    editor = SmartEditor(args.profile)

    # 自定义参数
    if args.duration:
        editor.profile.target_duration = args.duration
    if args.slow_motion:
        editor.profile.slow_motion_speed = args.slow_motion

    print(f"\n使用配置: {editor.profile.name}")
    print(f"目标时长: {editor.profile.target_duration}秒")
    print(f"慢镜头速度: {editor.profile.slow_motion_speed}x")

    # 查找音乐
    applier = EffectsApplier(editor.profile)
    music = applier.find_music()

    if music:
        print(f"使用音乐: {Path(music).name}")

    # 开始剪辑
    print("\n开始剪辑...")
    output = editor.edit_video(args.input, args.output, music)
    print(f"\n✓ 完成！输出: {output}")


if __name__ == "__main__":
    main()
