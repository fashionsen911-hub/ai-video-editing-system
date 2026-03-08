#!/usr/bin/env python3
"""人脸增强服务 - 磨皮美白"""
from pathlib import Path

class FaceEnhancementService:
    def __init__(self, model_manager):
        self.model_manager = model_manager

    def enhance(self, image_path, strength=0.8):
        """人脸增强"""
        print(f"🎨 人脸增强: {Path(image_path).name}")
        result = self.model_manager.call_gfpgan(image_path)
        return result
