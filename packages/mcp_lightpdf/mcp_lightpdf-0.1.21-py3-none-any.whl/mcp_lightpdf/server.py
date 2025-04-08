# 标准库导入
import asyncio
import os
from typing import List

# 第三方库导入
from dotenv import load_dotenv

# MCP相关导入
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.types as types

# 本地导入
from .converter import Converter, ConversionResult, Logger, FileHandler
from .editor import Editor, EditResult

# 加载环境变量
load_dotenv()

def generate_report(results: List[ConversionResult], is_watermark_removal: bool = False, is_page_numbering: bool = False) -> str:
    """生成转换报告
    
    Args:
        results: 转换结果列表
        is_watermark_removal: 是否为水印去除任务
        is_page_numbering: 是否为添加页码任务
        
    Returns:
        str: 格式化的报告文本
    """
    # 统计结果
    success_count = sum(1 for r in results if r.success)
    failed_count = len(results) - success_count
    
    # 生成报告头部，根据任务类型显示不同文案
    if is_watermark_removal:
        task_type = "水印去除"
    elif is_page_numbering:
        task_type = "添加页码"
    else:
        task_type = "转换"
        
    report_lines = [
        f"{task_type}结果：共 {len(results)} 个文件" + (
            f"，成功 {success_count} 个" if success_count > 0 else ""
        ) + (
            f"，失败 {failed_count} 个" if failed_count > 0 else ""
        ),
        ""
    ]
    
    # 添加成功的文件信息
    if success_count > 0:
        if is_watermark_removal:
            success_action = "去除水印成功"
        elif is_page_numbering:
            success_action = "添加页码成功"
        else:
            success_action = "转换成功"
            
        report_lines.extend([f"[成功] {success_action}的文件：", ""])
        for i, result in enumerate(results):
            if result.success:
                report_lines.extend([
                    f"[{i+1}] {result.file_path}",
                    f"- 在线下载地址: {result.download_url}",
                    ""
                ])
    
    # 添加失败的文件信息
    if failed_count > 0:
        if is_watermark_removal:
            failed_action = "水印去除失败"
        elif is_page_numbering:
            failed_action = "添加页码失败"
        else:
            failed_action = "转换失败"
            
        report_lines.extend([f"[失败] {failed_action}的文件：", ""])
        for i, result in enumerate(results):
            if not result.success:
                report_lines.extend([
                    f"[{i+1}] {result.file_path}",
                    f"- 错误: {result.error_message}",
                    ""
                ])
    
    return "\n".join(report_lines)

async def process_files(file_paths: List[str], format: str, logger: Logger, converter: Converter, extra_params: dict = None, password: str = None) -> List[ConversionResult]:
    """处理文件转换
    
    Args:
        file_paths: 要转换的文件路径列表
        format: 目标格式
        logger: 日志记录器
        converter: 转换器实例
        extra_params: 额外参数，用于页码添加等操作
        password: 文档密码，如果文档受密码保护，则需要提供此参数
        
    Returns:
        List[ConversionResult]: 转换结果列表
    """
    is_watermark_removal = format == "doc-repair"
    is_page_numbering = format == "number-pdf"
    
    # 操作描述文本
    if is_watermark_removal:
        operation_type = "去除水印"
    elif is_page_numbering:
        operation_type = "添加页码"
    else:
        operation_type = f"转换为 {format} 格式"
    
    # 定义处理单个文件的函数
    async def process_single_file(file_path: str):
        if is_page_numbering and extra_params:
            # 对于添加页码，使用add_page_numbers方法
            return await converter.add_page_numbers(
                file_path, 
                extra_params.get("start_num", 1),
                extra_params.get("position", "5"),
                extra_params.get("margin", 30),
                password
            )
        else:
            # 对于其他操作，使用convert_file方法
            return await converter.convert_file(file_path, format, extra_params, password)
    
    if len(file_paths) > 1:
        await logger.log("info", f"开始批量{operation_type}，共 {len(file_paths)} 个文件")
        
        # 并发处理文件，限制并发数为5
        semaphore = asyncio.Semaphore(5)
        
        async def process_with_semaphore(file_path: str):
            async with semaphore:
                return await process_single_file(file_path)
        
        # 创建任务列表
        tasks = [process_with_semaphore(file_path) for file_path in file_paths]
        return await asyncio.gather(*tasks)
    else:
        # 单文件处理
        return [await process_single_file(file_paths[0])]

