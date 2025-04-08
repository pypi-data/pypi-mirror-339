from dataclasses import dataclass
from typing import Optional, Any
from ...constants import WorkflowEventType

@dataclass
class WorkflowEvent:
    """Event emitted during workflow execution."""
    type: WorkflowEventType
    task_name: Optional[str] = None
    task_data: Optional[Any] = None
    error: Optional[Exception] = None