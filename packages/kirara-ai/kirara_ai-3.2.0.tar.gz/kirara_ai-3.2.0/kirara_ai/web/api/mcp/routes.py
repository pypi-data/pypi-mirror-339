#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quart import Blueprint, g, jsonify, request

from kirara_ai.config.config_loader import CONFIG_FILE, ConfigLoader
from kirara_ai.config.global_config import GlobalConfig, MCPServerConfig
from kirara_ai.logger import get_logger
from kirara_ai.mcp.manager import MCPServerManager
from kirara_ai.mcp.models import ConnectionType, ServerStatus
from kirara_ai.web.api.mcp.models import (MCPServerList, MCPServerListResponse, MCPServerResponse,
                                          MCPToolListResponse, MCPStatisticsResponse,
                                          MCPServerCreateRequest, MCPServerUpdateRequest,
                                          MessageResponse)

from ...auth.middleware import require_auth

# 创建蓝图
mcp_bp = Blueprint("mcp", __name__)
logger = get_logger("WebServer.MCP")


@mcp_bp.route("/servers", methods=["GET"])
@require_auth
async def list_servers():
    """获取所有MCP服务器列表"""
    try:
        # 从容器中获取MCP服务器管理器
        manager: MCPServerManager = g.container.resolve(MCPServerManager)

        # 获取所有服务器
        servers = manager.get_all_servers()

        # 返回响应
        return MCPServerListResponse(
            data=MCPServerList(servers=servers)
        ).model_dump()
    except Exception as e:
        logger.opt(exception=e).error("获取MCP服务器列表失败")
        return jsonify({"success": False, "message": str(e)}), 500


@mcp_bp.route("/statistics", methods=["GET"])
@require_auth
async def get_statistics():
    """获取MCP服务器统计信息"""
    try:
        # 从容器中获取MCP服务器管理器
        manager: MCPServerManager = g.container.resolve(MCPServerManager)

        # 获取统计信息
        stats = manager.get_statistics()

        # 返回响应
        return MCPStatisticsResponse(
            data={
                "total_servers": stats.get("total", 0),
                "standard_io_servers": stats.get("standard_io", 0),
                "sse_servers": stats.get("sse", 0),
                "running_servers": stats.get("running", 0),
                "stopped_servers": stats.get("stopped", 0),
                "error_servers": stats.get("error", 0)
            }
        ).model_dump()
    except Exception as e:
        logger.opt(exception=e).error("获取MCP统计信息失败")
        return jsonify({"success": False, "message": str(e)}), 500


@mcp_bp.route("/servers/<server_id>", methods=["GET"])
@require_auth
async def get_server(server_id: str):
    """获取特定MCP服务器的详情"""
    try:
        # 从容器中获取MCP服务器管理器
        manager: MCPServerManager = g.container.resolve(MCPServerManager)

        # 获取服务器
        server = manager.get_server(server_id)
        if not server:
            return jsonify({"success": False, "message": f"服务器 {server_id} 不存在"}), 404

        # 返回响应
        return MCPServerResponse(data=server).model_dump()
    except Exception as e:
        logger.opt(exception=e).error(f"获取MCP服务器 {server_id} 详情失败")
        return jsonify({"success": False, "message": str(e)}), 500


@mcp_bp.route("/servers/<server_id>/tools", methods=["GET"])
@require_auth
async def get_server_tools(server_id: str):
    """获取MCP服务器提供的工具列表"""
    try:
        # 从容器中获取MCP服务器管理器
        manager: MCPServerManager = g.container.resolve(MCPServerManager)

        # 获取服务器工具
        tools = await manager.get_server_tools(server_id)
        if tools is None:
            return jsonify({"success": False, "message": f"服务器 {server_id} 不存在"}), 404

        # 返回响应
        return MCPToolListResponse(data=tools).model_dump()
    except Exception as e:
        logger.opt(exception=e).error(f"获取MCP服务器 {server_id} 工具列表失败")
        return jsonify({"success": False, "message": str(e)}), 500


@mcp_bp.route("/servers/check/<server_id>", methods=["GET"])
@require_auth
async def check_server_id(server_id: str):
    """检查服务器ID是否可用"""
    try:
        # 从容器中获取MCP服务器管理器
        manager: MCPServerManager = g.container.resolve(MCPServerManager)

        # 检查ID是否可用
        is_available = manager.is_server_id_available(server_id)

        # 返回响应
        return jsonify({
            "success": True,
            "is_available": is_available,
            "message": "ID可用" if is_available else "ID已存在"
        })
    except Exception as e:
        logger.opt(exception=e).error(f"检查服务器ID {server_id} 可用性失败")
        return jsonify({"success": False, "message": str(e)}), 500


@mcp_bp.route("/servers", methods=["POST"])
@require_auth
async def create_server():
    """创建新的MCP服务器"""
    try:
        # 获取请求数据
        data = await request.get_json()
        request_data = MCPServerCreateRequest(**data)

        # 从容器中获取全局配置和MCP服务器管理器
        config: GlobalConfig = g.container.resolve(GlobalConfig)
        manager: MCPServerManager = g.container.resolve(MCPServerManager)

        # 检查ID是否已存在
        if not manager.is_server_id_available(request_data.id):
            return jsonify({"success": False, "message": f"服务器ID '{request_data.id}' 已存在"}), 409

        # 创建新的MCP服务器配置
        new_server_config = MCPServerConfig(
            id=request_data.id,
            description=request_data.description or "",
            command=request_data.command,
            args=request_data.args,
            connection_type=request_data.connection_type,
            enable=True
        )

        # 添加到全局配置中
        config.mcp.servers.append(new_server_config)

        # 保存配置
        ConfigLoader.save_config_with_backup(CONFIG_FILE, config)

        # 让管理器加载新服务器
        server = manager.load_server(new_server_config)

        # 返回响应
        return MCPServerResponse(
            message=f"MCP服务器 '{request_data.id}' 创建成功",
            data=server
        ).model_dump()
    except Exception as e:
        logger.opt(exception=e).error("创建MCP服务器失败")
        return jsonify({"success": False, "message": str(e)}), 500


