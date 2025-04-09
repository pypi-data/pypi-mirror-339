from typing import Set, AsyncIterator, List, Dict, Tuple, Any
import asyncio
import logging
from ..node import Node
from ...constants import TaskStatus, WorkflowEventType
from ...context import Context
from ...exceptions import WorkflowError
from ..graph.dependency import DependencyManager
from .events import WorkflowEvent
from .progress import Progress

class WorkflowExecutor:
    """Handles the execution of tasks in a workflow."""
    
    def __init__(self, 
                 nodes: List[Node], 
                 context: Context, 
                 progress: Progress, 
                 dependency_manager: DependencyManager,
                 logger: logging.Logger,
                 task_timeout: int = 120,
                 max_timeout_retries: int = 3,
                 log_full_traceback: bool = False):
        self.nodes = nodes
        self.context = context
        self.progress = progress
        self.dependency_manager = dependency_manager
        self.logger = logger
        self.task_timeout = task_timeout
        self.max_timeout_retries = max_timeout_retries
        self.log_full_traceback = log_full_traceback
    
    def _get_ready_tasks(self, completed_tasks: Set[str]) -> Set[str]:
        """Get all tasks that are ready to be executed based on dependencies."""
        ready_tasks = set()
        
        for node in self.nodes:
            task_name = node.task.name
            
            # Skip tasks that are already completed
            if task_name in completed_tasks:
                continue
                
            # Check if all dependencies are satisfied
            dependencies = self.dependency_manager.get_dependencies(task_name)
            if all(dep in completed_tasks for dep in dependencies):
                ready_tasks.add(task_name)
                
        return ready_tasks
    
    async def _execute_task(self, task_name: str) -> AsyncIterator[WorkflowEvent]:
        """Execute a single task and update its status."""
        node = next(t for t in self.nodes if t.task.name == task_name)
        
        self.logger.info(f"Starting task: {task_name}")
        self.progress.update_task_status(task_name, TaskStatus.RUNNING)           
        try:
            args = {
                name: mapping.resolve(self.context)
                for name, mapping in node.argument_mappings.items()
            }
            
            self.logger.debug(f"Task {task_name} arguments resolved: {args}")
            final_result = None
            
            # Execute the task and handle its result
            result = await node.task(**args)
            
            # Check if result should emit progress events
            is_generator_result = self._is_async_generator(node.task.processor_function)
            
            # Handle result (either async iterator or direct result)
            if hasattr(result, '__aiter__'):
                async for data in result:
                    final_result = data
                    
                    if is_generator_result and self._is_progress_event(node, data):
                        yield WorkflowEvent(
                            WorkflowEventType.TASK_PROGRESS,
                            task_name=task_name,
                            task_data=data
                        )
            else:
                # Direct result with no progress events
                final_result = result
            
            # Store the final result
            if final_result is not None:
                node.result_mapping.store(self.context, final_result)
            
            self.logger.info(f"Task completed successfully: {task_name}")
            self.progress.update_task_status(task_name, TaskStatus.COMPLETED)
        except Exception as e:
            self.logger.error(f"Task failed: {task_name}", exc_info=self.log_full_traceback)
            self.progress.update_task_status(task_name, TaskStatus.FAILED)
            # Use WorkflowError for cleaner error reporting
            raise WorkflowError("failed", task_name=task_name, original_error=e)
    
    def _is_async_generator(self, func) -> bool:
        """Check if a function is expected to return an async iterator."""
        has_annotations = hasattr(func, '__annotations__')
        if not has_annotations:
            return False
            
        has_return = 'return' in func.__annotations__
        if not has_return:
            return False
            
        annotation = str(func.__annotations__['return'])
        has_async_iterator = 'AsyncIterator' in annotation
        has_async_generator = 'AsyncGenerator' in annotation
        return has_async_iterator or has_async_generator
    
    def _is_progress_event(self, node: Node, data: Any) -> bool:
        """Determine if data is a progress event rather than a final result."""
        if node.task.progress_model and isinstance(data, node.task.progress_model):
            return True
        if not isinstance(data, node.task.output_model):
            return True
        return False
    
    async def _execute_and_forward_events(self, task_name: str, queue: asyncio.Queue) -> None:
        """Execute task and forward its events to the queue."""
        try:
            async for event in self._execute_task(task_name):
                await queue.put(("event", event))
            # Signal task completion
            await queue.put(("done", None))
        except Exception as e:
            # Signal task failure with the exception
            self.logger.error(f"Task execution failed: {task_name}", exc_info=self.log_full_traceback)
            await queue.put(("error", e))
    
    async def _process_task_events(self, tasks_in_progress: Set[str], 
                                 task_to_future: Dict[str, Tuple[asyncio.Task, asyncio.Queue]],
                                 timeout_counter: Dict[str, int],
                                 completed_tasks: Set[str]) -> List[WorkflowEvent]:
        """Process events from all running tasks with timeout handling."""
        events = []
        
        if not tasks_in_progress:
            return events
            
        # Create a map of wait tasks to their original tasks
        event_wait_tasks = []
        task_to_wait_task = {}
        
        for task_name in list(tasks_in_progress):
            _, queue = task_to_future[task_name]
            wait_task = asyncio.create_task(queue.get())
            event_wait_tasks.append(wait_task)
            task_to_wait_task[wait_task] = task_name
        
        # Wait for any task to produce an event
        done, pending = await asyncio.wait(
            event_wait_tasks, 
            return_when=asyncio.FIRST_COMPLETED,
            timeout=self.task_timeout
        )
        
        # Handle timeout if no tasks completed
        if not done:
            handled = await self._handle_timeout(tasks_in_progress, timeout_counter, task_to_future)
            for task in pending:
                task.cancel()
            if handled:
                return events  # Return early if timeout was handled
            
        # Reset timeout counter for tasks that made progress
        for wait_task in done:
            task_name = task_to_wait_task[wait_task]
            timeout_counter[task_name] = 0
        
        # Cancel pending wait tasks
        for task in pending:
            task.cancel()
        
        # Process events from completed tasks
        for wait_task in done:
            event_type, event_data = await wait_task
            task_name = task_to_wait_task[wait_task]
            
            if event_type == "event":
                events.append(event_data)
            elif event_type == "done":
                completed_tasks.add(task_name)
                tasks_in_progress.remove(task_name)
                del task_to_future[task_name]
                events.append(WorkflowEvent(WorkflowEventType.TASK_COMPLETED, task_name=task_name))
                self.logger.debug(f"Task completed and removed from in-progress: {task_name}")
            elif event_type == "error":
                completed_tasks.add(task_name)
                tasks_in_progress.remove(task_name)
                del task_to_future[task_name]
                
                if not isinstance(event_data, WorkflowError):
                    raise WorkflowError("failed", task_name=task_name, original_error=event_data)
                else:
                    raise event_data
        
        return events
    
    async def _handle_timeout(self, tasks_in_progress: Set[str], 
                             timeout_counter: Dict[str, int], 
                             task_to_future: Dict[str, Tuple[asyncio.Task, asyncio.Queue]]) -> bool:
        """Handle tasks that have timed out. Returns True if workflow should terminate."""
        self.logger.warning("No events received from tasks within timeout period. Tasks may be stuck.")
        
        timed_out_tasks = list(tasks_in_progress)
        self.logger.warning(f"Tasks that may be stuck: {timed_out_tasks}")
        
        # Increment timeout counters for all in-progress tasks
        for task_name in timed_out_tasks:
            timeout_counter[task_name] += 1
            
            # If a task has timed out too many times, cancel it
            if timeout_counter[task_name] >= self.max_timeout_retries:
                self.logger.error(f"Task {task_name} timed out {self.max_timeout_retries} times. Cancelling.")
                task_future, _ = task_to_future[task_name]
                task_future.cancel()
                
                # Create a specific timeout error
                timeout_error = TimeoutError(f"Task {task_name} timed out after {self.max_timeout_retries} retries")
                
                # Fail the workflow due to the task timeout
                raise RuntimeError(f"Workflow execution failed: Task {task_name} timed out") from timeout_error
        
        return False

    async def execute(self) -> AsyncIterator[WorkflowEvent]:
        """
        Execute tasks in parallel when possible based on their dependencies.
        Yields workflow events during execution.
        """
        self.logger.info("Starting workflow execution")
        
        try:
            completed_tasks: Set[str] = set()
            tasks_in_progress: Set[str] = set()
            task_to_future: Dict[str, Tuple[asyncio.Task, asyncio.Queue]] = {}
            timeout_counter: Dict[str, int] = {}
            
            while len(completed_tasks) < len(self.nodes):
                # Find tasks ready to execute
                ready_tasks = self._get_ready_tasks(completed_tasks) - tasks_in_progress
                
                # Check for deadlock
                if not ready_tasks and not tasks_in_progress:
                    remaining = {t.task.name for t in self.nodes} - completed_tasks
                    msg = f"Unable to make progress. Tasks stuck: {remaining}"
                    self.logger.error(msg)
                    raise RuntimeError(msg)
                
                # Start new tasks
                if ready_tasks:
                    self.logger.debug(f"Starting new tasks: {ready_tasks}")
                    for task_name in ready_tasks:
                        event_queue = asyncio.Queue()
                        task_future = asyncio.create_task(self._execute_and_forward_events(task_name, event_queue))
                        task_to_future[task_name] = (task_future, event_queue)
                        tasks_in_progress.add(task_name)
                        timeout_counter[task_name] = 0
                        yield WorkflowEvent(WorkflowEventType.TASK_STARTED, task_name=task_name)
                
                # Process events from running tasks
                events = await self._process_task_events(
                    tasks_in_progress, task_to_future, timeout_counter, completed_tasks
                )
                
                # Forward events
                for event in events:
                    yield event
            
            self.logger.info("Workflow execution completed successfully")
            
        except Exception:
            self.logger.error("Workflow execution failed", exc_info=True)
            raise