async def _process_tool_call(logger: Logger, file_paths: List[str], format: str, 
                     is_watermark_removal: bool = False, is_page_numbering: bool = False,
                     extra_params: dict = None, password: str = None) -> types.TextContent:
    """处理工具调用的通用逻辑
    
    Args:
        logger: 日志记录器
        file_paths: 文件路径列表
        format: 转换格式
        is_watermark_removal: 是否水印去除任务
        is_page_numbering: 是否添加页码任务
        extra_params: 额外参数
        password: 文档密码，如果文档受密码保护，则需要提供此参数
        
    Returns:
        types.TextContent: 包含处理结果的文本内容
    """
    # 创建必要的对象
    file_handler = FileHandler(logger)
    converter = Converter(logger, file_handler)
    
    # 处理文件
    results = await process_files(file_paths, format, logger, converter, extra_params, password)
    
    # 生成报告
    report_msg = generate_report(results, is_watermark_removal, is_page_numbering)
    
    # 如果全部失败，记录错误
    if not any(r.success for r in results):
        await logger.error(report_msg)
    
    return types.TextContent(
        type="text",
        text=report_msg
    )

# 创建Server实例
app = Server(
    name="LightPDF_AI_tools",
    instructions="轻闪文档处理工具。",
)

# 定义工具
@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="convert_document",
            description="文档格式转换工具。\n\nPDF可转换为：DOCX/XLSX/PPTX/图片/HTML/TXT；\n其他格式可转换为PDF：DOCX/XLSX/PPTX/图片/CAD/CAJ/OFD",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_paths": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "文件路径或URL的列表"
                    },
                    "password": {
                        "type": "string",
                        "description": "文档密码，如果文档受密码保护，则需要提供此参数"
                    },
                    "format": {
                        "type": "string",
                        "description": "目标格式",
                        "enum": ["pdf", "docx", "xlsx", "pptx", "jpg", "jpeg", "png", "bmp", "gif", "html", "txt"]
                    }
                },
                "required": ["file_paths", "format"]
            }
        ),
        types.Tool(
            name="remove_watermark",
            description="去除PDF文件中的水印，将文件处理后返回无水印的PDF版本。",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_paths": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "PDF文件路径或URL的列表"
                    },
                    "password": {
                        "type": "string",
                        "description": "PDF文档密码，如果文档受密码保护，则需要提供此参数"
                    }
                },
                "required": ["file_paths"]
            }
        ),
        types.Tool(
            name="add_page_numbers",
            description="在PDF文档的每一页上添加页码。",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_paths": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "PDF文件路径或URL的列表"
                    },
                    "password": {
                        "type": "string",
                        "description": "PDF文档密码，如果文档受密码保护，则需要提供此参数"
                    },
                    "start_num": {
                        "type": "integer",
                        "description": "起始页码",
                        "default": 1,
                        "minimum": 1
                    },
                    "position": {
                        "type": "string",
                        "description": "页码位置：1(左上), 2(上中), 3(右上), 4(左下), 5(下中), 6(右下)",
                        "enum": ["1", "2", "3", "4", "5", "6"],
                        "default": "5"
                    },
                    "margin": {
                        "type": "integer",
                        "description": "页码边距",
                        "enum": [10, 30, 60],
                        "default": 30
                    }
                },
                "required": ["file_paths"]
            }
        ),
        types.Tool(
            name="unlock_pdf",
            description="移除PDF文件的密码保护，生成无密码版本的PDF文件。",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_paths": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "需要解密的PDF文件路径或URL的列表"
                    },
                    "password": {
                        "type": "string",
                        "description": "PDF文档的密码，用于解锁文档"
                    }
                },
                "required": ["file_paths"]
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    # 创建日志记录器
    logger = Logger(app.request_context)
    
    # 定义工具配置和默认参数值
    TOOL_CONFIG = {
        "convert_document": {
            "format_key": "format",  # 从arguments获取format
            "is_watermark_removal": False,
            "is_page_numbering": False,
        },
        "remove_watermark": {
            "format": "doc-repair",  # 固定format
            "is_watermark_removal": True,
            "is_page_numbering": False,
        },
        "add_page_numbers": {
            "format": "number-pdf",  # 固定format
            "is_watermark_removal": False,
            "is_page_numbering": True,
            "param_keys": ["start_num", "position", "margin"]  # 需要从arguments获取的参数
        },
        "unlock_pdf": {
            "edit_type": "decrypt",  # 编辑类型
            "is_edit_operation": True,  # 标记为编辑操作
        }
    }
    
    DEFAULTS = {
        "start_num": 1,
        "position": "5",
        "margin": 30
    }
    
    if name in TOOL_CONFIG:
        # 处理文件路径
        file_paths = arguments.get("file_paths", [])
        if isinstance(file_paths, str):
            file_paths = [file_paths]
            
        config = TOOL_CONFIG[name]
        
        # 检查是否为编辑操作
        if config.get("is_edit_operation"):
            # 调用编辑处理函数
            result = await _process_edit_tool_call(
                logger,
                file_paths,
                edit_type=config["edit_type"],
                password=arguments.get("password")
            )
            return [result]
        else:
            # 确定格式
            format = config.get("format")
            if not format and "format_key" in config:
                format = arguments.get(config["format_key"], "")
            
            # 处理额外参数
            extra_params = None
            if "param_keys" in config:
                extra_params = {key: arguments.get(key, DEFAULTS.get(key)) for key in config["param_keys"]}
            
            # 调用通用处理函数
            result = await _process_tool_call(
                logger,
                file_paths,
                format,
                is_watermark_removal=config["is_watermark_removal"],
                is_page_numbering=config["is_page_numbering"],
                extra_params=extra_params,
                password=arguments.get("password")
            )
            return [result]
    
    error_msg = f"未知工具: {name}"
    await logger.error(error_msg, ValueError)

