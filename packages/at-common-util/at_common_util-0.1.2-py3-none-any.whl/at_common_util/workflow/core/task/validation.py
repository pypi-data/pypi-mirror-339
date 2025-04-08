from typing import Type, Callable, Any, Optional, Union, get_origin, get_args, Dict
from inspect import signature, isasyncgenfunction, iscoroutinefunction
from pydantic import BaseModel
from typing import AsyncIterator
from collections.abc import AsyncIterator as AsyncIteratorABC
import typing

from ..exceptions import (
    TaskConfigurationError, 
    ModelValidationError, 
    TaskValidationError,
    format_error
)

from ...utils.mappings import ArgumentMapping
from .definition import TaskDefinition

def validate_task_configuration(
    name: str,
    input_model: Optional[Type[BaseModel]],
    output_model: Optional[Type[BaseModel]],
    progress_model: Optional[Type[BaseModel]],
    processor_function: Optional[Callable]
) -> None:
    """
    Validate that task configuration meets requirements.
    
    Args:
        name: Task name
        input_model: Optional Pydantic model for input validation (can be None for no-input tasks)
        output_model: Optional Pydantic model for output validation (can be None for no-output tasks)
        progress_model: Pydantic model for progress events
        processor_function: Task execution function
        
    Raises:
        TaskConfigurationError: If configuration is invalid
        TypeError: If function signature is invalid
    """
    # Validate name
    if not name:
        raise TaskConfigurationError("Task name cannot be empty")
    
    # Validate input model (if provided)
    if input_model is not None and (not isinstance(input_model, type) or not issubclass(input_model, BaseModel)):
        raise TypeError(format_error(f"Input model must be a Pydantic BaseModel class, got {type(input_model).__name__}", task_name=name))
        
    # Validate output model (if provided)
    if output_model is not None and (not isinstance(output_model, type) or not issubclass(output_model, BaseModel)):
        raise TypeError(format_error(f"Output model must be a Pydantic BaseModel class, got {type(output_model).__name__}", task_name=name))
    
    # Progress model is optional but must be a BaseModel if provided
    if progress_model is not None and (not isinstance(progress_model, type) 
                                     or not issubclass(progress_model, BaseModel)):
        raise TypeError(format_error(f"Progress model must be a Pydantic BaseModel class, got {type(progress_model).__name__}", task_name=name))
    
    # Validate execute function
    if processor_function is None:
        raise TaskConfigurationError(format_error("Processor function cannot be None", task_name=name))
    if not callable(processor_function):
        raise TypeError(format_error(f"Processor function must be callable, got {type(processor_function).__name__}", task_name=name))
        
    # Must be an async function or async generator
    if not (iscoroutinefunction(processor_function) or isasyncgenfunction(processor_function)):
        raise TypeError(format_error("Processor function must be an async function (using 'async def')", task_name=name))
    
    # Validate function signature
    sig = signature(processor_function)
    params = list(sig.parameters.values())
    
    # Parameter count based on whether input model is defined
    if input_model is None:
        # For no-input tasks, processor function can have zero or one parameter
        if len(params) > 1:
            raise TypeError(format_error(
                f"Processor function for no-input task must take zero or one parameter, got {len(params)}", 
                task_name=name
            ))
        
        # If it has a parameter, it should be named 'input'
        if len(params) == 1 and params[0].name != 'input':
            raise TypeError(format_error(
                f"Processor function parameter must be named 'input', got '{params[0].name}'", 
                task_name=name
            ))
    else:
        # For tasks with input model, must have exactly one parameter
        if len(params) != 1:
            raise TypeError(format_error(
                f"Processor function for task with input model must take exactly one parameter, got {len(params)}", 
                task_name=name
            ))
        
        # The parameter should be named 'input'
        if params[0].name != 'input':
            raise TypeError(format_error(
                f"Processor function parameter must be named 'input', got '{params[0].name}'", 
                task_name=name
            ))
        
    # Skip return type validation if no output model is defined
    if output_model is None:
        return
        
    # Must have a return type annotation
    if not hasattr(processor_function, '__annotations__') or 'return' not in processor_function.__annotations__:
        raise TypeError(format_error("Processor function must have a return type annotation", task_name=name))
        
    # Extract the return type annotation
    return_annotation = processor_function.__annotations__['return']
    
    # Validate return type annotation
    is_valid = False
    expected_types = []
    
    # Option 1: Direct output value
    direct_output_type = f"Awaitable[{output_model.__name__}]"
    expected_types.append(direct_output_type)
    
    if hasattr(typing, 'get_origin') and hasattr(typing, 'get_args'):  # Python 3.8+
        if typing.get_origin(return_annotation) == typing.Awaitable:
            args = typing.get_args(return_annotation)
            if len(args) == 1 and args[0] == output_model:
                is_valid = True
    
    # Option 2: Async generator of output model (without Union)
    generator_output_type = f"AsyncIterator[{output_model.__name__}]"
    expected_types.append(generator_output_type)
    
    # Option 3: Async generator of Union[ProgressModel, OutputModel]
    union_output_type = None
    if progress_model:
        union_output_type = f"AsyncIterator[Union[{progress_model.__name__}, {output_model.__name__}]]"
        expected_types.append(union_output_type)
    
    # Check for AsyncIterator types
    if hasattr(typing, 'get_origin') and hasattr(typing, 'get_args'):
        if typing.get_origin(return_annotation) == typing.AsyncIterator:
            args = typing.get_args(return_annotation)
            if len(args) == 1:
                # Either AsyncIterator[OutputModel]
                if args[0] == output_model:
                    is_valid = True
                # Or AsyncIterator[Union[ProgressModel, OutputModel]]
                elif progress_model and typing.get_origin(args[0]) == typing.Union:
                    union_args = typing.get_args(args[0])
                    if len(union_args) == 2 and progress_model in union_args and output_model in union_args:
                        is_valid = True
    
    # Handle string representation of AsyncIterator
    str_return_annotation = str(return_annotation).strip()
    if (str_return_annotation.startswith("typing.AsyncIterator[") or 
        str_return_annotation.startswith("AsyncIterator[")) and output_model.__name__ in str_return_annotation:
        is_valid = True
    
    # Option 4: Direct result (for synchronous or simple functions)
    if return_annotation == output_model:
        is_valid = True
        expected_types.append(output_model.__name__)
    
    if not is_valid:
        raise TypeError(
            format_error(
                f"Processor function must return one of: \n"
                f"  - {direct_output_type}\n"
                f"  - {generator_output_type}\n" + 
                (f"  - {union_output_type}\n" if union_output_type else "") +
                f"  - {output_model.__name__}\n" +
                f"Got: {return_annotation}",
                task_name=name
            )
        )

