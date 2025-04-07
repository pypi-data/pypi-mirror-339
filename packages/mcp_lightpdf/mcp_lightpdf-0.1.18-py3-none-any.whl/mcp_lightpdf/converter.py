"""PDF文档转换模块"""
import asyncio
import json
import os
import tempfile
import time
import urllib.parse
import uuid
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Set

import httpx
from mcp.types import TextContent, LoggingMessageNotification, LoggingMessageNotificationParams, LoggingLevel

class InputFormat(str, Enum):
    """支持的输入文件格式"""
    PDF = "pdf"
    WORD = "docx"
    EXCEL = "xlsx"
    PPT = "pptx"
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"
    BMP = "bmp"
    GIF = "gif"
    CAD = "dwg"
    CAJ = "caj"
    OFD = "ofd"

class OutputFormat(str, Enum):
    """支持的输出文件格式"""
    PDF = "pdf"
    WORD = "docx"
    EXCEL = "xlsx"
    PPT = "pptx"
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"
    BMP = "bmp"
    GIF = "gif"
    HTML = "html"
    TEXT = "txt"

# 文件扩展名到输入格式的映射
INPUT_EXTENSIONS = {
    ".pdf": InputFormat.PDF,
    ".docx": InputFormat.WORD,
    ".xlsx": InputFormat.EXCEL,
    ".pptx": InputFormat.PPT,
    ".jpg": InputFormat.JPG,
    ".jpeg": InputFormat.JPEG,
    ".png": InputFormat.PNG,
    ".bmp": InputFormat.BMP,
    ".gif": InputFormat.GIF,
    ".dwg": InputFormat.CAD,
    ".caj": InputFormat.CAJ,
    ".ofd": InputFormat.OFD,
}

# 输入格式到可用输出格式的映射
FORMAT_CONVERSION_MAP = {
    InputFormat.PDF: {
        OutputFormat.WORD,   # PDF转Word
        OutputFormat.EXCEL,  # PDF转Excel
        OutputFormat.PPT,    # PDF转PPT
        OutputFormat.JPG,    # PDF转JPG
        OutputFormat.JPEG,   # PDF转JPEG
        OutputFormat.PNG,    # PDF转PNG
        OutputFormat.BMP,    # PDF转BMP
        OutputFormat.GIF,    # PDF转GIF
        OutputFormat.HTML,   # PDF转HTML
        OutputFormat.TEXT,   # PDF转文本
    },
    InputFormat.WORD: {OutputFormat.PDF},    # Word转PDF
    InputFormat.EXCEL: {OutputFormat.PDF},   # Excel转PDF
    InputFormat.PPT: {OutputFormat.PDF},     # PPT转PDF
    InputFormat.JPG: {OutputFormat.PDF},     # JPG转PDF
    InputFormat.JPEG: {OutputFormat.PDF},    # JPEG转PDF
    InputFormat.PNG: {OutputFormat.PDF},     # PNG转PDF
    InputFormat.BMP: {OutputFormat.PDF},     # BMP转PDF
    InputFormat.GIF: {OutputFormat.PDF},     # GIF转PDF
    InputFormat.CAD: {OutputFormat.PDF},     # CAD转PDF
    InputFormat.CAJ: {OutputFormat.PDF},     # CAJ转PDF
    InputFormat.OFD: {OutputFormat.PDF},     # OFD转PDF
}

@dataclass
class ConversionResult:
    """转换结果数据类"""
    success: bool
    file_path: str
    output_path: Optional[str] = None
    error_message: Optional[str] = None
    file_size: Optional[float] = None
    download_url: Optional[str] = None  # API返回的下载地址

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
    def get_input_format(file_path: str) -> Optional[InputFormat]:
        """根据文件路径获取输入格式"""
        ext = FileHandler.get_file_extension(file_path)
        return INPUT_EXTENSIONS.get(ext)

    @staticmethod
    def get_available_output_formats(input_format: InputFormat) -> Set[OutputFormat]:
        """获取指定输入格式支持的输出格式"""
        return FORMAT_CONVERSION_MAP.get(input_format, set())

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

