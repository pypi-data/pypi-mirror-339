import yt_dlp
import whisper
import torch
from pathlib import Path
import openai
import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
import shutil

# Load environment variables from .env file
load_dotenv()

# 创建模板目录
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# 默认模板
DEFAULT_TEMPLATE = """请将以下文本改写成一篇完整、连贯、专业的文章。

要求：
1. 你是一名资深科技领域编辑，同时具备优秀的文笔，文本转为一篇文章，确保段落清晰，文字连贯，可读性强，必要修改调整段落结构，确保内容具备良好的逻辑性。
2. 添加适当的小标题来组织内容
3. 以markdown格式输出，充分利用标题、列表、引用等格式元素
4. 如果原文有技术内容，确保准确表达并提供必要的解释

原文内容：
{content}
"""

# 创建默认模板文件
DEFAULT_TEMPLATE_PATH = os.path.join(TEMPLATES_DIR, "default.txt")
if not os.path.exists(DEFAULT_TEMPLATE_PATH):
    with open(DEFAULT_TEMPLATE_PATH, "w", encoding="utf-8") as f:
        f.write(DEFAULT_TEMPLATE)

def load_template(template_path=None):
    """
    加载模板文件
    :param template_path: 模板文件路径，如果为None则使用默认模板
    :return: 模板内容
    """
    if template_path is None:
        # 使用默认模板
        template_path = DEFAULT_TEMPLATE_PATH
    
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"加载模板文件失败: {str(e)}")
        print(f"使用内置默认模板")
        return DEFAULT_TEMPLATE

def sanitize_filename(filename):
    """
    清理文件名，移除或替换不安全的字符
    :param filename: 原始文件名
    :return: 清理后的文件名
    """
    # 替换不安全的字符
    unsafe_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '【', '】', '｜']
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    
    # 替换空格为下划线
    filename = filename.replace(' ', '_')
    
    # 移除前导和尾随空格
    filename = filename.strip()
    
    # 确保文件名不为空
    if not filename:
        filename = "audio_file"
    
    return filename

def download_youtube_video(youtube_url, output_dir=None, audio_only=True):
    """
    从YouTube下载视频或音频
    :param youtube_url: YouTube视频链接
    :param output_dir: 输出目录，如果为None，则根据audio_only自动选择目录
    :param audio_only: 是否只下载音频，如果为False则下载视频
    :return: 下载文件的完整路径
    """
    # 根据下载类型选择默认输出目录
    if output_dir is None:
        output_dir = "downloads" if audio_only else "videos"
    
    # 创建输出目录
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    print(f"输出目录: {os.path.abspath(output_dir)}")
    
    # 设置yt-dlp的选项
    if audio_only:
        # 音频下载选项
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'quiet': False  # 修改为False以显示下载进度和错误信息
        }
        expected_ext = "mp3"
    else:
        # 视频下载选项（最佳画质）
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # 优先选择mp4格式
            'merge_output_format': 'mp4',  # 确保输出为mp4
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'quiet': False  # 显示下载进度和错误信息
        }
        expected_ext = "mp4"
    
    try:
        print(f"开始{'音频' if audio_only else '视频'}下载: {youtube_url}")
        print(f"下载选项: {'仅音频' if audio_only else '完整视频'}")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 获取视频信息
            print(f"正在获取视频信息...")
            info = ydl.extract_info(youtube_url, download=True)
            
            # 获取原始文件名并清理
            original_title = info['title']
            sanitized_title = sanitize_filename(original_title)
            
            # 构建文件路径
            original_path = os.path.join(output_dir, f"{original_title}.{expected_ext}")
            sanitized_path = os.path.join(output_dir, f"{sanitized_title}.{expected_ext}")
            
            print(f"原始文件路径: {original_path}")
            print(f"清理后的文件路径: {sanitized_path}")
            
            # 如果文件名被清理了，需要重命名文件
            if original_path != sanitized_path and os.path.exists(original_path):
                try:
                    os.rename(original_path, sanitized_path)
                    print(f"文件已重命名: {original_title} -> {sanitized_title}")
                except Exception as e:
                    print(f"重命名文件失败: {str(e)}")
            
            # 检查文件是否存在
            if os.path.exists(sanitized_path):
                print(f"文件下载成功: {sanitized_path}")
                return sanitized_path
            elif os.path.exists(original_path):
                print(f"文件下载成功但未重命名: {original_path}")
                return original_path
            else:
                # 尝试查找可能的文件
                possible_files = list(Path(output_dir).glob(f"*.{expected_ext}"))
                if possible_files:
                    newest_file = max(possible_files, key=os.path.getctime)
                    print(f"找到可能的文件: {newest_file}")
                    return str(newest_file)
                
                # 如果找不到预期扩展名的文件，尝试查找任何新文件
                all_files = list(Path(output_dir).glob("*.*"))
                if all_files:
                    newest_file = max(all_files, key=os.path.getctime)
                    print(f"找到可能的文件（不同扩展名）: {newest_file}")
                    return str(newest_file)
                
                raise Exception(f"下载成功但找不到文件，请检查 {output_dir} 目录")
    except yt_dlp.utils.DownloadError as e:
        print(f"下载失败详细信息: {str(e)}")
        raise Exception(f"下载失败: {str(e)}")
    except Exception as e:
        print(f"下载失败详细信息: {str(e)}")
        raise Exception(f"下载失败: {str(e)}")

