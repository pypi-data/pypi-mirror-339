# -*- coding: utf-8 -*-
# server.py
# Copyright (c) 2025 zedmoster
# Revit integration through the Model Context Protocol.

from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from .revit_connection import RevitConnection
from .resources import get_all_builtin_category, get_greeting
from .prompts import asset_creation_strategy
from .tools import *
import types
import logging
import asyncio
import inspect

# 创建日志格式
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)

# 创建日志器
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 防止日志重复输出
if not logger.handlers:
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    logger.propagate = False

# 全局资源连接
_revit_connection: Optional[RevitConnection] = None
_haven_enabled: bool = False
_port: int = 8080

# 工具分类
ARCHITECTURAL_TOOLS = [
    create_levels, create_floor_plan_views, create_grids, create_walls, create_floors,
    create_door_windows, create_rooms, create_room_tags, create_family_instances, create_sheets
]

MEP_TOOLS = [
    create_ducts, create_pipes, create_cable_trays
]

GENERAL_TOOLS = [
    get_commands, execute_commands, call_func,
    find_elements, update_elements, delete_elements, parameter_elements, get_locations, move_elements,
    show_elements, active_view, get_selected_elements,
    link_dwg_and_activate_view,
]


def get_revit_connection() -> RevitConnection:
    """
    获取或创建持久的Revit连接

    返回:
        RevitConnection: 与Revit的连接对象

    异常:
        Exception: 连接失败时抛出
    """
    global _revit_connection, _haven_enabled

    if _revit_connection is not None:
        try:
            # 测试连接是否有效
            result = _revit_connection.send_command("get_haven_status")
            _haven_enabled = result.get("enabled", False)
            return _revit_connection
        except Exception as e:
            logger.warning(f"现有连接已失效: {str(e)}")
            try:
                _revit_connection.disconnect()
            except:
                pass
            _revit_connection = None

    # 创建新连接
    if _revit_connection is None:
        _revit_connection = RevitConnection(host="localhost", port=_port)
        if not _revit_connection.connect():
            logger.error("无法连接到Revit")
            _revit_connection = None
            raise Exception(
                "无法连接到Revit。请确保Revit插件正在运行。")
        logger.info("已创建新的持久连接到Revit")

    return _revit_connection


@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """
    管理服务器启动和关闭生命周期

    参数:
        server: FastMCP服务器实例
    """
    try:
        logger.info("RevitMCP服务器正在启动")
        try:
            get_revit_connection()
            logger.info("服务器启动时成功连接到Revit")
        except Exception as e:
            logger.warning(f"服务器启动时无法连接到Revit: {str(e)}")
            logger.warning(
                "在使用Revit资源或工具前，请确保Revit插件正在运行")

        yield {}
    finally:
        global _revit_connection
        if _revit_connection:
            logger.info("服务器关闭时断开与Revit的连接")
            _revit_connection.disconnect()
            _revit_connection = None
        logger.info("RevitMCP服务器已关闭")


# 创建带有生命周期支持的MCP服务器
mcp = FastMCP(
    "RevitMCP",
    description="通过模型上下文协议(MCP)集成Revit",
    lifespan=server_lifespan
)


def list_tools(self):
    """
    列出所有注册到MCP服务器的工具，并按类别分组

    返回:
        dict: 分类的工具字典，包含名称、描述和参数信息
    """
    tools_info = {
        "architectural": [],
        "mep": [],
        "general": []
    }

    # 获取建筑工具信息
    for tool in ARCHITECTURAL_TOOLS:
        # 获取函数签名
        sig = inspect.signature(tool)
        params = []
        for param_name, param in sig.parameters.items():
            if param_name != 'ctx':  # 排除上下文参数
                param_info = {
                    "name": param_name,
                    "required": param.default == inspect.Parameter.empty,
                    "default": None if param.default == inspect.Parameter.empty else param.default
                }
                params.append(param_info)

        tool_info = {
            "name": tool.__name__,
            "description": inspect.getdoc(tool).split('\n')[0] if inspect.getdoc(tool) else "无描述",
            "full_doc": inspect.getdoc(tool),
            "parameters": params
        }
        tools_info["architectural"].append(tool_info)

    # 获取MEP工具信息
    for tool in MEP_TOOLS:
        sig = inspect.signature(tool)
        params = []
        for param_name, param in sig.parameters.items():
            if param_name != 'ctx':
                param_info = {
                    "name": param_name,
                    "required": param.default == inspect.Parameter.empty,
                    "default": None if param.default == inspect.Parameter.empty else param.default
                }
                params.append(param_info)

        tool_info = {
            "name": tool.__name__,
            "description": inspect.getdoc(tool).split('\n')[0] if inspect.getdoc(tool) else "无描述",
            "full_doc": inspect.getdoc(tool),
            "parameters": params
        }
        tools_info["mep"].append(tool_info)

    # 获取通用工具信息
    for tool in GENERAL_TOOLS:
        sig = inspect.signature(tool)
        params = []
        for param_name, param in sig.parameters.items():
            if param_name != 'ctx':
                param_info = {
                    "name": param_name,
                    "required": param.default == inspect.Parameter.empty,
                    "default": None if param.default == inspect.Parameter.empty else param.default
                }
                params.append(param_info)

        tool_info = {
            "name": tool.__name__,
            "description": inspect.getdoc(tool).split('\n')[0] if inspect.getdoc(tool) else "无描述",
            "full_doc": inspect.getdoc(tool),
            "parameters": params
        }
        tools_info["general"].append(tool_info)

    # 添加所有工具的汇总列表
    all_tools = []
    all_tools.extend(tools_info["architectural"])
    all_tools.extend(tools_info["mep"])
    all_tools.extend(tools_info["general"])
    tools_info["all"] = all_tools

    logger.info(f"获取到 {len(all_tools)} 个工具函数")
    return tools_info


