#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from kirara_ai.mcp.models import MCPServer, MCPTool


class MCPServerList(BaseModel):
    """MCP服务器列表"""
    servers: List[MCPServer]


class MCPServerListResponse(BaseModel):
    """MCP服务器列表响应"""
    success: bool = True
    message: str = "成功获取MCP服务器列表"
    data: MCPServerList


class MCPServerResponse(BaseModel):
    """MCP服务器详情响应"""
    success: bool = True
    message: str = "成功获取MCP服务器详情"
    data: MCPServer


class MCPToolListResponse(BaseModel):
    """MCP服务器工具列表响应"""
    success: bool = True
    message: str = "成功获取MCP服务器工具列表"
    data: List[MCPTool]


class MCPStatisticsResponse(BaseModel):
    """MCP服务器统计信息响应"""
    success: bool = True
    message: str = "成功获取MCP服务器统计信息"
    data: Dict[str, int]


class MCPServerCreateRequest(BaseModel):
    """创建MCP服务器请求"""
    id: str
    description: Optional[str] = None
    command: str
    args: str
    connection_type: str


class MCPServerUpdateRequest(BaseModel):
    """更新MCP服务器请求"""
    description: Optional[str] = None
    command: Optional[str] = None
    args: Optional[str] = None
    connection_type: Optional[str] = None


class MessageResponse(BaseModel):
    """通用消息响应"""
    success: bool = True
    message: str 