def download_youtube_audio(youtube_url, output_dir="downloads"):
    """
    从YouTube视频中下载音频
    :param youtube_url: YouTube视频链接
    :param output_dir: 输出目录
    :return: 音频文件的完整路径
    """
    # 创建输出目录
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 设置yt-dlp的选项
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 获取视频信息
            info = ydl.extract_info(youtube_url, download=True)
            
            # 获取原始文件名并清理
            original_title = info['title']
            sanitized_title = sanitize_filename(original_title)
            
            # 如果文件名被清理了，需要重命名文件
            original_path = os.path.join(output_dir, f"{original_title}.mp3")
            sanitized_path = os.path.join(output_dir, f"{sanitized_title}.mp3")
            
            if original_path != sanitized_path and os.path.exists(original_path):
                try:
                    os.rename(original_path, sanitized_path)
                    print(f"文件已重命名: {original_title} -> {sanitized_title}")
                except Exception as e:
                    print(f"重命名文件失败: {str(e)}")
            
            # 返回清理后的文件路径
            return sanitized_path
    except Exception as e:
        raise Exception(f"下载音频失败: {str(e)}")

def extract_audio_from_video(video_path, output_dir="downloads"):
    """
    从视频文件中提取音频
    :param video_path: 视频文件路径
    :param output_dir: 输出目录，默认为downloads
    :return: 提取的音频文件路径
    """
    try:
        # 创建输出目录
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # 获取视频文件名（不含扩展名）
        video_name = Path(video_path).stem
        sanitized_name = sanitize_filename(video_name)
        
        # 设置输出音频路径
        audio_path = os.path.join(output_dir, f"{sanitized_name}.mp3")
        
        print(f"正在从视频提取音频: {video_path} -> {audio_path}")
        
        # 检查ffmpeg是否可用
        try:
            import subprocess
            result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
            if result.returncode != 0:
                print("警告: ffmpeg命令不可用。请确保已安装ffmpeg并添加到系统PATH中。")
                print("您可以从 https://ffmpeg.org/download.html 下载ffmpeg。")
                raise Exception("ffmpeg命令不可用")
        except FileNotFoundError:
            print("错误: 找不到ffmpeg命令。请确保已安装ffmpeg并添加到系统PATH中。")
            print("您可以从 https://ffmpeg.org/download.html 下载ffmpeg。")
            raise Exception("找不到ffmpeg命令")
        
        # 首先检查视频文件是否包含音频流
        import subprocess
        probe_cmd = ["ffmpeg", "-i", video_path, "-hide_banner"]
        probe_process = subprocess.Popen(probe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, stderr = probe_process.communicate()
        stderr_text = stderr.decode('utf-8', errors='ignore')
        
        # 检查输出中是否包含音频流信息
        if "Stream" in stderr_text and "Audio" not in stderr_text:
            print("警告: 视频文件不包含音频流")
            print("错误详情:")
            print(stderr_text)
            raise Exception("视频文件不包含音频流，无法提取音频")
        
        # 使用ffmpeg-python库提取音频
        try:
            import ffmpeg
            # 使用ffmpeg-python库
            try:
                # 先获取视频信息
                probe = ffmpeg.probe(video_path)
                # 检查是否有音频流
                audio_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'audio']
                if not audio_streams:
                    raise Exception("视频文件不包含音频流，无法提取音频")
                
                # 有音频流，继续处理
                (
                    ffmpeg
                    .input(video_path)
                    .output(audio_path, acodec='libmp3lame', q=0)
                    .run(quiet=False, overwrite_output=True, capture_stdout=True, capture_stderr=True)
                )
                print(f"音频提取完成: {audio_path}")
            except ffmpeg._run.Error as e:
                print(f"ffmpeg错误: {str(e)}")
                print("尝试使用subprocess直接调用ffmpeg...")
                raise Exception("ffmpeg-python库调用失败，尝试使用subprocess")
        except (ImportError, Exception) as e:
            # 如果ffmpeg-python库不可用或调用失败，回退到subprocess
            print(f"使用subprocess调用ffmpeg: {str(e)}")
            import subprocess
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-q:a", "0",
                "-vn",
                "-y",  # 覆盖输出文件
                audio_path
            ]
            
            # 执行命令，捕获输出
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                stderr_text = stderr.decode('utf-8', errors='ignore')
                print(f"ffmpeg命令执行失败，返回代码: {process.returncode}")
                print(f"错误输出: {stderr_text}")
                
                # 检查是否是因为没有音频流
                if "Stream map 'a' matches no streams" in stderr_text or "does not contain any stream" in stderr_text:
                    raise Exception("视频文件不包含音频流，无法提取音频")
                else:
                    raise Exception(f"ffmpeg命令执行失败: {stderr_text}")
            
            print(f"音频提取完成: {audio_path}")
        
        # 检查生成的音频文件是否存在
        if not os.path.exists(audio_path):
            raise Exception(f"音频文件未生成: {audio_path}")
        
        # 检查音频文件大小
        file_size = os.path.getsize(audio_path)
        if file_size == 0:
            raise Exception(f"生成的音频文件大小为0: {audio_path}")
        
        print(f"音频文件大小: {file_size} 字节")
        return audio_path
    except Exception as e:
        error_msg = f"从视频提取音频失败: {str(e)}"
        print(error_msg)
        raise Exception(error_msg)