async def call_tool(self, tool_name: str, **kwargs):
    """
    调用指定的工具并传入参数

    参数:
        tool_name (str): 要调用的工具名称
        **kwargs: 传递给工具的参数

    返回:
        Any: 工具的执行结果

    异常:
        ValueError: 当工具不存在或参数无效时抛出
        Exception: 工具执行失败时抛出的其他异常
    """
    logger.info(f"尝试调用工具: {tool_name}, 参数: {kwargs}")

    # 获取所有工具字典
    all_tools = {}
    for tool in ARCHITECTURAL_TOOLS + MEP_TOOLS + GENERAL_TOOLS:
        all_tools[tool.__name__] = tool

    # 查找并调用工具
    if tool_name in all_tools:
        try:
            # 检查工具函数
            tool_func = all_tools[tool_name]
            sig = inspect.signature(tool_func)

            # 验证必要参数
            missing_params = []
            for param_name, param in sig.parameters.items():
                if param_name != 'ctx' and param_name != 'revit_connection' and param.default == inspect.Parameter.empty:
                    if param_name not in kwargs:
                        missing_params.append(param_name)

            if missing_params:
                raise ValueError(f"调用 {tool_name} 缺少必要参数: {', '.join(missing_params)}")

            # 添加Revit连接参数(如果需要)
            if 'revit_connection' in sig.parameters:
                kwargs['revit_connection'] = get_revit_connection()

            # 调用工具函数(异步或同步)
            if asyncio.iscoroutinefunction(tool_func):
                result = await tool_func(**kwargs)
            else:
                result = tool_func(**kwargs)

            return result

        except ValueError as ve:
            logger.error(f"调用工具 '{tool_name}' 参数错误: {str(ve)}")
            raise
        except Exception as e:
            logger.error(f"调用工具 '{tool_name}' 失败: {str(e)}")
            raise
    else:
        # 提供可用工具列表
        available_tools = list(all_tools.keys())
        logger.error(f"工具 '{tool_name}' 不存在")
        raise ValueError(f"工具 '{tool_name}' 不存在。可用的工具有: {available_tools}")


def list_prompts(self):
    """
    列出所有注册到MCP服务器的提示

    返回:
        list: 包含详细信息的提示列表
    """
    logger.info("获取MCP服务器提示列表")

    # 获取资产创建策略提示的详细信息
    asset_strategy_doc = inspect.getdoc(asset_creation_strategy)
    asset_strategy_summary = asset_strategy_doc.split('\n')[0] if asset_strategy_doc else "无描述"

    prompts = [
        {
            "name": "asset_creation_strategy",
            "description": asset_strategy_summary,
            "full_doc": asset_strategy_doc,
            "usage": "用于指导AI如何创建Revit资产和执行设计任务",
            "parameters": {
                "context": "当前设计上下文信息",
                "requirements": "用户设计要求",
                "constraints": "设计约束条件"
            },
            "example": {
                "context": "办公建筑设计",
                "requirements": "需要创建标准办公层平面",
                "constraints": "建筑面积限制为1000平方米"
            }
        }
    ]

    logger.info(f"获取到 {len(prompts)} 个提示")
    return prompts


def list_resource_templates(self):
    """
    列出所有注册到MCP服务器的资源模板

    返回:
        list: 包含详细信息的资源模板列表
    """
    logger.info("获取MCP服务器资源模板列表")

    # 获取资源处理函数的文档
    builtin_category_doc = inspect.getdoc(get_all_builtin_category)
    greeting_doc = inspect.getdoc(get_greeting)

    templates = [
        {
            "template": "config://BuiltInCategory",
            "description": "获取所有内置类别",
            "function": "get_all_builtin_category",
            "doc": builtin_category_doc,
            "return_format": "返回Revit内置类别的完整列表，包括类别ID和名称",
            "usage_example": "config://BuiltInCategory"
        },
        {
            "template": "greeting://{name}",
            "description": "获取问候信息",
            "function": "get_greeting",
            "doc": greeting_doc,
            "parameters": {
                "name": "要问候的用户名称"
            },
            "return_format": "返回针对指定用户的问候消息",
            "usage_example": "greeting://John"
        }
    ]

    logger.info(f"获取到 {len(templates)} 个资源模板")
    return templates


# 将这些方法绑定到mcp实例
mcp.list_tools = types.MethodType(list_tools, mcp)
mcp.call_tool = types.MethodType(call_tool, mcp)
mcp.list_prompts = types.MethodType(list_prompts, mcp)
mcp.list_resource_templates = types.MethodType(list_resource_templates, mcp)

mcp.prompt()(asset_creation_strategy)
mcp.resource("config://BuiltInCategory")(get_all_builtin_category)
mcp.resource("greeting://{name}")(get_greeting)


def main():
    """运行MCP服务器"""
    logger.info("启动RevitMCP服务器...")
    try:
        mcp.run()
    except Exception as e:
        logger.error(f"服务器运行时发生错误: {str(e)}")
        raise


if __name__ == "__main__":
    main()
