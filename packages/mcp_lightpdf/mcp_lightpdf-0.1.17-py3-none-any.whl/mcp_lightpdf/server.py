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

# 加载环境变量
load_dotenv()

# 创建Server实例
app = Server(
    name="lightpdf_convert_document",
    instructions="文档格式转换工具。支持PDF与其他格式的相互转换。",
)

def generate_report(results: List[ConversionResult]) -> str:
    """生成转换报告
    
    Args:
        results: 转换结果列表
        
    Returns:
        str: 格式化的报告文本
    """
    # 统计结果
    success_count = sum(1 for r in results if r.success)
    failed_count = len(results) - success_count
    
    # 生成报告头部
    report_lines = [
        f"转换结果：共 {len(results)} 个文件，成功 {success_count} 个，失败 {failed_count} 个",
        ""
    ]
    
    # 添加成功的文件信息
    if success_count > 0:
        report_lines.extend(["[成功] 转换成功的文件：", ""])
        for i, result in enumerate(results):
            if result.success:
                file_size_kb = result.file_size / 1024
                report_lines.extend([
                    f"[{i+1}] {result.file_path}",
                    f"- 在线下载地址: {result.download_url}",
                    f"- 本地保存位置: {result.output_path}",
                    f"- 文件大小: {file_size_kb:.2f} KB",
                    ""
                ])
    
    # 添加失败的文件信息
    if failed_count > 0:
        report_lines.extend(["[失败] 转换失败的文件：", ""])
        for i, result in enumerate(results):
            if not result.success:
                report_lines.extend([
                    f"[{i+1}] {result.file_path}",
                    f"- 错误: {result.error_message}",
                    ""
                ])
    
    return "\n".join(report_lines)

async def process_files(file_paths: List[str], format: str, logger: Logger, converter: Converter, remove_watermark: bool = False) -> List[ConversionResult]:
    """处理文件转换
    
    Args:
        file_paths: 要转换的文件路径列表
        format: 目标格式
        logger: 日志记录器
        converter: 转换器实例
        remove_watermark: 是否去除水印
        
    Returns:
        List[ConversionResult]: 转换结果列表
    """
    if len(file_paths) > 1:
        operation_desc = "批量去除水印" if remove_watermark else f"批量转换为 {format} 格式"
        await logger.log("info", f"开始{operation_desc}，共 {len(file_paths)} 个文件")
        
        # 并发处理文件，限制并发数为5
        semaphore = asyncio.Semaphore(5)
        
        async def process_single_file(file_path: str):
            async with semaphore:
                if remove_watermark:
                    return await converter.convert_file(file_path, "pdf", {"remove_watermark": True})
                else:
                    return await converter.convert_file(file_path, format)
        
        # 创建任务列表
        tasks = [process_single_file(file_path) for file_path in file_paths]
        return await asyncio.gather(*tasks)
    else:
        # 单文件处理
        if remove_watermark:
            result = await converter.convert_file(file_paths[0], "pdf", {"remove_watermark": True})
        else:
            result = await converter.convert_file(file_paths[0], format)
        return [result]

# 定义工具
@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="convert_document",
            description="文档格式转换工具。\n\nPDF可转换为：DOCX/XLSX/PPTX/图片/HTML/TXT，\n其他格式可转换为PDF：DOCX/XLSX/PPTX/图片/CAD/CAJ/OFD",
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
    
    if name == "convert_document":
        file_paths = arguments.get("file_paths", [])
        # 如果传入的是字符串，转换为列表
        if isinstance(file_paths, str):
            file_paths = [file_paths]
        format = arguments.get("format", "")
        
        # 创建必要的对象
        file_handler = FileHandler(logger)
        converter = Converter(logger, file_handler)
        
        # 处理文件转换
        results = await process_files(file_paths, format, logger, converter)
        
        # 生成报告
        report_msg = generate_report(results)
        
        # 如果全部失败，记录错误
        if not any(r.success for r in results):
            await logger.error(report_msg)
        
        return [types.TextContent(
            type="text",
            text=report_msg
        )]
    elif name == "remove_watermark":
        file_paths = arguments.get("file_paths", [])
        # 如果传入的是字符串，转换为列表
        if isinstance(file_paths, str):
            file_paths = [file_paths]
        
        # 创建必要的对象
        file_handler = FileHandler(logger)
        converter = Converter(logger, file_handler)
        
        # 处理去除水印
        results = await process_files(file_paths, "pdf", logger, converter, remove_watermark=True)
        
        # 生成报告
        report_msg = generate_report(results)
        
        # 如果全部失败，记录错误
        if not any(r.success for r in results):
            await logger.error(report_msg)
        
        return [types.TextContent(
            type="text",
            text=report_msg
        )]
    
    error_msg = f"未知工具: {name}"
    await logger.error(error_msg, ValueError)

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
