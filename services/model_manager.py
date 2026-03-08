#!/usr/bin/env python3
"""模型管理器 - 统一管理所有AI模型API调用"""
import os
import requests

class ModelManager:
    def __init__(self, config):
        self.config = config
        self.hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
        self.hf_api = "https://api-inference.huggingface.co/models/"

    def call_gfpgan(self, image_path):
        """调用人脸修复（Hugging Face）"""
        with open(image_path, "rb") as f:
            data = f.read()
        response = requests.post(
            self.hf_api + "tencentarc/gfpgan-v1-3",
            headers={"Authorization": f"Bearer {self.hf_token}"},
            data=data
        )
        return response.content

    def call_remove_bg(self, image_path):
        """调用背景移除（Hugging Face RMBG）"""
        with open(image_path, "rb") as f:
            data = f.read()
        response = requests.post(
            self.hf_api + "briaai/RMBG-1.4",
            headers={"Authorization": f"Bearer {self.hf_token}"},
            data=data
        )
        return response.content

    def call_ip_adapter(self, image_path, reference_path, prompt):
        """调用参考图修图（Hugging Face）"""
        # 使用Stable Diffusion图生图
        with open(image_path, "rb") as f:
            data = f.read()
        response = requests.post(
            self.hf_api + "stabilityai/stable-diffusion-xl-base-1.0",
            headers={"Authorization": f"Bearer {self.hf_token}"},
            json={"inputs": prompt},
            data=data
        )
        return response.content

