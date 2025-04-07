"""
摘要生成器模块 - 负责文本摘要生成

此模块使用AI模型（如GPT、Claude、DeepSeek）生成文本摘要。
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
from openai import OpenAI
import requests

from youtube_assistant.utils.common import ensure_directory, save_text_to_file
from youtube_assistant.utils.composite import TextSummaryComposite


def summarize_text(text_path, model=None, api_key=None, base_url=None, stream=False, output_dir="summaries", custom_prompt=None, template_path=None):
    """
    使用大语言模型总结文本内容
    :param text_path: 文本文件路径
    :param model: 使用的模型名称，默认从环境变量获取
    :param api_key: API密钥，默认从环境变量获取
    :param base_url: 自定义API基础URL，默认从环境变量获取
    :param stream: 是否使用流式输出，默认为False
    :param output_dir: 输出目录，默认为summaries
    :param custom_prompt: 自定义提示词，如果提供则使用此提示词代替默认提示词
    :param template_path: 模板文件路径，如果提供则使用此模板
    :return: Markdown格式的总结文本
    """
    try:
        # 导入TextSummaryComposite类 (避免循环导入)
        from youtube_assistant.utils.composite import TextSummaryComposite
        
        # 创建输出目录
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # 读取文本文件
        with open(text_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 使用组合模型生成摘要
        composite = TextSummaryComposite()
        
        # 设置模型和API密钥（如果提供）
        if model:
            composite.target_model = model
        if api_key:
            composite.target_api_key = api_key
        if base_url:
            composite.target_api_url = base_url
        
        # 生成输出文件名
        base_name = Path(text_path).stem.replace("_transcript", "")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{base_name}_{timestamp}_article.md"
        output_path = os.path.join(output_dir, output_filename)
        
        # 使用组合模型生成摘要
        print("开始使用组合模型生成文章...")
        article = composite.generate_summary(content, stream=stream, custom_prompt=custom_prompt, template_path=template_path)
        
        # 保存摘要
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(article)
        
        print("文章生成完成!")
        return output_path
    except Exception as e:
        print(f"文章生成失败: {str(e)}")
        raise Exception(f"文章生成失败: {str(e)}")