def validate_input(name: str, input_model: Optional[Type[BaseModel]], **kwargs) -> Any:
    """
    Validate input arguments against input_model.
    If input_model is None, returns an empty dict as the input.
    
    Args:
        name: Task name
        input_model: Optional Pydantic model for input validation
        **kwargs: Input arguments
        
    Returns:
        Validated input model instance or empty dict if no model
        
    Raises:
        ModelValidationError: If input validation fails
    """
    if not input_model:
        return {}  # Return empty dict for no-input tasks
        
    try:
        return input_model(**kwargs)
    except Exception as e:
        raise ModelValidationError(format_error("Input validation failed", task_name=name, details=str(e))) from e

def validate_output(
    name: str,
    output: Any, 
    output_model: Optional[Type[BaseModel]], 
    progress_model: Optional[Type[BaseModel]] = None,
    is_progress: bool = False
) -> Any:
    """
    Validate output against output_model or progress_model.
    If output_model is None, the output is returned as-is without validation.
    
    Args:
        name: Task name
        output: Task output or progress event
        output_model: Optional Pydantic model for output validation
        progress_model: Optional Pydantic model for progress events
        is_progress: Whether validating a progress event or final result
        
    Returns:
        Validated output model instance or raw output if no model
        
    Raises:
        ModelValidationError: If output validation fails
    """
    # If no output model is defined, return as-is without validation
    if not output_model:
        return output
        
    # If instance is already a valid model instance, return it directly
    if isinstance(output, output_model):
        return output
    
    if progress_model and isinstance(output, progress_model):
        return output
    
    # Determine which model to use for validation based on output type and context
    # If we know this is a progress event but output is a final model, that's an error
    if is_progress and progress_model and not isinstance(output, progress_model) and isinstance(output, output_model):
        raise ModelValidationError(format_error(
            f"Expected progress event but got final output type {type(output).__name__}", 
            task_name=name
        ))
    
    # Handle final output
    if isinstance(output, output_model) or (not is_progress):
        # Final output or not explicitly a progress event
        try:
            return output_model(**output)
        except Exception as e:
            raise ModelValidationError(format_error(
                "Output validation failed", 
                task_name=name, 
                details=str(e)
            )) from e
    
    # Handle progress event
    if not progress_model:
        raise ModelValidationError(format_error(
            "No progress model defined but received progress event", 
            task_name=name
        ))
        
    try:
        return progress_model(**output)
    except Exception as e:
        raise ModelValidationError(format_error(
            "Progress event validation failed", 
            task_name=name,
            details=str(e)
        )) from e

