#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter
from .routes import router as mcp_router

router = APIRouter()
router.include_router(mcp_router, prefix="/mcp", tags=["MCP服务器管理"]) 