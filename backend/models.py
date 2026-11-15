"""
Lucen Data Models - Graph Node & Edge Definitions for Agent Context Layer
"""
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class MCPServerNode(BaseModel):
    id: str
    name: str
    description: str
    version: str = "1.0.0"
    transport: str = "stdio"
    status: str = "active"

