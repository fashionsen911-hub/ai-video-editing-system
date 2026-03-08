#!/usr/bin/env python3
"""AI描述词解析器 - 使用Claude API解析用户描述词"""
import os
import anthropic

class AIPromptParser:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def parse(self, prompt):
        """解析用户描述词，生成处理任务"""
        system_prompt = """你是一个图片处理任务解析器。将用户的描述词转换为JSON格式的处理任务。
可用任务类型：face_enhancement（人脸增强）、background_remove（背景移除）、reference_style（参考图风格）
返回格式：{"tasks": [{"type": "任务类型", "params": {...}}]}"""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[{"role": "user", "content": f"{system_prompt}\n\n用户描述：{prompt}"}]
        )

        import json
        return json.loads(response.content[0].text)
