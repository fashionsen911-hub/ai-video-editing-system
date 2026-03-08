#!/usr/bin/env python3
"""参考图修图服务 - 风格迁移"""
from pathlib import Path

class ReferenceImageService:
    def __init__(self, model_manager):
        self.model_manager = model_manager

    def apply_reference_style(self, image_path, reference_path, prompt="apply reference style"):
        """应用参考图风格"""
        print(f"🎨 参考图修图: {Path(image_path).name} -> {Path(reference_path).name}")
        result = self.model_manager.call_ip_adapter(image_path, reference_path, prompt)
        return result
