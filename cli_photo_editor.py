#!/usr/bin/env python3
"""AI智能修图 - 命令行工具"""
import sys
from pathlib import Path
from photo_editing_controller import PhotoEditingController

def main():
    if len(sys.argv) < 3:
        print("使用方法:")
        print("  python cli_photo_editor.py <输入图片> --prompt <描述词>")
        print("  python cli_photo_editor.py <输入图片> --reference <参考图> --prompt <描述词>")
        print("  python cli_photo_editor.py <输入图片> --preset <预设名>")
        sys.exit(1)

    controller = PhotoEditingController("photo_editing_config.json")

    input_path = sys.argv[1]
    output_path = f"output_{Path(input_path).name}"

    kwargs = {"image_path": input_path}

    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == "--prompt" and i+1 < len(sys.argv):
            kwargs["prompt"] = sys.argv[i+1]
        elif arg == "--reference" and i+1 < len(sys.argv):
            kwargs["reference_image"] = sys.argv[i+1]
        elif arg == "--preset" and i+1 < len(sys.argv):
            kwargs["preset"] = sys.argv[i+1]

    result = controller.process(**kwargs)

    with open(output_path, 'wb') as f:
        f.write(result)

    print(f"输出: {output_path}")

if __name__ == "__main__":
    main()
