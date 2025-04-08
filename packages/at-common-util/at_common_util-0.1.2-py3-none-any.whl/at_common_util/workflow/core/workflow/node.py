from typing import Dict, Set, Optional
from ..task import ProcessingTask
from ...utils.mappings import ArgumentMapping, ResultMapping
from ..exceptions import WorkflowValidationError, format_error
from ..task.validation import validate_arguments

class Node:
    """Represents a task node in the workflow graph."""
    
    def __init__(
        self,
        task: ProcessingTask,
        argument_mappings: Dict[str, ArgumentMapping],
        result_mapping: ResultMapping
    ) -> None:
        """
        Initialize a workflow node.
        
        Args:
            task: The task to execute
            argument_mappings: Mappings for task arguments
            result_mapping: Mapping for task result
            
        Raises:
            TaskValidationError: If argument validation fails
            WorkflowValidationError: If task or result_mapping is None
        """
        if not task:
            raise WorkflowValidationError(format_error("Task cannot be None"))
        if not result_mapping:
            raise WorkflowValidationError(format_error("Result mapping cannot be None"))
            
        # Validate arguments against the input model
        validate_arguments(task.name, task.input_model, argument_mappings)
        
        self.task = task
        self.argument_mappings = argument_mappings
        self.result_mapping = result_mapping
        self.dependencies: Set[str] = set()
    
    def __repr__(self) -> str:
        """String representation of the node."""
        return f"Node(task={self.task.name}, result_key={self.result_mapping.context_key})"