def transcribe_audio_to_text(audio_path, output_dir="transcripts", model_size="small"):
    """
    使用Whisper将音频转换为文本
    :param audio_path: 音频文件路径
    :param output_dir: 输出目录
    :param model_size: 模型大小，可选 "tiny", "base", "small", "medium", "large"
    :return: 文本文件的路径
    """
    # 创建输出目录
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    try:
        # 检测设备
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"使用设备: {device}")
        
        # 确保CUDA可用时正确设置
        if device == "cuda":
            print(f"CUDA是否可用: {torch.cuda.is_available()}")
            print(f"CUDA设备数量: {torch.cuda.device_count()}")
            print(f"当前CUDA设备: {torch.cuda.current_device()}")
            print(f"CUDA设备名称: {torch.cuda.get_device_name(0)}")
        
        # 加载模型
        print(f"加载 {model_size} 模型...")
        model = whisper.load_model(model_size, device=device)
        
        # 转录音频
        print("开始转录音频...")
        result = model.transcribe(audio_path)
        print("转录完成!")
        
        # 生成输出文件路径
        base_name = Path(audio_path).stem
        sanitized_base_name = sanitize_filename(base_name)
        output_path = os.path.join(output_dir, f"{sanitized_base_name}_transcript.txt")
        
        # 保存转录文本
        with open(output_path, "w", encoding="utf-8") as f:
            # 如果result包含segments，按段落保存
            if 'segments' in result:
                for segment in result['segments']:
                    f.write(f"{segment['text'].strip()}\n\n")
            else:
                f.write(result['text'])
        
        return output_path
    except Exception as e:
        raise Exception(f"音频转文字失败: {str(e)}")

def transcribe_only(audio_path, whisper_model_size="medium", output_dir="transcripts"):
    """
    仅将音频转换为文本，不进行摘要生成
    
    参数:
        audio_path (str): 音频文件路径
        whisper_model_size (str): Whisper模型大小
        output_dir (str): 转录文本保存目录
    
    返回:
        str: 转录文本文件路径
    """
    print(f"正在将音频转换为文本: {audio_path}")
    
    # 检查文件是否存在
    if not os.path.exists(audio_path):
        print(f"错误: 文件 {audio_path} 不存在")
        return None
    
    # 转录音频
    text_path = transcribe_audio_to_text(audio_path, output_dir=output_dir, model_size=whisper_model_size)
    
    print(f"音频转文本完成，文本已保存至: {text_path}")
    return text_path

def process_local_audio(audio_path, model=None, api_key=None, base_url=None, whisper_model_size="medium", stream=True, summary_dir="summaries", custom_prompt=None, template_path=None):
    """
    处理本地音频文件的主函数
    :param audio_path: 本地音频文件路径
    :param model: 使用的模型名称，默认从环境变量获取
    :param api_key: API密钥，默认从环境变量获取
    :param base_url: 自定义API基础URL，默认从环境变量获取
    :param whisper_model_size: Whisper模型大小，默认为medium
    :param stream: 是否使用流式输出生成总结，默认为True
    :param summary_dir: 总结文件保存目录，默认为summaries
    :param custom_prompt: 自定义提示词，如果提供则使用此提示词代替默认提示词
    :param template_path: 模板文件路径，如果提供则使用此模板
    :return: 总结文件的路径
    """
    try:
        print("1. 开始转录音频...")
        text_path = transcribe_audio_to_text(audio_path, model_size=whisper_model_size)
        print(f"转录文本已保存到: {text_path}")
        
        print("\n2. 开始生成文章...")
        summary_path = summarize_text(
            text_path, 
            model=model, 
            api_key=api_key, 
            base_url=base_url, 
            stream=stream,
            output_dir=summary_dir,
            custom_prompt=custom_prompt,
            template_path=template_path
        )
        print(f"文章已保存到: {summary_path}")
        
        return summary_path
    except Exception as e:
        print(f"处理过程中出现错误: {str(e)}")
        return None

