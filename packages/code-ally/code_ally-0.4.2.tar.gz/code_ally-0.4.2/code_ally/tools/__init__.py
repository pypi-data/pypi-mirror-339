"""Tool implementations for the Code Ally agent.

This package provides the tools that the agent can use to interact with
the system, such as file operations, shell commands, and more.
"""

# Base classes and registry
from .base import BaseTool

# Core tools
from .bash import BashTool
from .edit import FileEditTool
from .glob import GlobTool
from .grep import GrepTool
from .read import FileReadTool
from .registry import ToolRegistry, register_tool
from .write import FileWriteTool
from .code import CodeStructureAnalyzerTool
from .batch import BatchOperationTool
from .directory import DirectoryTool
from .refactor import RefactorTool
from .plan import TaskPlanTool

# Public API
__all__ = [
    # Base classes and infrastructure
    "BaseTool",
    "ToolRegistry",
    "register_tool",
    # Core tools
    "BashTool",
    "FileReadTool",
    "FileWriteTool",
    "FileEditTool",
    "GlobTool",
    "GrepTool",
    "CodeStructureAnalyzerTool",
    "BatchOperationTool",
    "DirectoryTool",
    "RefactorTool",
    "TaskPlanTool",
]

# Create registry instance to ensure all tools are registered
registry = ToolRegistry()