class Converter:
    """PDF文档转换器"""
    def __init__(self, logger: Logger, file_handler: FileHandler):
        self.logger = logger
        self.file_handler = file_handler
        self.api_key = os.getenv("API_KEY")
        self.api_base_url = os.getenv("API_BASE_URL", "https://techsz.aoscdn.com/api/tasks/document/conversion")

    async def convert_file(self, file_path: str, format: str, extra_params: dict = None) -> ConversionResult:
        """转换单个文件
        
        Args:
            file_path: 要转换的文件路径
            format: 目标格式
            extra_params: 额外的API参数，例如去除水印
            
        Returns:
            ConversionResult: 转换结果
        """
        if not self.api_key:
            await self.logger.error("未找到API_KEY。请在客户端配置API_KEY环境变量。")

        # 特殊格式：doc-repair用于去除水印，输出为PDF
        is_watermark_removal = format == "doc-repair"
        actual_output_format = "pdf" if is_watermark_removal else format

        # 验证输入文件格式
        input_format = self.file_handler.get_input_format(file_path)
        if not input_format and not is_watermark_removal:
            await self.logger.error(f"不支持的输入文件格式: {self.file_handler.get_file_extension(file_path)}")

        # 如果是去除水印操作，检查是否PDF文件
        if is_watermark_removal and input_format != InputFormat.PDF:
            await self.logger.error("去除水印功能仅支持PDF文件")

        # 验证输出格式（除去水印操作外）
        if not is_watermark_removal:
            try:
                output_format = OutputFormat(format)
            except ValueError:
                await self.logger.error(f"不支持的输出格式: {format}")

            # 验证格式转换是否支持
            if input_format:  # 确保input_format有效
                available_formats = self.file_handler.get_available_output_formats(input_format)
                if output_format not in available_formats:
                    await self.logger.error(
                        f"不支持从 {input_format.value} 格式转换为 {output_format.value} 格式。"
                        f"支持的输出格式: {', '.join(f.value for f in available_formats)}"
                    )
        else:
            # 对于去水印操作，设置输出格式为PDF
            output_format = OutputFormat.PDF

        # 验证文件
        is_url = self.file_handler.is_url(file_path)
        if not is_url and not os.path.exists(file_path):
            await self.logger.error(f"文件不存在：{file_path}", FileNotFoundError)

        # 获取输出目录
        output_dir = await self.file_handler.get_output_dir(file_path)
        # 无论传入什么format，对于去水印操作，确保输出文件后缀为.pdf
        output_path = self.file_handler.get_unique_output_path(file_path, actual_output_format, output_dir)

        # 操作描述
        if is_watermark_removal:
            operation_desc = "去除水印"
        else:
            operation_desc = f"将 {input_format.value.upper()} 转换为 {output_format.value.upper()} 格式"
        await self.logger.log("info", f"正在{operation_desc}...")

        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                # 创建转换任务
                task_id = await self._create_task(client, file_path, format, is_url, extra_params)
                
                # 等待任务完成
                download_url = await self._wait_for_task(client, task_id)
                
                # 下载结果
                await self._download_result(client, download_url, output_path)
                
                # 获取文件大小
                file_size = os.path.getsize(output_path)
                
                return ConversionResult(
                    success=True,
                    file_path=file_path,
                    output_path=output_path,
                    file_size=file_size,
                    download_url=download_url
                )

            except Exception as e:
                return ConversionResult(
                    success=False,
                    file_path=file_path,
                    error_message=str(e)
                )

    async def _create_task(self, client: httpx.AsyncClient, file_path: str, format: str, is_url: bool, extra_params: dict = None) -> str:
        """创建转换任务
        
        Args:
            client: HTTP客户端
            file_path: 文件路径
            format: 目标格式，特殊格式"doc-repair"用于去除水印
            is_url: 是否URL路径
            extra_params: 额外API参数(可选)，用于传递API所需的其他参数
        
        Returns:
            str: 任务ID
        """
        await self.logger.log("info", "正在提交转换任务...")
        
        headers = {"X-API-KEY": self.api_key}
        data = {"format": format}
        
        # 添加额外参数
        if extra_params:
            data.update(extra_params)
        
        if is_url:
            data["url"] = file_path
            response = await client.post(
                self.api_base_url,
                data=data,
                headers=headers
            )
        else:
            with open(file_path, "rb") as f:
                files = {"file": f}
                response = await client.post(
                    self.api_base_url,
                    files=files,
                    data=data,
                    headers=headers
                )
        
        if response.status_code != 200:
            await self.logger.error(f"创建任务失败。状态码: {response.status_code}\n响应: {response.text}")
        
        result = response.json()
        if "data" not in result or "task_id" not in result["data"]:
            await self.logger.error(f"无法获取任务ID。API响应：{json.dumps(result, ensure_ascii=False)}")
        
        return result["data"]["task_id"]

    async def _wait_for_task(self, client: httpx.AsyncClient, task_id: str) -> str:
        """等待任务完成并返回下载链接"""
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
            state_detail = status_result.get("data", {}).get("state_detail", "Unknown")
            progress = status_result.get("data", {}).get("progress", 0)
            
            if state == 1:  # 完成
                download_url = status_result.get("data", {}).get("file")
                if not download_url:
                    await self.logger.error(f"任务完成但未找到下载链接。任务状态：{json.dumps(status_result, ensure_ascii=False)}")
                return download_url
            elif state < 0:  # 失败
                await self.logger.error(f"任务失败: {json.dumps(status_result, ensure_ascii=False)}")
            else:  # 进行中
                await self.logger.log("debug", f"转换进度: {progress}%", add_to_result=False)
        
        await self.logger.error(f"超过最大尝试次数（{MAX_ATTEMPTS}），任务未完成")

    async def _download_result(self, client: httpx.AsyncClient, download_url: str, output_path: str):
        """下载转换结果"""
        await self.logger.log("info", "正在下载转换后的文件...")
        download_response = await client.get(download_url)
        
        if download_response.status_code != 200:
            await self.logger.error(f"下载失败。状态码: {download_response.status_code}")
        
        with open(output_path, "wb") as f:
            f.write(download_response.content)
        
        await self.logger.log("info", "转换完成") 