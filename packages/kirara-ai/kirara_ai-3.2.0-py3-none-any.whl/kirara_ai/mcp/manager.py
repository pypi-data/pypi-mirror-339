#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Union

from pydantic import ValidationError

from kirara_ai.config.global_config import GlobalConfig, MCPServerConfig
from kirara_ai.logger import get_logger
from kirara_ai.mcp.models import MCPServer, MCPTool, ConnectionType, ServerStatus
from kirara_ai.utils.singleton import Singleton

logger = get_logger("MCPServerManager")

class MCPServerManager(metaclass=Singleton):
    """MCP服务器管理器，负责管理和控制MCP服务器进程"""

    def __init__(self, config: GlobalConfig):
        """初始化MCP服务器管理器"""
        self.config = config
        self.servers: Dict[str, MCPServer] = {}
        self.processes: Dict[str, subprocess.Popen] = {}
        self.tools_cache: Dict[str, List[MCPTool]] = {}
        
        # 加载所有配置的服务器
        self.load_servers()
        
        logger.info(f"MCP服务器管理器初始化完成，加载了 {len(self.servers)} 个服务器")
        
        # 自动启动服务器（如果配置了自动启动）
        if self.config.mcp.auto_start:
            asyncio.create_task(self._auto_start_servers())
            
    async def _auto_start_servers(self):
        """自动启动所有启用的服务器"""
        for server_id, server in self.servers.items():
            # 查找对应的服务器配置
            server_config = next((s for s in self.config.mcp.servers if s.id == server_id), None)
            if server_config and server_config.enable:
                try:
                    logger.info(f"正在自动启动MCP服务器: {server_id}")
                    await self.start_server(server_id)
                except Exception as e:
                    logger.opt(exception=e).error(f"自动启动MCP服务器 {server_id} 失败")
                    
                # 等待一小段时间，避免同时启动多个服务器导致资源争用
                await asyncio.sleep(2)
    
    def load_servers(self):
        """从配置加载所有MCP服务器"""
        for server_config in self.config.mcp.servers:
            try:
                self.load_server(server_config)
            except Exception as e:
                logger.opt(exception=e).error(f"加载MCP服务器 {server_config.id} 失败")
    
    def load_server(self, server_config: MCPServerConfig) -> MCPServer:
        """从配置加载单个MCP服务器"""
        server = MCPServer(
            id=server_config.id,
            description=server_config.description,
            command=server_config.command,
            args=server_config.args,
            connection_type=ConnectionType(server_config.connection_type),
            status=ServerStatus.STOPPED,
            error_message="",
            created_at=datetime.now(),
            last_used_at=None
        )
        self.servers[server_config.id] = server
        return server
    
    def unload_server(self, server_id: str) -> bool:
        """卸载MCP服务器"""
        if server_id in self.servers:
            # 如果服务器正在运行，先停止它
            if self.servers[server_id].status == ServerStatus.RUNNING:
                asyncio.create_task(self.stop_server(server_id))
            
            # 从内存中移除服务器
            self.servers.pop(server_id, None)
            self.processes.pop(server_id, None)
            self.tools_cache.pop(server_id, None)
            return True
        return False
    
    def get_all_servers(self) -> List[MCPServer]:
        """获取所有MCP服务器列表"""
        return list(self.servers.values())
    
    def get_server(self, server_id: str) -> Optional[MCPServer]:
        """获取指定ID的MCP服务器"""
        return self.servers.get(server_id)
    
    def is_server_id_available(self, server_id: str) -> bool:
        """检查服务器ID是否可用（不存在）"""
        return server_id not in self.servers
    
    def get_statistics(self) -> Dict[str, int]:
        """获取MCP服务器统计信息"""
        total = len(self.servers)
        standard_io = sum(1 for s in self.servers.values() if s.connection_type == ConnectionType.STANDARD_IO)
        sse = sum(1 for s in self.servers.values() if s.connection_type == ConnectionType.SSE)
        running = sum(1 for s in self.servers.values() if s.status == ServerStatus.RUNNING)
        stopped = sum(1 for s in self.servers.values() if s.status == ServerStatus.STOPPED)
        error = sum(1 for s in self.servers.values() if s.status == ServerStatus.ERROR)
        
        return {
            "total": total,
            "standard_io": standard_io,
            "sse": sse,
            "running": running,
            "stopped": stopped,
            "error": error
        }
    
    async def start_server(self, server_id: str) -> bool:
        """启动MCP服务器"""
        server = self.servers.get(server_id)
        if not server:
            logger.error(f"无法启动不存在的MCP服务器: {server_id}")
            return False
        
        if server.status == ServerStatus.RUNNING:
            logger.warning(f"MCP服务器 {server_id} 已经在运行中")
            return True
        
        try:
            # 构建命令行
            cmd = [server.command]
            if server.args:
                cmd.extend(server.args.split())
            
            logger.info(f"正在启动MCP服务器 {server_id}: {' '.join(cmd)}")
            
            # 启动进程
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # 保存进程引用
            self.processes[server_id] = process
            
            # 等待短暂时间，确保进程启动
            await asyncio.sleep(2)
            
            # 检查进程是否还在运行
            if process.poll() is not None:
                # 进程已结束，获取错误信息
                _, stderr = process.communicate()
                error_msg = stderr or "未知错误"
                
                # 更新服务器状态
                server.status = ServerStatus.ERROR
                server.error_message = error_msg
                logger.error(f"MCP服务器 {server_id} 启动失败: {error_msg}")
                return False
            
            # 更新服务器状态
            server.status = ServerStatus.RUNNING
            server.error_message = ""
            server.last_used_at = datetime.now()
            
            # 清除工具缓存，以便下次获取最新的工具列表
            self.tools_cache.pop(server_id, None)
            
            logger.info(f"MCP服务器 {server_id} 已成功启动")
            return True
            
        except Exception as e:
            logger.opt(exception=e).error(f"启动MCP服务器 {server_id} 时发生错误")
            server.status = ServerStatus.ERROR
            server.error_message = str(e)
            return False
    
    async def stop_server(self, server_id: str) -> bool:
        """停止MCP服务器"""
        server = self.servers.get(server_id)
        process = self.processes.get(server_id)
        
        if not server:
            logger.error(f"无法停止不存在的MCP服务器: {server_id}")
            return False
        
        if not process or server.status != ServerStatus.RUNNING:
            logger.warning(f"MCP服务器 {server_id} 未运行")
            server.status = ServerStatus.STOPPED
            return True
        
        try:
            logger.info(f"正在停止MCP服务器 {server_id}")
            
            # 发送终止信号
            if sys.platform == "win32":
                process.terminate()
            else:
                process.send_signal(signal.SIGTERM)
            
            # 等待进程退出（最多等待5秒）
            try:
                await asyncio.wait_for(asyncio.create_subprocess_shell(f"waitfor /t 5 anykey 2>nul"), timeout=5)
            except asyncio.TimeoutError:
                # 如果超时，强制终止进程
                process.kill()
            
            # 更新服务器状态
            server.status = ServerStatus.STOPPED
            server.error_message = ""
            
            # 清除进程引用
            self.processes.pop(server_id, None)
            
            logger.info(f"MCP服务器 {server_id} 已成功停止")
            return True
            
        except Exception as e:
            logger.opt(exception=e).error(f"停止MCP服务器 {server_id} 时发生错误")
            # 尝试强制终止进程
            try:
                if process.poll() is None:
                    process.kill()
                    self.processes.pop(server_id, None)
            except:
                pass
            
            server.status = ServerStatus.ERROR
            server.error_message = str(e)
            return False
    
    async def get_server_tools(self, server_id: str) -> Optional[List[MCPTool]]:
        """获取MCP服务器提供的工具列表"""
        server = self.servers.get(server_id)
        if not server:
            logger.error(f"无法获取不存在的MCP服务器的工具列表: {server_id}")
            return None
        
        # 如果工具已缓存且服务器正在运行，直接返回缓存
        if server_id in self.tools_cache and server.status == ServerStatus.RUNNING:
            return self.tools_cache[server_id]
        
        # 如果服务器未运行，无法获取工具
        if server.status != ServerStatus.RUNNING:
            logger.warning(f"MCP服务器 {server_id} 未运行，无法获取工具列表")
            return []
        
        # 实现获取工具列表的逻辑
        # 这里应该实现与MCP服务器通信，获取工具列表的代码
        # 由于实现细节可能因连接类型而异，这里暂时返回空列表
        # TODO: 实现具体的工具列表获取逻辑
        
        # 假设我们获取到了工具列表
        mock_tools = [
            MCPTool(
                name="tool1",
                description="示例工具1",
                parameters={
                    "type": "object",
                    "properties": {
                        "param1": {"type": "string", "description": "参数1"},
                        "param2": {"type": "integer", "description": "参数2"}
                    },
                    "required": ["param1"]
                }
            ),
            MCPTool(
                name="tool2",
                description="示例工具2",
                parameters={
                    "type": "object",
                    "properties": {
                        "param1": {"type": "string", "description": "参数1"}
                    },
                    "required": ["param1"]
                }
            )
        ]
        
        # 缓存工具列表
        self.tools_cache[server_id] = mock_tools
        return mock_tools
    
    async def shutdown(self):
        """关闭所有MCP服务器并清理资源"""
        logger.info("正在关闭所有MCP服务器...")
        
        # 创建关闭任务列表
        shutdown_tasks = []
        for server_id, server in list(self.servers.items()):
            if server.status == ServerStatus.RUNNING:
                shutdown_tasks.append(self.stop_server(server_id))
        
        # 等待所有关闭任务完成
        if shutdown_tasks:
            await asyncio.gather(*shutdown_tasks)
        
        logger.info("所有MCP服务器已关闭") 