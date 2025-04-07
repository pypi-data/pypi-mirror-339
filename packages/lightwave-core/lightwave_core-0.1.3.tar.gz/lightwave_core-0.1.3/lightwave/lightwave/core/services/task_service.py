from pathlib import Path
from typing import List, Optional, Dict, Any
from ..models.task import Task, SubTask
from ..exceptions import TaskNotFoundError, TaskValidationError, CircularDependencyError
from .base import BaseService

class TaskService(BaseService):
    """Service for managing tasks."""
    
    def __init__(self, tasks_file: Optional[str] = None, config_dir: Optional[str] = None):
        """Initialize the task service."""
        super().__init__(config_dir)
        self.tasks_file = Path(tasks_file) if tasks_file else self.get_data_file_path("tasks.json")
    
    def list_tasks(self, status_filter: Optional[str] = None) -> List[Task]:
        """List all tasks, optionally filtered by status."""
        data = self.read_json_file(self.tasks_file)
        tasks = [Task(**task_data) for task_data in data.get("tasks", [])]
        
        if status_filter:
            tasks = [t for t in tasks if t.status == status_filter]
        
        return tasks
    
    def get_task(self, task_id: int) -> Task:
        """Get a task by ID."""
        tasks = self.list_tasks()
        task = next((t for t in tasks if t.id == task_id), None)
        if not task:
            raise TaskNotFoundError(f"Task {task_id} not found")
        return task
    
    def create_task(self, task_data: Dict[str, Any]) -> Task:
        """Create a new task."""
        data = self.read_json_file(self.tasks_file)
        tasks = data.get("tasks", [])
        
        # Generate new task ID
        task_id = max([t.get("id", 0) for t in tasks], default=0) + 1
        task_data["id"] = task_id
        
        # Create and validate task
        task = Task(**task_data)
        self._validate_task_dependencies(task, tasks)
        
        # Save task
        tasks.append(task.dict())
        self.write_json_file(self.tasks_file, {"tasks": tasks})
        
        return task
    
    def update_task(self, task_id: int, task_data: Dict[str, Any]) -> Task:
        """Update an existing task."""
        data = self.read_json_file(self.tasks_file)
        tasks = data.get("tasks", [])
        
        # Find and update task
        task_index = next((i for i, t in enumerate(tasks) if t.get("id") == task_id), None)
        if task_index is None:
            raise TaskNotFoundError(f"Task {task_id} not found")
        
        # Preserve ID and merge updates
        task_data["id"] = task_id
        updated_task = Task(**task_data)
        self._validate_task_dependencies(updated_task, tasks)
        
        tasks[task_index] = updated_task.dict()
        self.write_json_file(self.tasks_file, {"tasks": tasks})
        
        return updated_task
    
    def delete_task(self, task_id: int) -> None:
        """Delete a task."""
        data = self.read_json_file(self.tasks_file)
        tasks = data.get("tasks", [])
        
        # Remove task
        tasks = [t for t in tasks if t.get("id") != task_id]
        self.write_json_file(self.tasks_file, {"tasks": tasks})
    
    def expand_task(self, task_id: int, num_subtasks: int, context_prompt: Optional[str] = None) -> Task:
        """Expand a task with subtasks."""
        task = self.get_task(task_id)
        
        # Clear existing subtasks if any
        task.subtasks = []
        
        # Add new subtasks (in a real implementation, this might use AI to generate meaningful subtasks)
        for i in range(num_subtasks):
            task.add_subtask(
                title=f"Subtask {i+1}",
                description=f"Auto-generated subtask {i+1}" + (f" with context: {context_prompt}" if context_prompt else ""),
                details=None
            )
        
        # Save updated task
        return self.update_task(task_id, task.dict())
    
    def _validate_task_dependencies(self, task: Task, all_tasks: List[Dict[str, Any]]) -> None:
        """Validate task dependencies and check for circular dependencies."""
        task_ids = {t.get("id") for t in all_tasks}
        
        # Check if all dependencies exist
        for dep_id in task.dependencies:
            if dep_id not in task_ids:
                raise TaskValidationError(f"Dependency task {dep_id} does not exist")
            if dep_id == task.id:
                raise TaskValidationError("Task cannot depend on itself")
        
        # Check for circular dependencies
        visited = set()
        path = []
        
        def check_circular(task_id: int) -> None:
            if task_id in path:
                cycle = path[path.index(task_id):] + [task_id]
                raise CircularDependencyError(f"Circular dependency detected: {' -> '.join(map(str, cycle))}")
            
            if task_id in visited:
                return
            
            visited.add(task_id)
            path.append(task_id)
            
            task_data = next((t for t in all_tasks if t.get("id") == task_id), None)
            if task_data:
                for dep_id in task_data.get("dependencies", []):
                    check_circular(dep_id)
            
            path.pop()
        
        check_circular(task.id) 