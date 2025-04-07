"""
组合模型处理模块 - 用于处理不同API的组合调用
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from .summarizer import generate_summary_openai, generate_summary_claude, generate_summary_deepseek

# 加载环境变量
load_dotenv()


class TextSummaryComposite:
    """处理 DeepSeek 和其他 OpenAI 兼容模型的组合，用于文本摘要生成"""
    
    def __init__(self):
        """初始化组合模型"""
        # 从环境变量获取配置
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        self.deepseek_api_url = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")
        self.deepseek_model = os.getenv("DEEPSEEK_MODEL", "deepseek-ai/DeepSeek-R1")
        self.is_origin_reasoning = os.getenv("IS_ORIGIN_REASONING", "true").lower() == "true"
        
        self.target_api_key = os.getenv("OPENAI_COMPOSITE_API_KEY") or os.getenv("CLAUDE_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.target_api_url = os.getenv("OPENAI_COMPOSITE_API_URL") or os.getenv("CLAUDE_API_URL") or "https://api.openai.com/v1"
        self.target_model = os.getenv("OPENAI_COMPOSITE_MODEL") or os.getenv("CLAUDE_MODEL") or "gpt-3.5-turbo"
        
        # 检查必要的API密钥
        if not self.deepseek_api_key:
            raise ValueError("缺少 DeepSeek API 密钥，请在环境变量中设置 DEEPSEEK_API_KEY")
        
        if not self.target_api_key:
            raise ValueError("缺少目标模型 API 密钥，请在环境变量中设置相应的 API 密钥")
    
    def get_short_model_name(self):
        """
        获取目标模型的简短名称，用于文件命名
        :return: 简化的模型名称
        """
        # 从完整模型名称中提取简短名称
        model_name = self.target_model
        
        # 移除路径前缀 (例如 "anthropic/" 或 "google/")
        if "/" in model_name:
            model_name = model_name.split("/")[-1]
        
        # 提取主要模型名称 (例如 "claude-3-sonnet" 变为 "claude")
        if "claude" in model_name.lower():
            return "claude"
        elif "gpt" in model_name.lower():
            return "gpt"
        elif "gemini" in model_name.lower():
            return "gemini"
        elif "llama" in model_name.lower():
            return "llama"
        elif "qwen" in model_name.lower():
            return "qwen"
        else:
            # 如果无法识别，返回原始名称的前10个字符
            return model_name[:10].lower()
    
    def generate_summary(self, content, stream=False, custom_prompt=None, template_path=None):
        """
        生成文本摘要
        :param content: 需要摘要的文本内容
        :param stream: 是否使用流式输出
        :param custom_prompt: 自定义提示词，如果提供则使用此提示词代替默认提示词
        :param template_path: 模板文件路径，如果提供则使用此模板
        :return: 生成的摘要文本
        """
        # 准备提示词
        system_prompt = "你是一个专业的内容编辑和文章撰写专家。"
        
        # 使用自定义提示词、模板或默认提示词
        if custom_prompt:
            user_prompt = custom_prompt.format(content=content)
        elif template_path:
            template = load_template(template_path)
            user_prompt = template.format(content=content)
        else:
            template = load_template()
            user_prompt = template.format(content=content)
        
        # 使用 DeepSeek 生成推理过程
        print("1. 使用 DeepSeek 生成推理过程...")
        reasoning = self._get_deepseek_reasoning(system_prompt, user_prompt)
        
        # 使用目标模型生成最终摘要
        print("2. 使用目标模型基于推理过程生成最终文章...")
        if stream:
            return self._get_target_model_summary_stream(system_prompt, user_prompt, reasoning)
        else:
            return self._get_target_model_summary(system_prompt, user_prompt, reasoning)
    
    def _get_deepseek_reasoning(self, system_prompt, user_prompt):
        """
        获取 DeepSeek 的推理过程
        :param system_prompt: 系统提示词
        :param user_prompt: 用户提示词
        :return: 推理过程文本
        """
        try:
            # 准备请求头和数据
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.deepseek_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7,
                "stream": False
            }
            
            # 发送请求
            import requests
            response = requests.post(
                self.deepseek_api_url,
                headers=headers,
                json=data
            )
            
            # 检查响应
            if response.status_code != 200:
                raise Exception(f"DeepSeek API 请求失败: {response.status_code}, {response.text}")
            
            # 解析响应
            response_data = response.json()
            
            # 提取推理内容
            if "choices" in response_data and len(response_data["choices"]) > 0:
                message = response_data["choices"][0]["message"]
                
                # 检查是否有原生推理内容
                if "reasoning_content" in message:
                    return message["reasoning_content"]
                
                # 如果没有原生推理内容，尝试从普通内容中提取
                content = message.get("content", "")
                
                # 尝试从内容中提取 <div className="think-block">...</div> 标签
                import re
                think_match = re.search(r'<div className="think-block">(.*?)</div>', content, re.DOTALL)
                if think_match:
                    return think_match.group(1).strip()
                
                # 如果没有找到标签，则使用完整内容作为推理
                return content
            
            raise Exception("无法从 DeepSeek 响应中提取推理内容")
        
        except Exception as e:
            print(f"获取 DeepSeek 推理过程失败: {str(e)}")
            # 返回一个简单的提示，表示推理过程获取失败
            return "无法获取推理过程，但我会尽力生成一篇高质量的文章。"
    
    def _get_target_model_summary(self, system_prompt, user_prompt, reasoning):
        """
        使用目标模型生成最终摘要
        :param system_prompt: 系统提示词
        :param user_prompt: 用户提示词
        :param reasoning: DeepSeek 的推理过程
        :return: 生成的摘要文本
        """
        try:
            # 创建 OpenAI 客户端
            client = OpenAI(
                api_key=self.target_api_key,
                base_url=self.target_api_url
            )
            
            # 构造结合推理过程的提示词
            combined_prompt = f"""这是我的原始请求：
            
            {user_prompt}
            
            以下是另一个模型的推理过程：
            
            {reasoning}
            
            请基于上述推理过程，提供你的最终文章。直接输出文章内容，不需要解释你的思考过程。
            """
            
            # 发送请求
            response = client.chat.completions.create(
                model=self.target_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": combined_prompt}
                ],
                temperature=0.7
            )
            
            # 提取回答
            if response.choices and len(response.choices) > 0:
                article = response.choices[0].message.content
                # 清理 Markdown 格式
                cleaned_markdown = clean_markdown_formatting(article)
                return cleaned_markdown
            
            raise Exception("无法从目标模型响应中提取内容")
        
        except Exception as e:
            print(f"获取目标模型摘要失败: {str(e)}")
            # 如果目标模型失败，则返回 DeepSeek 的推理作为备用
            return f"目标模型生成失败，以下是推理过程:\n\n{reasoning}"
    
    def _get_target_model_summary_stream(self, system_prompt, user_prompt, reasoning):
        """
        使用目标模型流式生成最终摘要
        :param system_prompt: 系统提示词
        :param user_prompt: 用户提示词
        :param reasoning: DeepSeek 的推理过程
        :return: 生成的摘要文本
        """
        try:
            # 创建 OpenAI 客户端
            client = OpenAI(
                api_key=self.target_api_key,
                base_url=self.target_api_url
            )
            
            # 构造结合推理过程的提示词
            combined_prompt = f"""这是我的原始请求：
            
            {user_prompt}
            
            以下是另一个模型的推理过程：
            
            {reasoning}
            
            请基于上述推理过程，提供你的最终文章。直接输出文章内容，不需要解释你的思考过程。
            """
            
            # 发送流式请求
            stream_response = client.chat.completions.create(
                model=self.target_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": combined_prompt}
                ],
                temperature=0.7,
                stream=True
            )
            
            # 收集完整响应
            full_response = ""
            
            print("生成文章中...")
            for chunk in stream_response:
                if not chunk.choices:
                    continue
                content_chunk = chunk.choices[0].delta.content
                if content_chunk:
                    # 打印进度
                    print(".", end="", flush=True)
                    # 收集完整响应
                    full_response += content_chunk
            print("\n文章生成完成!")
            
            # 清理 Markdown 格式
            cleaned_markdown = clean_markdown_formatting(full_response)
            return cleaned_markdown
        
        except Exception as e:
            print(f"获取目标模型流式摘要失败: {str(e)}")
            # 如果目标模型失败，则返回 DeepSeek 的推理作为备用
            return f"目标模型生成失败，以下是推理过程:\n\n{reasoning}"

