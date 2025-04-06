#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ConnectionType(str, Enum):
    """MCP服务器连接类型"""
    STANDARD_IO = "standard_io"
    SSE = "sse"


class ServerStatus(str, Enum):
    """MCP服务器状态"""
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"


class MCPServer(BaseModel):
    """MCP服务器模型"""
    id: str
    description: Optional[str] = None
    command: str
    args: str
    connection_type: ConnectionType
    status: ServerStatus = ServerStatus.STOPPED
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    last_used_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "claude-mcp",
                "description": "Claude MCP 服务器",
                "command": "python",
                "args": "-m claude_cli.mcp",
                "connection_type": "standard_io",
                "status": "stopped"
            }
        }


class MCPTool(BaseModel):
    """MCP服务器工具"""
    name: str
    description: str
    parameters: Dict[str, Any] 