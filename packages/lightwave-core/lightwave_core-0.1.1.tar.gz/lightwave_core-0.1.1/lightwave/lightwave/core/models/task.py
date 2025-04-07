from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class SubTask(BaseModel):
    id: str  # Format: "parent_id.subtask_number"
    title: str
    description: str
    status: str = "pending"
    details: Optional[str] = None

class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str = "pending"
    dependencies: List[int] = Field(default_factory=list)
    priority: str = "medium"
    details: Optional[str] = None
    test_strategy: Optional[str] = None
    subtasks: List[SubTask] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def is_blocked(self, completed_tasks: List[int]) -> bool:
        """Check if task is blocked by dependencies."""
        return any(dep not in completed_tasks for dep in self.dependencies)
    
    def add_subtask(self, title: str, description: str, details: Optional[str] = None) -> SubTask:
        """Add a new subtask to this task."""
        subtask_id = f"{self.id}.{len(self.subtasks) + 1}"
        subtask = SubTask(
            id=subtask_id,
            title=title,
            description=description,
            details=details
        )
        self.subtasks.append(subtask)
        return subtask
    
    def get_subtask(self, subtask_id: str) -> Optional[SubTask]:
        """Get a subtask by its ID."""
        return next((st for st in self.subtasks if st.id == subtask_id), None)
    
    def update_status(self, new_status: str) -> None:
        """Update task status and updated_at timestamp."""
        self.status = new_status
        self.updated_at = datetime.utcnow()
    
    def is_complete(self) -> bool:
        """Check if task and all subtasks are complete."""
        if self.status != "done":
            return False
        return all(st.status == "done" for st in self.subtasks) 