def process_local_video(video_path, model=None, api_key=None, base_url=None, whisper_model_size="medium", stream=True, summary_dir="summaries", custom_prompt=None, template_path=None):
    """
    处理本地视频文件的主函数
    :param video_path: 本地视频文件路径
    :param model: 使用的模型名称，默认从环境变量获取
    :param api_key: API密钥，默认从环境变量获取
    :param base_url: 自定义API基础URL，默认从环境变量获取
    :param whisper_model_size: Whisper模型大小，默认为medium
    :param stream: 是否使用流式输出生成总结，默认为True
    :param summary_dir: 总结文件保存目录，默认为summaries
    :param custom_prompt: 自定义提示词，如果提供则使用此提示词代替默认提示词
    :param template_path: 模板文件路径，如果提供则使用此模板
    :return: 总结文件的路径
    """
    try:
        print("1. 从视频中提取音频...")
        audio_path = extract_audio_from_video(video_path, output_dir="downloads")
        print(f"音频已提取到: {audio_path}")
        
        print("2. 开始转录音频...")
        text_path = transcribe_audio_to_text(audio_path, model_size=whisper_model_size)
        print(f"转录文本已保存到: {text_path}")
        
        print("\n3. 开始生成文章...")
        summary_path = summarize_text(
            text_path, 
            model=model, 
            api_key=api_key, 
            base_url=base_url, 
            stream=stream,
            output_dir=summary_dir,
            custom_prompt=custom_prompt,
            template_path=template_path
        )
        print(f"文章已保存到: {summary_path}")
        
        return summary_path
    except Exception as e:
        print(f"处理过程中出现错误: {str(e)}")
        return None

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
        # 创建输出目录
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # 读取文本文件
        with open(text_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 使用组合模型生成摘要
        composite = TextSummaryComposite()
        
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
        if not self.deepseek_api_key and not self.target_api_key:
            raise ValueError("缺少 API 密钥，请在环境变量中设置 DEEPSEEK_API_KEY 或 OPENAI_API_KEY")
    
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
        
        # 如果有 DeepSeek API 密钥，先使用 DeepSeek 生成推理过程
        reasoning = None
        if self.deepseek_api_key:
            try:
                print("1. 使用 DeepSeek 生成推理过程...")
                reasoning = self._get_deepseek_reasoning(system_prompt, user_prompt)
                print("2. 使用目标模型基于推理过程生成最终文章...")
            except Exception as e:
                print(f"警告: DeepSeek 推理过程生成失败: {str(e)}")
                print("将直接使用目标模型生成文章...")
                reasoning = None
        else:
            print("未设置 DeepSeek API 密钥，将直接使用目标模型生成文章...")
        
        # 使用目标模型生成最终摘要
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
    
    def _get_target_model_summary(self, system_prompt, user_prompt, reasoning=None):
        """
        使用目标模型生成最终摘要
        :param system_prompt: 系统提示词
        :param user_prompt: 用户提示词
        :param reasoning: DeepSeek 的推理过程，可以为 None
        :return: 生成的摘要文本
        """
        try:
            # 创建 OpenAI 客户端
            client = OpenAI(
                api_key=self.target_api_key,
                base_url=self.target_api_url
            )
            
            # 构造提示词，根据是否有推理过程来决定
            if reasoning:
                combined_prompt = f"""这是我的原始请求：
                
                {user_prompt}
                
                以下是另一个模型的推理过程：
                
                {reasoning}
                
                请基于上述推理过程，提供你的最终文章。直接输出文章内容，不需要解释你的思考过程。
                """
            else:
                combined_prompt = f"""请根据以下内容生成一篇高质量的文章：
                
                {user_prompt}
                
                直接输出文章内容，不需要解释你的思考过程。
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
            if reasoning:
                return f"目标模型生成失败，以下是推理过程:\n\n{reasoning}"
            else:
                raise Exception(f"文章生成失败: {str(e)}")
    
    def _get_target_model_summary_stream(self, system_prompt, user_prompt, reasoning=None):
        """
        使用目标模型流式生成最终摘要
        :param system_prompt: 系统提示词
        :param user_prompt: 用户提示词
        :param reasoning: DeepSeek 的推理过程，可以为 None
        :return: 生成的摘要文本
        """
        try:
            # 创建 OpenAI 客户端
            client = OpenAI(
                api_key=self.target_api_key,
                base_url=self.target_api_url
            )
            
            # 构造提示词，根据是否有推理过程来决定
            if reasoning:
                combined_prompt = f"""这是我的原始请求：
                
                {user_prompt}
                
                以下是另一个模型的推理过程：
                
                {reasoning}
                
                请基于上述推理过程，提供你的最终文章。直接输出文章内容，不需要解释你的思考过程。
                """
            else:
                combined_prompt = f"""请根据以下内容生成一篇高质量的文章：
                
                {user_prompt}
                
                直接输出文章内容，不需要解释你的思考过程。
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

def process_youtube_video(youtube_url, model=None, api_key=None, base_url=None, whisper_model_size="medium", stream=True, summary_dir="summaries", download_video=False, custom_prompt=None, template_path=None):
    """
    处理YouTube视频的主函数
    :param youtube_url: YouTube视频链接
    :param model: 使用的模型名称，默认从环境变量获取
    :param api_key: API密钥，默认从环境变量获取
    :param base_url: 自定义API基础URL，默认从环境变量获取
    :param whisper_model_size: Whisper模型大小，默认为medium
    :param stream: 是否使用流式输出生成总结，默认为True
    :param summary_dir: 总结文件保存目录，默认为summaries
    :param download_video: 是否下载视频（True）或仅音频（False），默认为False
    :param custom_prompt: 自定义提示词，如果提供则使用此提示词代替默认提示词
    :param template_path: 模板文件路径，如果提供则使用此模板
    :return: 总结文件的路径
    """
    try:
        print("1. 开始下载YouTube内容...")
        audio_path = None
        
        if download_video:
            print("下载视频（最佳画质）...")
            try:
                # 使用videos目录存储视频
                file_path = download_youtube_video(youtube_url, output_dir="videos", audio_only=False)
                print(f"视频已下载到: {file_path}")
                
                # 检查文件是否存在
                if not os.path.exists(file_path):
                    raise Exception(f"下载的视频文件不存在: {file_path}")
                
                # 如果下载的是视频，我们需要提取音频
                print("从视频中提取音频...")
                try:
                    audio_path = extract_audio_from_video(file_path, output_dir="downloads")
                    print(f"音频已提取到: {audio_path}")
                except Exception as e:
                    print(f"从视频提取音频失败: {str(e)}")
                    print("尝试直接下载音频作为备选方案...")
                    audio_path = download_youtube_video(youtube_url, output_dir="downloads", audio_only=True)
            except Exception as e:
                print(f"视频下载失败: {str(e)}")
                print("尝试改为下载音频...")
                audio_path = download_youtube_video(youtube_url, output_dir="downloads", audio_only=True)
        else:
            print("仅下载音频...")
            # 使用downloads目录存储音频
            audio_path = download_youtube_video(youtube_url, output_dir="downloads", audio_only=True)
        
        if not audio_path or not os.path.exists(audio_path):
            raise Exception(f"无法获取有效的音频文件")
            
        print(f"音频文件路径: {audio_path}")
        
        print("\n2. 开始转录音频...")
        text_path = transcribe_audio_to_text(audio_path, model_size=whisper_model_size)
        print(f"转录文本已保存到: {text_path}")
        
        print("\n3. 开始生成文章...")
        summary_path = summarize_text(
            text_path, 
            model=model, 
            api_key=api_key, 
            base_url=base_url, 
            stream=stream,
            output_dir=summary_dir,
            custom_prompt=custom_prompt,
            template_path=template_path
        )
        print(f"文章已保存到: {summary_path}")
        
        return summary_path
    except Exception as e:
        print(f"处理过程中出现错误: {str(e)}")
        import traceback
        print(f"错误详情:\n{traceback.format_exc()}")
        return None

def process_youtube_videos_batch(youtube_urls, model=None, api_key=None, base_url=None, whisper_model_size="medium", stream=True, summary_dir="summaries", download_video=False, custom_prompt=None, template_path=None):
    """
    批量处理多个YouTube视频
    :param youtube_urls: YouTube视频链接列表
    :param model: 使用的模型名称，默认从环境变量获取
    :param api_key: API密钥，默认从环境变量获取
    :param base_url: 自定义API基础URL，默认从环境变量获取
    :param whisper_model_size: Whisper模型大小，默认为medium
    :param stream: 是否使用流式输出生成总结，默认为True
    :param summary_dir: 总结文件保存目录，默认为summaries
    :param download_video: 是否下载视频（True）或仅音频（False），默认为False
    :param custom_prompt: 自定义提示词，如果提供则使用此提示词代替默认提示词
    :param template_path: 模板文件路径，如果提供则使用此模板
    :return: 处理结果的字典，键为URL，值为对应的总结文件路径或错误信息
    """
    results = {}
    total_urls = len(youtube_urls)
    
    print(f"开始批量处理 {total_urls} 个YouTube视频...")
    print(f"下载选项: {'完整视频' if download_video else '仅音频'}")
    
    for i, url in enumerate(youtube_urls):
        print(f"\n处理第 {i+1}/{total_urls} 个视频: {url}")
        try:
            summary_path = process_youtube_video(
                url,
                model=model,
                api_key=api_key,
                base_url=base_url,
                whisper_model_size=whisper_model_size,
                stream=stream,
                summary_dir=summary_dir,
                download_video=download_video,  # 确保正确传递download_video参数
                custom_prompt=custom_prompt,
                template_path=template_path
            )
            
            if summary_path:
                print(f"视频处理成功: {url}")
                results[url] = {
                    "status": "success",
                    "summary_path": summary_path
                }
            else:
                print(f"视频处理失败: {url}")
                results[url] = {
                    "status": "failed",
                    "error": "处理过程中出现错误，请查看日志获取详细信息"
                }
        except Exception as e:
            print(f"处理视频时出错: {url}")
            print(f"错误详情: {str(e)}")
            results[url] = {
                "status": "failed",
                "error": str(e)
            }
    
    # 打印处理结果统计
    success_count = sum(1 for result in results.values() if result["status"] == "success")
    failed_count = sum(1 for result in results.values() if result["status"] == "failed")
    
    print("\n批量处理完成!")
    print(f"总计: {total_urls} 个视频")
    print(f"成功: {success_count} 个视频")
    print(f"失败: {failed_count} 个视频")
    
    if failed_count > 0:
        print("\n失败的视频:")
        for url, result in results.items():
            if result["status"] == "failed":
                print(f"- {url}: {result['error']}")
    
    return results

def process_local_text(text_path, model=None, api_key=None, base_url=None, stream=True, summary_dir="summaries", custom_prompt=None, template_path=None):
    """
    处理本地文本文件，直接生成摘要和文章
    
    参数:
        text_path (str): 本地文本文件路径
        model (str): 模型名称
        api_key (str): API密钥
        base_url (str): API基础URL
        stream (bool): 是否使用流式输出
        summary_dir (str): 摘要保存目录
        custom_prompt (str): 自定义提示词
        template_path (str): 模板路径
    
    返回:
        str: 生成的文章文件路径
    """
    print(f"正在处理本地文本文件: {text_path}")
    
    # 检查文件是否存在
    if not os.path.exists(text_path):
        print(f"错误: 文件 {text_path} 不存在")
        return None
    
    # 检查文件是否为文本文件
    if not text_path.lower().endswith(('.txt', '.md')):
        print(f"警告: 文件 {text_path} 可能不是文本文件，但仍将尝试处理")
    
    # 直接生成摘要
    summary_file = summarize_text(
        text_path, 
        model=model, 
        api_key=api_key, 
        base_url=base_url, 
        stream=stream, 
        output_dir=summary_dir,
        custom_prompt=custom_prompt,
        template_path=template_path
    )
    
    print(f"文本处理完成，文章已保存至: {summary_file}")
    return summary_file

def create_template(template_name, content=None):
    """
    创建新的模板文件
    :param template_name: 模板名称
    :param content: 模板内容，如果为None则使用默认模板内容
    :return: 模板文件路径
    """
    if not template_name.endswith('.txt'):
        template_name = f"{template_name}.txt"
    
    template_path = os.path.join(TEMPLATES_DIR, template_name)
    
    if content is None:
        content = DEFAULT_TEMPLATE
    
    with open(template_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"模板已创建: {template_path}")
    return template_path

def list_templates():
    """
    列出所有可用的模板
    :return: 模板文件列表
    """
    templates = []
    for file in os.listdir(TEMPLATES_DIR):
        if file.endswith('.txt'):
            templates.append(file)
    
    return templates

def clean_markdown_formatting(markdown_text):
    """
    Clean up markdown formatting issues
    :param markdown_text: Original markdown text
    :return: Cleaned markdown text
    """
    import re
    
    # Split the text into lines for processing
    lines = markdown_text.split('\n')
    result_lines = []
    
    # Track if we're inside a code block
    in_code_block = False
    current_code_language = None
    
    # First, check if the first line is ```markdown and remove it
    if lines and (lines[2].strip() == '```markdown' or lines[2].strip() == '```Markdown' or lines[2].strip() == '``` markdown'):
        lines = lines[3:]  # Remove the first line
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for code block start
        code_block_start = re.match(r'^(\s*)```\s*(\w*)\s*$', line)
        if code_block_start and not in_code_block:
            # Starting a code block
            in_code_block = True
            indent = code_block_start.group(1)
            language = code_block_start.group(2)
            current_code_language = language
            
            # Add the properly formatted code block start
            if language:
                result_lines.append(f"{indent}```{language}")
            else:
                result_lines.append(f"{indent}```")
        
        # Check for code block end
        elif re.match(r'^(\s*)```\s*$', line) and in_code_block:
            # Ending a code block
            in_code_block = False
            current_code_language = None
            result_lines.append(line)
        
        # Check for standalone triple backticks that aren't part of code blocks
        elif re.match(r'^(\s*)```\s*(markdown|Markdown)\s*$', line) and not in_code_block:
            # Skip unnecessary ```markdown markers
            pass
        elif line.strip() == '```' and not in_code_block:
            # Skip standalone closing backticks that aren't closing a code block
            pass
        
        # Regular line, add it to the result
        else:
            result_lines.append(line)
        
        i += 1
    
    # Ensure all code blocks are closed
    if in_code_block:
        result_lines.append("```")
    
    # Remove any trailing empty lines
    while result_lines and not result_lines[-1].strip():
        result_lines.pop()
    
    return '\n'.join(result_lines)

def create_example_batch_file(filename="youtube_urls.txt"):
    """
    创建示例批处理文件，用于批量处理YouTube视频
    :param filename: 文件名
    :return: 文件路径
    """
    content = """# YouTube视频URL列表，每行一个URL
# 以#开头的行会被忽略（用于注释）

# 示例URL（请替换为您自己的URL）
https://www.youtube.com/watch?v=example1
https://www.youtube.com/watch?v=example2
https://www.youtube.com/watch?v=example3
"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"示例批处理文件已创建: {os.path.abspath(filename)}")
    print("请编辑此文件，添加您要处理的YouTube视频URL，然后使用以下命令运行批处理:")
    print(f"python -m youtube_assistant --batch {filename}")
    
    return os.path.abspath(filename)

def main_cli():
    """
    命令行入口函数
    """
    import argparse
    import sys
    
    # 设置控制台输出编码为UTF-8
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='从YouTube视频或本地音频/视频文件中提取文本，并生成文章')
    
    # 创建互斥组，用户必须提供YouTube URL或本地音频/视频文件
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument('--youtube', type=str, help='YouTube视频URL')
    source_group.add_argument('--audio', type=str, help='本地音频文件路径')
    source_group.add_argument('--video', type=str, help='本地视频文件路径')
    source_group.add_argument('--text', type=str, help='本地文本文件路径，直接进行摘要生成')
    source_group.add_argument('--batch', type=str, help='包含多个YouTube URL的文本文件路径，每行一个URL')
    source_group.add_argument('--urls', nargs='+', type=str, help='多个YouTube URL，用空格分隔')
    source_group.add_argument('--create-batch-file', action='store_true', help='创建示例批处理文件')
    source_group.add_argument('--create-template', type=str, help='创建新模板，需要指定模板名称')
    source_group.add_argument('--list-templates', action='store_true', help='列出所有可用的模板')
    
    # 其他参数
    parser.add_argument('--model', type=str, help='使用的模型名称，默认从环境变量获取')
    parser.add_argument('--api-key', type=str, help='API密钥，默认从环境变量获取')
    parser.add_argument('--base-url', type=str, help='自定义API基础URL，默认从环境变量获取')
    parser.add_argument('--whisper-model', type=str, default='small', 
                      choices=['tiny', 'base', 'small', 'medium', 'large'],
                      help='Whisper模型大小，默认为small')
    parser.add_argument('--no-stream', action='store_true', help='不使用流式输出')
    parser.add_argument('--summary-dir', type=str, default='summaries', help='文章保存目录，默认为summaries')
    parser.add_argument('--download-video', action='store_true', help='下载视频而不仅仅是音频（仅适用于YouTube）')
    parser.add_argument('--batch-file-name', type=str, default='youtube_urls.txt', help='创建示例批处理文件时的文件名')
    parser.add_argument('--prompt', type=str, help='自定义提示词，用于指导文章生成。使用{content}作为占位符表示转录内容')
    parser.add_argument('--template', type=str, help='使用指定的模板文件，可以是模板名称或完整路径')
    parser.add_argument('--template-content', type=str, help='创建模板时的模板内容，仅与--create-template一起使用')
    parser.add_argument('--transcribe-only', action='store_true', help='仅将音频转换为文本，不进行摘要生成')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 处理模板路径
    template_path = None
    if args.template:
        # 检查是否是完整路径
        if os.path.exists(args.template):
            template_path = args.template
        else:
            # 检查是否是模板名称
            if not args.template.endswith('.txt'):
                template_name = f"{args.template}.txt"
            else:
                template_name = args.template
            
            potential_path = os.path.join(TEMPLATES_DIR, template_name)
            if os.path.exists(potential_path):
                template_path = potential_path
            else:
                print(f"警告: 找不到模板 '{args.template}'，将使用默认模板")
    
    # 如果用户请求创建示例批处理文件
    if args.create_batch_file:
        create_example_batch_file(args.batch_file_name)
        return
    
    # 如果用户请求创建新模板
    if args.create_template:
        create_template(args.create_template, args.template_content)
        return
    
    # 如果用户请求列出所有模板
    if args.list_templates:
        templates = list_templates()
        if templates:
            print("可用的模板:")
            for template in templates:
                print(f"- {template}")
        else:
            print("没有找到可用的模板")
        return
    
    # 如果没有提供参数，显示帮助信息
    if not (args.youtube or args.audio or args.video or args.text or args.batch or args.urls):
        parser.print_help()
        print("\n示例用法:")
        print("# 处理单个YouTube视频:")
        print("python youtube_transcriber.py --youtube https://www.youtube.com/watch?v=your_video_id")
        print("python youtube_transcriber.py --youtube https://www.youtube.com/watch?v=your_video_id --whisper-model large --no-stream")
        print("python youtube_transcriber.py --youtube https://www.youtube.com/watch?v=your_video_id --download-video")
        
        print("\n# 批量处理多个YouTube视频:")
        print("python youtube_transcriber.py --urls https://www.youtube.com/watch?v=id1 https://www.youtube.com/watch?v=id2")
        print("python youtube_transcriber.py --batch urls.txt  # 文件中每行一个URL")
        print("python youtube_transcriber.py --create-batch-file  # 创建示例批处理文件")
        
        print("\n# 处理本地音频文件:")
        print("python youtube_transcriber.py --audio path/to/your/audio.mp3")
        print("python youtube_transcriber.py --audio path/to/your/audio.mp3 --whisper-model large --summary-dir my_articles")
        
        print("\n# 处理本地视频文件:")
        print("python youtube_transcriber.py --video path/to/your/video.mp4")
        print("python youtube_transcriber.py --video path/to/your/video.mp4 --whisper-model large --summary-dir my_articles")
        
        print("\n# 处理本地文本文件:")
        print("python youtube_transcriber.py --text path/to/your/text.txt")
        print("python youtube_transcriber.py --text path/to/your/text.txt --summary-dir my_articles")
        
        print("\n# 使用自定义提示词:")
        print('python youtube_transcriber.py --youtube https://www.youtube.com/watch?v=your_video_id --prompt "请将以下内容总结为一篇新闻报道：\\n\\n{content}"')
        
        print("\n# 使用模板功能:")
        print("python youtube_transcriber.py --youtube https://www.youtube.com/watch?v=your_video_id --template news")
        print("python youtube_transcriber.py --create-template news --template-content \"请将以下内容改写为新闻报道格式：\\n\\n{content}\"")
        print("python youtube_transcriber.py --list-templates")
    else:
        # 处理自定义提示词
        custom_prompt = args.prompt
        
        # 处理YouTube视频、批量处理或本地音频/视频
        if args.youtube:
            # 处理单个YouTube视频
            if args.transcribe_only:
                summary_path = transcribe_only(download_youtube_video(args.youtube, output_dir="downloads", audio_only=True), whisper_model_size=args.whisper_model, output_dir="transcripts")
            else:
                summary_path = process_youtube_video(
                    args.youtube,
                    model=args.model,
                    api_key=args.api_key,
                    base_url=args.base_url,
                    whisper_model_size=args.whisper_model,
                    stream=not args.no_stream,
                    summary_dir=args.summary_dir,
                    download_video=args.download_video,
                    custom_prompt=custom_prompt,
                    template_path=template_path
                )
            
            if summary_path:
                print(f"\n处理完成! 文章已保存到: {summary_path}")
            else:
                print("\n处理失败，请检查错误信息。")
                
        elif args.urls:
            # 直接从命令行处理多个URL
            results = process_youtube_videos_batch(
                args.urls,
                model=args.model,
                api_key=args.api_key,
                base_url=args.base_url,
                whisper_model_size=args.whisper_model,
                stream=not args.no_stream,
                summary_dir=args.summary_dir,
                download_video=args.download_video,
                custom_prompt=custom_prompt,
                template_path=template_path
            )
            
        elif args.batch:
            # 从文件读取URL列表
            try:
                with open(args.batch, 'r', encoding='utf-8') as f:
                    urls = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
                
                if not urls:
                    print(f"错误: 文件 {args.batch} 中没有找到有效的URL")
                else:
                    print(f"从文件 {args.batch} 中读取了 {len(urls)} 个URL")
                    results = process_youtube_videos_batch(
                        urls,
                        model=args.model,
                        api_key=args.api_key,
                        base_url=args.base_url,
                        whisper_model_size=args.whisper_model,
                        stream=not args.no_stream,
                        summary_dir=args.summary_dir,
                        download_video=args.download_video,
                        custom_prompt=custom_prompt,
                        template_path=template_path
                    )
            except Exception as e:
                print(f"读取批处理文件时出错: {str(e)}")
                
        elif args.video:
            # 处理本地视频文件
            if args.transcribe_only:
                summary_path = transcribe_only(extract_audio_from_video(args.video, output_dir="downloads"), whisper_model_size=args.whisper_model, output_dir="transcripts")
            else:
                summary_path = process_local_video(
                    args.video, 
                    model=args.model, 
                    api_key=args.api_key, 
                    base_url=args.base_url, 
                    whisper_model_size=args.whisper_model, 
                    stream=not args.no_stream, 
                    summary_dir=args.summary_dir,
                    custom_prompt=custom_prompt,
                    template_path=template_path
                )
            
            if summary_path:
                print(f"\n处理完成! 文章已保存到: {summary_path}")
            else:
                print("\n处理失败，请检查错误信息。")
                
        elif args.audio:
            # 处理本地音频文件
            if args.transcribe_only:
                summary_path = transcribe_only(args.audio, whisper_model_size=args.whisper_model, output_dir="transcripts")
            else:
                summary_path = process_local_audio(
                    args.audio, 
                    model=args.model, 
                    api_key=args.api_key, 
                    base_url=args.base_url, 
                    whisper_model_size=args.whisper_model, 
                    stream=not args.no_stream, 
                    summary_dir=args.summary_dir,
                    custom_prompt=custom_prompt,
                    template_path=template_path
                )
            
            if summary_path:
                print(f"\n处理完成! 文章已保存到: {summary_path}")
            else:
                print("\n处理失败，请检查错误信息。")
                
        elif args.text:
            # 处理本地文本文件
            summary_path = process_local_text(
                args.text,
                model=args.model,
                api_key=args.api_key,
                base_url=args.base_url,
                stream=not args.no_stream,
                summary_dir=args.summary_dir,
                custom_prompt=custom_prompt,
                template_path=template_path
            )
            
            if summary_path:
                print(f"\n处理完成! 文章已保存到: {summary_path}")
            else:
                print("\n处理失败，请检查错误信息。")
                
        else:
            parser.print_help()

if __name__ == "__main__":
    main_cli()