# 添加edit_pdf功能的报告生成函数
def generate_edit_report(results: List[EditResult], operation_name: str) -> str:
    """生成PDF编辑操作的报告
    
    Args:
        results: 编辑结果列表
        operation_name: 操作名称（如"解密"、"加密"等）
        
    Returns:
        str: 格式化的报告文本
    """
    # 统计结果
    success_count = sum(1 for r in results if r.success)
    failed_count = len(results) - success_count
    
    # 生成报告头部
    report_lines = [
        f"PDF{operation_name}结果：共 {len(results)} 个文件" + (
            f"，成功 {success_count} 个" if success_count > 0 else ""
        ) + (
            f"，失败 {failed_count} 个" if failed_count > 0 else ""
        ),
        ""
    ]
    
    # 添加成功的文件信息
    if success_count > 0:
        report_lines.extend([f"[成功] {operation_name}成功的文件：", ""])
        for i, result in enumerate(results):
            if result.success:
                report_lines.extend([
                    f"[{i+1}] {result.file_path}",
                    f"- 在线下载地址: {result.download_url}",
                    ""
                ])
    
    # 添加失败的文件信息
    if failed_count > 0:
        report_lines.extend([f"[失败] {operation_name}失败的文件：", ""])
        for i, result in enumerate(results):
            if not result.success:
                report_lines.extend([
                    f"[{i+1}] {result.file_path}",
                    f"- 错误: {result.error_message}",
                    ""
                ])
    
    return "\n".join(report_lines)

# 处理PDF编辑功能的函数
async def process_edit_files(file_paths: List[str], edit_type: str, logger: Logger, editor: Editor, password: str = None) -> List[EditResult]:
    """处理PDF编辑功能
    
    Args:
        file_paths: 要处理的文件路径列表
        edit_type: 编辑类型（如"decrypt"表示解密）
        logger: 日志记录器
        editor: 编辑器实例
        password: 文档密码
        
    Returns:
        List[EditResult]: 编辑结果列表
    """
    # 操作描述文本
    operation_map = {
        "decrypt": "解密"
    }
    operation_type = operation_map.get(edit_type, edit_type)
    
    # 定义处理单个文件的函数
    async def process_single_file(file_path: str):
        if edit_type == "decrypt":
            return await editor.decrypt_pdf(file_path, password)
        else:
            await logger.error(f"不支持的编辑类型: {edit_type}")
            return EditResult(success=False, file_path=file_path, error_message=f"不支持的编辑类型: {edit_type}")
    
    if len(file_paths) > 1:
        await logger.log("info", f"开始批量PDF{operation_type}，共 {len(file_paths)} 个文件")
        
        # 并发处理文件，限制并发数为5
        semaphore = asyncio.Semaphore(5)
        
        async def process_with_semaphore(file_path: str):
            async with semaphore:
                return await process_single_file(file_path)
        
        # 创建任务列表
        tasks = [process_with_semaphore(file_path) for file_path in file_paths]
        return await asyncio.gather(*tasks)
    else:
        # 单文件处理
        return [await process_single_file(file_paths[0])]

# 处理PDF编辑工具调用的通用逻辑
async def _process_edit_tool_call(logger: Logger, file_paths: List[str], edit_type: str, 
                          password: str = None) -> types.TextContent:
    """处理PDF编辑工具调用的通用逻辑
    
    Args:
        logger: 日志记录器
        file_paths: 文件路径列表
        edit_type: 编辑类型
        password: 文档密码
        
    Returns:
        types.TextContent: 包含处理结果的文本内容
    """
    # 创建必要的对象
    file_handler = FileHandler(logger)
    editor = Editor(logger, file_handler)
    
    # 如果是解密操作但没有提供密码，记录警告
    if edit_type == "decrypt" and not password:
        await logger.log("warning", "未提供PDF密码，如果文档受密码保护，操作可能会失败")
    
    # 处理文件
    results = await process_edit_files(file_paths, edit_type, logger, editor, password)
    
    # 生成报告
    operation_map = {
        "decrypt": "解密"
    }
    operation_name = operation_map.get(edit_type, edit_type)
    report_msg = generate_edit_report(results, operation_name)
    
    # 如果全部失败，记录错误
    if not any(r.success for r in results):
        await logger.error(report_msg)
    
    return types.TextContent(
        type="text",
        text=report_msg
    )

async def main():
    import mcp.server.stdio as stdio
    
    async with stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(
                notification_options=NotificationOptions()
            )
        )

def cli_main():
    asyncio.run(main())

if __name__ == "__main__":
    cli_main()
