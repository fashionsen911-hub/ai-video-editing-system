#!/usr/bin/env python3
"""背景处理服务 - 抠图、背景替换"""
from pathlib import Path

class BackgroundService:
    def __init__(self, model_manager):
        self.model_manager = model_manager

    def remove_background(self, image_path):
        """移除背景"""
        print(f"✂️ 背景移除: {Path(image_path).name}")
        result = self.model_manager.call_remove_bg(image_path)
        return result
