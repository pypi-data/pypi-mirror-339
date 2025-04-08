"""PDF文档编辑模块"""
import asyncio
import json
import os
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict, Any, Union

import httpx

from mcp_lightpdf.converter import Logger, FileHandler, ConversionResult, InputFormat

class EditType(str, Enum):
    """支持的PDF编辑操作类型"""
    SPLIT = "split"          # 拆分PDF
    MERGE = "merge"          # 合并PDF
    ROTATE = "rotate"        # 旋转PDF
    COMPRESS = "compress"    # 压缩PDF
    ENCRYPT = "protect"      # 加密PDF
    DECRYPT = "unlock"       # 解密PDF
    ADD_SIGNATURE = "sign"   # 添加签名
    ADD_WATERMARK = "watermark"  # 添加水印

@dataclass
class EditResult:
    """编辑结果数据类"""
    success: bool
    file_path: str
    error_message: Optional[str] = None
    download_url: Optional[str] = None  # API返回的下载地址

class Editor:
    """PDF文档编辑器"""
    def __init__(self, logger: Logger, file_handler: FileHandler):
        self.logger = logger
        self.file_handler = file_handler
        self.api_key = os.getenv("API_KEY")
        self.api_base_url = os.getenv("API_BASE_URL", "https://techsz.aoscdn.com/api/tasks/document/pdfedit")

    async def split_pdf(self, file_path: str, pages: str, password: Optional[str] = None) -> EditResult:
        """拆分PDF文件
        
        Args:
            file_path: 要拆分的PDF文件路径
            pages: 拆分页面规则，例如 "1,3,5-7" 表示提取第1,3,5,6,7页
            password: 文档密码，如果文档受密码保护，则需要提供（可选）
            
        Returns:
            EditResult: 拆分结果
        """
        # 验证输入文件是否为PDF
        input_format = self.file_handler.get_input_format(file_path)
        if input_format != InputFormat.PDF:
            await self.logger.error(f"PDF拆分功能仅支持PDF文件，当前文件格式为: {self.file_handler.get_file_extension(file_path)}")
        
        # 构建API参数
        extra_params = {
            "pages": pages
        }
        
        # 记录操作描述
        await self.logger.log("info", f"正在拆分PDF文件（页面: {pages}）...")
        
        # 调用edit_pdf方法处理API请求
        return await self.edit_pdf(file_path, EditType.SPLIT, extra_params, password)

    async def merge_pdfs(self, file_paths: List[str], password: Optional[str] = None) -> EditResult:
        """合并多个PDF文件
        
        Args:
            file_paths: 要合并的PDF文件路径列表
            password: 文档密码，如果文档受密码保护，则需要提供（可选）
            
        Returns:
            EditResult: 合并结果
        """
        if len(file_paths) < 2:
            await self.logger.error("合并PDF至少需要两个文件")
        
        # 验证所有文件是否都是PDF
        for pdf_file in file_paths:
            input_format = self.file_handler.get_input_format(pdf_file)
            if input_format != InputFormat.PDF:
                await self.logger.error(f"合并功能仅支持PDF文件，文件 {pdf_file} 格式为: {self.file_handler.get_file_extension(pdf_file)}")
            
            # 验证文件是否存在
            is_url = self.file_handler.is_url(pdf_file)
            if not is_url and not os.path.exists(pdf_file):
                await self.logger.error(f"文件不存在：{pdf_file}", FileNotFoundError)
        
        # 记录操作描述
        await self.logger.log("info", f"正在合并 {len(file_paths)} 个PDF文件...")
        
        # 合并PDF需要特殊处理，因为涉及多个文件
        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                # 创建合并任务
                task_id = await self._create_merge_task(client, file_paths, password)
                
                # 等待任务完成
                download_url = await self._wait_for_task(client, task_id)
                
                # 记录完成信息
                await self.logger.log("info", "PDF合并完成。可通过下载链接获取结果文件。")
                
                return EditResult(
                    success=True,
                    file_path=file_paths[0],  # 使用第一个文件路径作为参考
                    error_message=None,
                    download_url=download_url
                )

            except Exception as e:
                return EditResult(
                    success=False,
                    file_path=file_paths[0],
                    error_message=str(e),
                    download_url=None
                )

    async def rotate_pdf(self, file_path: str, angle: int, pages: str = "all", password: Optional[str] = None) -> EditResult:
        """旋转PDF文件的页面
        
        Args:
            file_path: 要旋转的PDF文件路径
            angle: 旋转角度，可选值: 90, 180, 270 (顺时针)
            pages: 要旋转的页面，例如 "1,3,5-7" 或 "all" 表示所有页面
            password: 文档密码，如果文档受密码保护，则需要提供（可选）
            
        Returns:
            EditResult: 旋转结果
        """
        # 验证输入文件是否为PDF
        input_format = self.file_handler.get_input_format(file_path)
        if input_format != InputFormat.PDF:
            await self.logger.error(f"PDF旋转功能仅支持PDF文件，当前文件格式为: {self.file_handler.get_file_extension(file_path)}")
        
        # 验证旋转角度
        valid_angles = {90, 180, 270}
        if angle not in valid_angles:
            await self.logger.error(f"无效的旋转角度: {angle}。有效值为: 90, 180, 270")
        
        # 构建API参数
        extra_params = {
            "angle": angle,
            "pages": pages
        }
        
        # 记录操作描述
        await self.logger.log("info", f"正在旋转PDF文件（角度: {angle}°, 页面: {pages}）...")
        
        # 调用edit_pdf方法处理API请求
        return await self.edit_pdf(file_path, EditType.ROTATE, extra_params, password)

    async def compress_pdf(self, file_path: str, quality: str = "medium", password: Optional[str] = None) -> EditResult:
        """压缩PDF文件
        
        Args:
            file_path: 要压缩的PDF文件路径
            quality: 压缩质量，可选值: "low", "medium", "high"，默认为"medium"
            password: 文档密码，如果文档受密码保护，则需要提供（可选）
            
        Returns:
            EditResult: 压缩结果
        """
        # 验证输入文件是否为PDF
        input_format = self.file_handler.get_input_format(file_path)
        if input_format != InputFormat.PDF:
            await self.logger.error(f"PDF压缩功能仅支持PDF文件，当前文件格式为: {self.file_handler.get_file_extension(file_path)}")
        
        # 验证压缩质量
        valid_qualities = {"low", "medium", "high"}
        if quality not in valid_qualities:
            await self.logger.error(f"无效的压缩质量: {quality}。有效值为: low, medium, high")
        
        # 构建API参数
        extra_params = {
            "quality": quality
        }
        
        # 记录操作描述
        await self.logger.log("info", f"正在压缩PDF文件（质量: {quality}）...")
        
        # 调用edit_pdf方法处理API请求
        return await self.edit_pdf(file_path, EditType.COMPRESS, extra_params, password)

    async def encrypt_pdf(self, file_path: str, new_password: str, owner_password: Optional[str] = None, password: Optional[str] = None) -> EditResult:
        """加密PDF文件
        
        Args:
            file_path: 要加密的PDF文件路径
            new_password: 设置的新用户密码
            owner_password: 设置的新所有者密码（可选）
            password: 文档原密码，如果文档已受密码保护，则需要提供（可选）
            
        Returns:
            EditResult: 加密结果
        """
        # 验证输入文件是否为PDF
        input_format = self.file_handler.get_input_format(file_path)
        if input_format != InputFormat.PDF:
            await self.logger.error(f"PDF加密功能仅支持PDF文件，当前文件格式为: {self.file_handler.get_file_extension(file_path)}")
        
        # 构建API参数
        extra_params = {
            "new_password": new_password
        }
        
        # 如果提供了所有者密码，则添加到参数中
        if owner_password:
            extra_params["owner_password"] = owner_password
        
        # 记录操作描述
        await self.logger.log("info", "正在加密PDF文件...")
        
        # 调用edit_pdf方法处理API请求
        return await self.edit_pdf(file_path, EditType.ENCRYPT, extra_params, password)

    async def decrypt_pdf(self, file_path: str, password: Optional[str] = None) -> EditResult:
        """解密PDF文件
        
        Args:
            file_path: 要解密的PDF文件路径
            password: 文档密码（可选），如果文档受密码保护，则需要提供
            
        Returns:
            EditResult: 解密结果
        """
        # 验证输入文件是否为PDF
        input_format = self.file_handler.get_input_format(file_path)
        if input_format != InputFormat.PDF:
            await self.logger.error(f"PDF解密功能仅支持PDF文件，当前文件格式为: {self.file_handler.get_file_extension(file_path)}")
        
        # 记录操作描述
        await self.logger.log("info", "正在解密PDF文件...")
        
        # 调用edit_pdf方法处理API请求
        return await self.edit_pdf(file_path, EditType.DECRYPT, {}, password)

    async def add_signature(self, file_path: str, signature_image_path: str, page: int = 1, position: Dict[str, float] = None, password: Optional[str] = None) -> EditResult:
        """为PDF文件添加签名
        
        Args:
            file_path: 要添加签名的PDF文件路径
            signature_image_path: 签名图片路径
            page: 添加签名的页码，默认为第1页
            position: 签名位置，包含"x", "y", "width", "height"键的字典，默认为None（自动定位）
            password: 文档密码，如果文档受密码保护，则需要提供（可选）
            
        Returns:
            EditResult: 添加签名结果
        """
        # 验证输入文件是否为PDF
        input_format = self.file_handler.get_input_format(file_path)
        if input_format != InputFormat.PDF:
            await self.logger.error(f"添加签名功能仅支持PDF文件，当前文件格式为: {self.file_handler.get_file_extension(file_path)}")
        
        # 验证签名图片存在
        is_url = self.file_handler.is_url(signature_image_path)
        if not is_url and not os.path.exists(signature_image_path):
            await self.logger.error(f"签名图片不存在：{signature_image_path}", FileNotFoundError)
        
        # 构建API参数
        extra_params = {
            "page": page
        }
        
        # 如果提供了位置信息，添加到参数中
        if position:
            extra_params["position"] = position
        
        # 记录操作描述
        await self.logger.log("info", f"正在为PDF添加签名（页码: {page}）...")
        
        # 签名需要特殊处理，因为需要上传两个文件
        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                # 创建签名任务
                task_id = await self._create_signature_task(client, file_path, signature_image_path, extra_params, password)
                
                # 等待任务完成
                download_url = await self._wait_for_task(client, task_id)
                
                # 记录完成信息
                await self.logger.log("info", "添加签名完成。可通过下载链接获取结果文件。")
                
                return EditResult(
                    success=True,
                    file_path=file_path,
                    error_message=None,
                    download_url=download_url
                )

            except Exception as e:
                return EditResult(
                    success=False,
                    file_path=file_path,
                    error_message=str(e),
                    download_url=None
                )

    async def add_watermark(self, file_path: str, text: str, opacity: float = 0.5, angle: int = 45, pages: str = "all", password: Optional[str] = None) -> EditResult:
        """为PDF文件添加水印
        
        Args:
            file_path: 要添加水印的PDF文件路径
            text: 水印文本内容
            opacity: 水印透明度，0.0-1.0，默认为0.5
            angle: 水印角度，默认为45度
            pages: 要添加水印的页面，例如 "1,3,5-7" 或 "all" 表示所有页面
            password: 文档密码，如果文档受密码保护，则需要提供（可选）
            
        Returns:
            EditResult: 添加水印结果
        """
        # 验证输入文件是否为PDF
        input_format = self.file_handler.get_input_format(file_path)
        if input_format != InputFormat.PDF:
            await self.logger.error(f"添加水印功能仅支持PDF文件，当前文件格式为: {self.file_handler.get_file_extension(file_path)}")
        
        # 验证透明度
        if not 0.0 <= opacity <= 1.0:
            await self.logger.error(f"无效的透明度: {opacity}。有效值范围为: 0.0-1.0")
        
        # 构建API参数
        extra_params = {
            "text": text,
            "opacity": opacity,
            "angle": angle,
            "pages": pages
        }
        
        # 记录操作描述
        await self.logger.log("info", f"正在为PDF添加水印（文本: {text}, 透明度: {opacity}, 角度: {angle}°, 页面: {pages}）...")
        
        # 调用edit_pdf方法处理API请求
        return await self.edit_pdf(file_path, EditType.ADD_WATERMARK, extra_params, password)

    async def edit_pdf(self, file_path: str, edit_type: EditType, extra_params: Dict[str, Any] = None, password: Optional[str] = None) -> EditResult:
        """编辑PDF文件
        
        Args:
            file_path: 要编辑的PDF文件路径
            edit_type: 编辑操作类型
            extra_params: 额外的API参数
            password: 文档密码，如果文档受密码保护，则需要提供（可选）
            
        Returns:
            EditResult: 编辑结果
        """
        if not self.api_key:
            await self.logger.error("未找到API_KEY。请在客户端配置API_KEY环境变量。")

        # 验证输入文件格式
        input_format = self.file_handler.get_input_format(file_path)
        if input_format != InputFormat.PDF:
            await self.logger.error(f"PDF编辑功能仅支持PDF文件，当前文件格式为: {self.file_handler.get_file_extension(file_path)}")

        # 验证文件
        is_url = self.file_handler.is_url(file_path)
        if not is_url and not os.path.exists(file_path):
            await self.logger.error(f"文件不存在：{file_path}", FileNotFoundError)

        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                # 初始化extra_params（如果为None）
                if extra_params is None:
                    extra_params = {}
                
                # 如果提供了密码，将其添加到extra_params
                if password:
                    extra_params["password"] = password
                
                # 创建编辑任务
                task_id = await self._create_task(client, file_path, edit_type, is_url, extra_params)
                
                # 等待任务完成
                download_url = await self._wait_for_task(client, task_id)
                
                # 记录完成信息
                await self.logger.log("info", "编辑完成。可通过下载链接获取结果文件。")
                
                return EditResult(
                    success=True,
                    file_path=file_path,
                    error_message=None,
                    download_url=download_url
                )

            except Exception as e:
                return EditResult(
                    success=False,
                    file_path=file_path,
                    error_message=str(e),
                    download_url=None
                )

    async def _create_task(self, client: httpx.AsyncClient, file_path: str, edit_type: EditType, is_url: bool, extra_params: Dict[str, Any] = None) -> str:
        """创建编辑任务
        
        Args:
            client: HTTP客户端
            file_path: 文件路径
            edit_type: 编辑操作类型
            is_url: 是否URL路径
            extra_params: 额外API参数(可选)
        
        Returns:
            str: 任务ID
        """
        await self.logger.log("info", "正在提交PDF编辑任务...")
        
        headers = {"X-API-KEY": self.api_key}
        data = {"type": edit_type.value}
        
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

    async def _create_merge_task(self, client: httpx.AsyncClient, file_paths: List[str], password: Optional[str] = None) -> str:
        """创建PDF合并任务
        
        Args:
            client: HTTP客户端
            file_paths: 要合并的PDF文件路径列表
            password: 文档密码，如果文档受密码保护，则需要提供（可选）
        
        Returns:
            str: 任务ID
        """
        await self.logger.log("info", "正在提交PDF合并任务...")
        
        headers = {"X-API-KEY": self.api_key}
        data = {"type": EditType.MERGE.value}
        
        # 如果提供了密码，添加到数据中
        if password:
            data["password"] = password
        
        # 准备文件
        files = {}
        for i, file_path in enumerate(file_paths):
            if self.file_handler.is_url(file_path):
                # 对于URL，添加到data中
                data[f"url{i+1}"] = file_path
            else:
                # 对于本地文件，添加到files中
                files[f"file{i+1}"] = open(file_path, "rb")
        
        try:
            # 发送请求
            response = await client.post(
                self.api_base_url,
                data=data,
                files=files,
                headers=headers
            )
            
            if response.status_code != 200:
                await self.logger.error(f"创建合并任务失败。状态码: {response.status_code}\n响应: {response.text}")
            
            result = response.json()
            if "data" not in result or "task_id" not in result["data"]:
                await self.logger.error(f"无法获取任务ID。API响应：{json.dumps(result, ensure_ascii=False)}")
            
            return result["data"]["task_id"]
            
        finally:
            # 确保所有打开的文件都被关闭
            for file_obj in files.values():
                file_obj.close()

    async def _create_signature_task(self, client: httpx.AsyncClient, file_path: str, signature_image_path: str, extra_params: Dict[str, Any], password: Optional[str] = None) -> str:
        """创建添加签名任务
        
        Args:
            client: HTTP客户端
            file_path: PDF文件路径
            signature_image_path: 签名图片路径
            extra_params: 额外参数
            password: 文档密码，如果文档受密码保护，则需要提供（可选）
        
        Returns:
            str: 任务ID
        """
        await self.logger.log("info", "正在提交添加签名任务...")
        
        headers = {"X-API-KEY": self.api_key}
        data = {"type": EditType.ADD_SIGNATURE.value}
        
        # 添加额外参数
        if extra_params:
            data.update(extra_params)
        
        # 如果提供了密码，添加到数据中
        if password:
            data["password"] = password
        
        files = {}
        
        # 处理PDF文件
        pdf_is_url = self.file_handler.is_url(file_path)
        if pdf_is_url:
            data["url"] = file_path
        else:
            files["file"] = open(file_path, "rb")
        
        # 处理签名图片
        sig_is_url = self.file_handler.is_url(signature_image_path)
        if sig_is_url:
            data["signature_url"] = signature_image_path
        else:
            files["signature"] = open(signature_image_path, "rb")
        
        try:
            # 发送请求
            response = await client.post(
                self.api_base_url,
                data=data,
                files=files,
                headers=headers
            )
            
            if response.status_code != 200:
                await self.logger.error(f"创建签名任务失败。状态码: {response.status_code}\n响应: {response.text}")
            
            result = response.json()
            if "data" not in result or "task_id" not in result["data"]:
                await self.logger.error(f"无法获取任务ID。API响应：{json.dumps(result, ensure_ascii=False)}")
            
            return result["data"]["task_id"]
            
        finally:
            # 确保所有打开的文件都被关闭
            for file_obj in files.values():
                file_obj.close()

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
            progress = status_result.get("data", {}).get("progress", 0)
            
            if state == 1:  # 完成
                download_url = status_result.get("data", {}).get("file")
                if not download_url:
                    await self.logger.error(f"任务完成但未找到下载链接。任务状态：{json.dumps(status_result, ensure_ascii=False)}")
                return download_url
            elif state < 0:  # 失败
                await self.logger.error(f"任务失败: {json.dumps(status_result, ensure_ascii=False)}")
            else:  # 进行中
                await self.logger.log("debug", f"处理进度: {progress}%", add_to_result=False)
        
        await self.logger.error(f"超过最大尝试次数（{MAX_ATTEMPTS}），任务未完成") 