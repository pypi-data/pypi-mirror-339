class WorkflowError(Exception):
    """A workflow execution error with clean formatting.
    
    This class provides a cleaner way to handle workflow errors by:
    1. Preserving the original exception
    2. Providing a clean error message
    3. Adding context about the task that failed
    4. Simplifying display of nested exceptions
    """
    
    def __init__(self, message: str, task_name: str = None, original_error: Exception = None):
        self.task_name = task_name
        self.original_error = original_error
        
        # Create a clean error message
        error_parts = []
        if task_name:
            error_parts.append(f"Task '{task_name}'")
        
        error_parts.append(message)
        
        if original_error:
            # Include original error message without full type name
            error_type = type(original_error).__name__
            error_msg = str(original_error).split(":", 1)[-1].strip()
            if error_msg:
                error_parts.append(f"{error_type}: {error_msg}")
            else:
                error_parts.append(f"{error_type}")
        
        super().__init__(" - ".join(error_parts))

class TaskValidationError(WorkflowError):
    """Raised when task validation fails"""
    pass

class WorkflowValidationError(WorkflowError):
    """Raised when workflow validation fails"""
    pass

class TaskConfigurationError(WorkflowError):
    """Raised when task configuration is invalid"""
    pass

class ModelValidationError(WorkflowError):
    """Raised when input or output model validation fails"""
    pass

class TaskExecutionError(WorkflowError):
    """Raised when task execution fails"""
    pass

class DependencyError(WorkflowError):
    """Raised when there's an issue with task dependencies"""
    pass

class ContextError(WorkflowError):
    """Raised when there's an issue with the context"""
    pass

def format_error(base_message: str, task_name: str = None, details: str = None) -> str:
    """
    Format error messages consistently.
    
    Args:
        base_message: The main error message
        task_name: Optional task name for context
        details: Optional additional error details
        
    Returns:
        Formatted error message
    """
    parts = []
    
    if task_name:
        parts.append(f"Task '{task_name}':")
    
    parts.append(base_message)
    
    if details:
        parts.append(f"- {details}")
    
    return " ".join(parts)