"""
AT Common Workflow - A DAG-based workflow execution engine with typed input/output.

This package provides a framework for defining and executing workflows
with automatic dependency resolution, parallel execution, and progress tracking.
"""

# Core components
from .core.context import Context
from .core.task.processing_task import ProcessingTask
from .core.workflow.base import Workflow
from .core.workflow.builder import WorkflowBuilder

# Constants and types
from .core.constants import WorkflowEventType
from .core.task.base import InputType, OutputType

__version__ = "1.5.0"
__all__ = [
    # Core components
    "Context",
    "ProcessingTask",
    "Workflow",
    "WorkflowBuilder",
    
    # Constants and types
    "WorkflowEventType",
    "InputType", 
    "OutputType"
]