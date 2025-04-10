"""通用工具模块"""
import asyncio
import json
import os
import tempfile
import time
import urllib.parse
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple

import httpx
from mcp.types import TextContent, LoggingMessageNotification, LoggingMessageNotificationParams, LoggingLevel

@dataclass
class BaseResult:
    """基础结果数据类"""
    success: bool
    file_path: str
    error_message: Optional[str] = None
    download_url: Optional[str] = None

class Logger:
    """通用日志记录类"""
    def __init__(self, context, collect_info: bool = True):
        self.context = context
        self.collect_info = collect_info
        self.result_info = []

    async def log(self, level: str, message: str, add_to_result: bool = True):
        """记录日志并可选择添加到结果信息中"""
        print(f"log: {message}")
        log_message = LoggingMessageNotification(
            method="notifications/message",
            params=LoggingMessageNotificationParams(
                level=getattr(LoggingLevel, level.lower(), "info"),
                data=message
            )
        )
        await self.context.session.send_notification(log_message)
        if self.collect_info and add_to_result and level != "debug":
            self.result_info.append(message)

    async def error(self, message: str, error_class=RuntimeError):
        """处理错误：记录日志并抛出异常"""
        print(f"error: {message}")
        await self.log("error", message)
        raise error_class(message)

    def get_result_info(self) -> List[str]:
        """获取收集的日志信息"""
        return self.result_info

class FileHandler:
    """文件处理工具类"""
    def __init__(self, logger: Logger):
        self.logger = logger

    @staticmethod
    def is_url(path: str) -> bool:
        """检查路径是否为URL"""
        return path.startswith(("http://", "https://"))

    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """获取文件扩展名（小写）"""
        if "?" in file_path:  # 处理URL中的查询参数
            file_path = file_path.split("?")[0]
        return os.path.splitext(file_path)[1].lower()
        
    @staticmethod
    def get_input_format(file_path: str):
        """根据文件路径获取输入格式
        
        此方法需要导入InputFormat和INPUT_EXTENSIONS，
        但为避免循环导入，由调用者提供转换逻辑
        """
        ext = FileHandler.get_file_extension(file_path)
        return ext
        
    @staticmethod
    def get_available_output_formats(input_format):
        """获取指定输入格式支持的输出格式
        
        此方法需要导入FORMAT_CONVERSION_MAP，
        但为避免循环导入，由调用者提供转换逻辑
        """
        # 实际实现在converter.py
        return {}

    async def validate_file_exists(self, file_path: str) -> Tuple[bool, bool]:
        """验证文件是否存在
        
        Args:
            file_path: 文件路径
            
        Returns:
            tuple: (文件是否存在, 是否为URL)
        """
        is_url = self.is_url(file_path)
        if not is_url and not os.path.exists(file_path):
            await self.logger.error(f"文件不存在：{file_path}", FileNotFoundError)
            return False, is_url
        return True, is_url

    @staticmethod
    def is_dir_writable(dir_path: str) -> bool:
        """检查目录是否存在且可写"""
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path, exist_ok=True)
                return True
            except Exception:
                return False
        return os.access(dir_path, os.W_OK)

    async def get_output_dir(self, file_path: str) -> str:
        """确定输出目录
        
        Args:
            file_path: 输入文件路径
            
        Returns:
            str: 可写的输出目录路径
            
        Raises:
            RuntimeError: 如果找不到可写的输出目录
        """
        output_dir_candidates = []
        
        # 1. 对于本地文件，使用输入文件所在目录
        if not self.is_url(file_path):
            input_file_dir = os.path.dirname(file_path)
            if input_file_dir:  # 确保不是空字符串
                output_dir_candidates.append(input_file_dir)
        
        # 2. 当前工作目录
        output_dir_candidates.append(os.getcwd())
        
        # 3. 系统临时目录
        output_dir_candidates.append(tempfile.gettempdir())
        
        # 尝试找到第一个可写的目录
        for dir_candidate in output_dir_candidates:
            if self.is_dir_writable(dir_candidate):
                return dir_candidate
        
        await self.logger.error("无法找到可写的输出目录")

    def get_unique_output_path(self, file_path: str, format: str, output_dir: str) -> str:
        """生成唯一的输出文件路径
        
        Args:
            file_path: 输入文件路径
            format: 目标格式
            output_dir: 输出目录
            
        Returns:
            str: 唯一的输出文件路径
        """
        if self.is_url(file_path):
            # 从URL中提取文件名
            url_path = urllib.parse.urlparse(file_path).path
            file_name = os.path.splitext(os.path.basename(url_path))[0]
            
            # 如果文件名为空（URL没有明确的文件名），使用一个默认名称
            if not file_name:
                file_name = f"pdf_converted_{int(time.time())}"
        else:
            file_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # 生成输出文件路径
        output_name = f"{file_name}.{format}"
        output_path = os.path.join(output_dir, output_name)
        
        # 确保输出文件名在目标目录中是唯一的
        counter = 1
        while os.path.exists(output_path):
            base_name = f"{file_name}_{counter}"
            output_name = f"{base_name}.{format}"
            output_path = os.path.join(output_dir, output_name)
            counter += 1
        
        return output_path