def validate_arguments(task_name: str, input_model: Optional[Type[BaseModel]], argument_mappings: Dict[str, ArgumentMapping]) -> None:
    """
    Validate that all required fields in input model are provided in argument mappings.
    If input_model is None, skip validation as no arguments are needed.
    
    Args:
        task_name: Name of the task for error messages
        input_model: Optional Pydantic model class for the task input
        argument_mappings: Mapping of argument names to their sources (constant or context)
        
    Raises:
        TaskConfigurationError: If a required field is missing or argument not in model
    """
    # If no input model, skip validation - no arguments needed
    if not input_model:
        # If there are argument mappings but no input model, that's an error
        if argument_mappings:
            raise TaskConfigurationError(format_error(
                f"Task has {len(argument_mappings)} argument mappings but no input model", 
                task_name=task_name
            ))
        return
        
    # Get required fields from model
    required_fields = set()
    if hasattr(input_model, 'model_fields'):
        # Pydantic V2 approach
        for field_name, field_info in input_model.model_fields.items():
            if field_info.is_required():
                required_fields.add(field_name)
    elif hasattr(input_model, '__fields__'):
        # Pydantic V1 approach (backwards compatibility)
        for field_name, field_info in input_model.__fields__.items():
            if field_info.required:
                required_fields.add(field_name)
    else:
        # Fallback for unknown model type
        for field_name in input_model.__annotations__:
            required_fields.add(field_name)  # Assume all fields are required
    
    # Check that all arguments exist in the model
    for arg_name in argument_mappings:
        if hasattr(input_model, 'model_fields'):
            # Pydantic V2
            if arg_name not in input_model.model_fields:
                raise TaskConfigurationError(
                    format_error(f"Argument '{arg_name}' is not defined in input model", task_name=task_name)
                )
        elif hasattr(input_model, '__fields__'):
            # Pydantic V1
            if arg_name not in input_model.__fields__:
                raise TaskConfigurationError(
                    format_error(f"Argument '{arg_name}' is not defined in input model", task_name=task_name)
                )
        else:
            # Fallback for unknown model type - check annotations
            if arg_name not in input_model.__annotations__:
                raise TaskConfigurationError(
                    format_error(f"Argument '{arg_name}' is not defined in input model", task_name=task_name)
                )
    
    # Check for missing required arguments
    for field_name in required_fields:
        if field_name not in argument_mappings:
            raise TaskConfigurationError(
                format_error(f"Required argument '{field_name}' is missing", task_name=task_name)
            )

class TaskValidator:
    """
    Validates task definitions to ensure they are properly configured before execution.
    
    This class is responsible for checking that a task definition is complete and valid,
    including validating input models, output models, and argument mappings.
    """
    
    @staticmethod
    def validate_task_definition(task_def: TaskDefinition) -> None:
        """
        Validate a task definition to ensure it is complete and valid.
        
        Args:
            task_def: The task definition to validate
            
        Raises:
            TaskConfigurationError: If the task definition is invalid
            TypeError: If input or output models are not valid Pydantic models
        """
        # Check for required components
        # Input model is optional
        
        # Check if this is a special "no_output" case (prefixed with double underscore)
        is_no_output = task_def.result_key and task_def.result_key.startswith(f"__{task_def.name}_no_output")
        
        # Output model is optional for tasks with no_output
        if not is_no_output and not task_def.output_model:
            raise TaskConfigurationError(format_error("Output model must be defined when storing results", task_name=task_def.name))
        
        if not task_def.processor_function:
            raise TaskConfigurationError(format_error("Processor function must be defined", task_name=task_def.name))
        
        if not task_def.result_key and not is_no_output:
            raise TaskConfigurationError(format_error("Output result key must be defined", task_name=task_def.name))
        
        # Validate model types
        if task_def.input_model is not None and not (isinstance(task_def.input_model, type) and issubclass(task_def.input_model, BaseModel)):
            raise TypeError(f"input_model must be a Pydantic BaseModel class, got {type(task_def.input_model).__name__}")
        
        # Validate output_model only if it's defined
        if task_def.output_model and not (isinstance(task_def.output_model, type) and issubclass(task_def.output_model, BaseModel)):
            raise TypeError(f"output_model must be a Pydantic BaseModel class, got {type(task_def.output_model).__name__}")
        
        if task_def.progress_model and not (isinstance(task_def.progress_model, type) and issubclass(task_def.progress_model, BaseModel)):
            raise TypeError(f"progress_model must be a Pydantic BaseModel class, got {type(task_def.progress_model).__name__}")
        
        # Validate arguments match input model fields (if input model exists)
        if task_def.input_model:
            arg_mappings = {name: mapping for name, mapping in task_def.argument_mappings.items()}
            validate_arguments(task_def.name, task_def.input_model, arg_mappings)
    
    @staticmethod
    def validate_context_references(task_def: TaskDefinition) -> None:
        """
        Validate that context references in argument mappings follow the correct format.
        
        Args:
            task_def: The task definition to validate
            
        Raises:
            TaskConfigurationError: If any context reference is invalid
        """
        for arg_name, arg_mapping in task_def.argument_mappings.items():
            if not hasattr(arg_mapping, 'get_context_refs'):
                continue
                
            # Check that context references are properly formatted
            for ref in arg_mapping.get_context_refs():
                if not ref or not isinstance(ref, str):
                    raise TaskConfigurationError(
                        format_error(f"Invalid context reference for argument '{arg_name}'", task_name=task_def.name)
                    ) 