#!/usr/bin/env python3
"""模型管理器 - 统一管理所有AI模型API调用"""
import os
import replicate
import requests

class ModelManager:
    def __init__(self, config):
        self.config = config
        self.replicate_token = os.getenv("REPLICATE_API_TOKEN")

    def call_gfpgan(self, image_path):
        """调用GFPGAN人脸修复"""
        model = self.config["models"]["gfpgan"]["model"]
        output = replicate.run(model, input={"img": open(image_path, "rb"), "version": "v1.4", "scale": 2})
        return self._download_image(output)

    def call_remove_bg(self, image_path):
        """调用Remove.bg抠图API"""
        api_key = os.getenv("REMOVE_BG_API_KEY")
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': open(image_path, 'rb')},
            headers={'X-Api-Key': api_key}
        )
        return response.content

    def call_ip_adapter(self, image_path, reference_path, prompt):
        """调用IP-Adapter参考图修图"""
        model = self.config["models"]["ip_adapter"]["model"]
        output = replicate.run(model, input={
            "image": open(image_path, "rb"),
            "ip_adapter_image": open(reference_path, "rb"),
            "prompt": prompt
        })
        return self._download_image(output)

    def _download_image(self, url):
        """下载图片"""
        response = requests.get(url)
        return response.content