class BaseApiClient:
    """API客户端基类"""
    def __init__(self, logger: Logger, file_handler: FileHandler):
        self.logger = logger
        self.file_handler = file_handler
        self.api_key = os.getenv("API_KEY")
        # 子类必须设置api_base_url
        self.api_base_url = None

    async def _wait_for_task(self, client: httpx.AsyncClient, task_id: str, operation_type: str = "处理") -> str:
        """等待任务完成并返回下载链接
        
        Args:
            client: HTTP客户端
            task_id: 任务ID
            operation_type: 操作类型描述，用于日志，默认为"处理"
            
        Returns:
            str: 下载链接
            
        Raises:
            RuntimeError: 如果任务失败或超时
        """
        headers = {"X-API-KEY": self.api_key}
        MAX_ATTEMPTS = 100
        
        for attempt in range(MAX_ATTEMPTS):
            await asyncio.sleep(3)
            
            status_response = await client.get(
                f"{self.api_base_url}/{task_id}",
                headers=headers
            )
            
            if status_response.status_code != 200:
                await self.logger.log("warning", f"获取任务状态失败。状态码: {status_response.status_code}")
                continue
            
            status_result = status_response.json()
            state = status_result.get("data", {}).get("state")
            progress = status_result.get("data", {}).get("progress", 0)
            
            if state == 1:  # 完成
                download_url = status_result.get("data", {}).get("file")
                if not download_url:
                    await self.logger.error(f"任务完成但未找到下载链接。任务状态：{json.dumps(status_result, ensure_ascii=False)}")
                return download_url
            elif state < 0:  # 失败
                await self.logger.error(f"任务失败: {json.dumps(status_result, ensure_ascii=False)}")
            else:  # 进行中
                await self.logger.log("debug", f"{operation_type}进度: {progress}%", add_to_result=False)
        
        await self.logger.error(f"超过最大尝试次数（{MAX_ATTEMPTS}），任务未完成")

    async def _handle_api_response(self, response: httpx.Response, error_prefix: str) -> str:
        """处理API响应并提取任务ID
        
        Args:
            response: API响应
            error_prefix: 错误消息前缀
            
        Returns:
            str: 任务ID
            
        Raises:
            RuntimeError: 如果响应无效或任务ID缺失
        """
        if response.status_code != 200:
            await self.logger.error(f"{error_prefix}失败。状态码: {response.status_code}\n响应: {response.text}")
        
        result = response.json()
        if "data" not in result or "task_id" not in result["data"]:
            await self.logger.error(f"无法获取任务ID。API响应：{json.dumps(result, ensure_ascii=False)}")
        
        return result["data"]["task_id"] 