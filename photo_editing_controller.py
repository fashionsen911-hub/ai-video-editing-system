#!/usr/bin/env python3
"""AI智能修图框架 - 主控制器"""
import json
from pathlib import Path
from services.model_manager import ModelManager
from services.ai_prompt_parser import AIPromptParser
from services.face_enhancement_service import FaceEnhancementService
from services.background_service import BackgroundService
from services.reference_image_service import ReferenceImageService

class PhotoEditingController:
    def __init__(self, config_path):
        with open(config_path) as f:
            self.config = json.load(f)

        self.model_manager = ModelManager(self.config)
        self.parser = AIPromptParser()
        self.face_service = FaceEnhancementService(self.model_manager)
        self.bg_service = BackgroundService(self.model_manager)
        self.ref_service = ReferenceImageService(self.model_manager)

    def process(self, image_path, prompt=None, reference_image=None, preset=None, tasks=None):
        """处理图片"""
        print(f"\n🎬 AI智能修图开始")
        print(f"输入: {Path(image_path).name}\n")

        if tasks is None:
            if prompt:
                tasks = self.parser.parse(prompt)["tasks"]
            elif preset:
                tasks = self._load_preset(preset)

        result = None
        for task in tasks:
            task_type = task["type"]
            params = task.get("params", {})

            if task_type == "face_enhancement":
                result = self.face_service.enhance(image_path, **params)
            elif task_type == "background_remove":
                result = self.bg_service.remove_background(image_path)
            elif task_type == "reference_style" and reference_image:
                result = self.ref_service.apply_reference_style(image_path, reference_image, prompt or "")

        print("\n✅ 处理完成")
        return result

    def _load_preset(self, preset_name):
        """加载预设配置"""
        preset = self.config["presets"].get(preset_name, {})
        return [{"type": k, "params": v} for k, v in preset.items()]