@mcp_bp.route("/servers/<server_id>", methods=["PUT"])
@require_auth
async def update_server(server_id: str):
    """更新MCP服务器配置"""
    try:
        # 获取请求数据
        data = await request.get_json()
        request_data = MCPServerUpdateRequest(**data)

        # 从容器中获取全局配置和MCP服务器管理器
        config: GlobalConfig = g.container.resolve(GlobalConfig)
        manager: MCPServerManager = g.container.resolve(MCPServerManager)

        # 查找服务器配置
        server_index = -1
        for i, server in enumerate(config.mcp.servers):
            if server.id == server_id:
                server_index = i
                break

        if server_index == -1:
            return jsonify({"success": False, "message": f"服务器 '{server_id}' 不存在"}), 404

        # 检查服务器状态
        current_server = manager.get_server(server_id)
        if current_server and current_server.status == ServerStatus.RUNNING:
            return jsonify({"success": False, "message": "无法更新正在运行的服务器，请先停止服务器"}), 409

        # 更新服务器配置
        server_config = config.mcp.servers[server_index]

        if request_data.description is not None:
            server_config.description = request_data.description

        if request_data.command is not None:
            server_config.command = request_data.command

        if request_data.args is not None:
            server_config.args = request_data.args

        if request_data.connection_type is not None:
            server_config.connection_type = request_data.connection_type

        # 保存配置
        ConfigLoader.save_config_with_backup(CONFIG_FILE, config)

        # 重新加载服务器
        updated_server = manager.load_server(server_config)

        # 返回响应
        return MCPServerResponse(
            message=f"MCP服务器 '{server_id}' 更新成功",
            data=updated_server
        ).model_dump()
    except Exception as e:
        logger.opt(exception=e).error(f"更新MCP服务器 {server_id} 失败")
        return jsonify({"success": False, "message": str(e)}), 500


@mcp_bp.route("/servers/<server_id>", methods=["DELETE"])
@require_auth
async def delete_server(server_id: str):
    """删除MCP服务器"""
    try:
        # 从容器中获取全局配置和MCP服务器管理器
        config: GlobalConfig = g.container.resolve(GlobalConfig)
        manager: MCPServerManager = g.container.resolve(MCPServerManager)

        # 查找服务器配置
        server_index = -1
        for i, server in enumerate(config.mcp.servers):
            if server.id == server_id:
                server_index = i
                break

        if server_index == -1:
            return jsonify({"success": False, "message": f"服务器 '{server_id}' 不存在"}), 404

        # 如果服务器正在运行，先停止它
        current_server = manager.get_server(server_id)
        if current_server and current_server.status == ServerStatus.RUNNING:
            await manager.stop_server(server_id)

        # 从配置中删除服务器
        removed_server = config.mcp.servers.pop(server_index)

        # 保存配置
        ConfigLoader.save_config_with_backup(CONFIG_FILE, config)

        # 让管理器卸载服务器
        manager.unload_server(server_id)

        # 返回响应
        return MessageResponse(
            message=f"MCP服务器 '{server_id}' 删除成功"
        ).model_dump()
    except Exception as e:
        logger.opt(exception=e).error(f"删除MCP服务器 {server_id} 失败")
        return jsonify({"success": False, "message": str(e)}), 500


@mcp_bp.route("/servers/<server_id>/start", methods=["POST"])
@require_auth
async def start_server(server_id: str):
    """启动MCP服务器"""
    try:
        # 从容器中获取MCP服务器管理器
        manager: MCPServerManager = g.container.resolve(MCPServerManager)

        # 尝试启动服务器
        success = await manager.start_server(server_id)

        if not success:
            return jsonify({"success": False, "message": f"服务器 '{server_id}' 不存在或无法启动"}), 404

        # 返回响应
        return MessageResponse(
            message=f"MCP服务器 '{server_id}' 启动成功"
        ).model_dump()
    except Exception as e:
        logger.opt(exception=e).error(f"启动MCP服务器 {server_id} 失败")
        return jsonify({"success": False, "message": str(e)}), 500


@mcp_bp.route("/servers/<server_id>/stop", methods=["POST"])
@require_auth
async def stop_server(server_id: str):
    """停止MCP服务器"""
    try:
        # 从容器中获取MCP服务器管理器
        manager: MCPServerManager = g.container.resolve(MCPServerManager)

        # 尝试停止服务器
        success = await manager.stop_server(server_id)

        if not success:
            return jsonify({"success": False, "message": f"服务器 '{server_id}' 不存在或未运行"}), 404

        # 返回响应
        return MessageResponse(
            message=f"MCP服务器 '{server_id}' 停止成功"
        ).model_dump()
    except Exception as e:
        logger.opt(exception=e).error(f"停止MCP服务器 {server_id} 失败")
        return jsonify({"success": False, "message": str(e)}), 500
