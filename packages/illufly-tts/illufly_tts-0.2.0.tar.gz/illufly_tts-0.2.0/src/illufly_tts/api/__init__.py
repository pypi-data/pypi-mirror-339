"""
TTS FastAPI接口模块 - 轻量级，可以集成到其他应用
"""

# 导出主要的挂载函数
from .endpoints import mount_tts_service
from .mcp_server import create_mcp_server

__all__ = [
    'mount_tts_service',
    'create_mcp_server',
]