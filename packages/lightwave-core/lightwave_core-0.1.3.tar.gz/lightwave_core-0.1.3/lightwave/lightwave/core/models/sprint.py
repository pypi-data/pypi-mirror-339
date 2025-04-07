from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

class Sprint(BaseModel):
    id: str
    name: str
    scrum_id: str
    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(days=14))
    goal: Optional[str] = None
    status: str = "planned"  # planned, active, completed, cancelled
    task_ids: List[int] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    def is_active(self) -> bool:
        """Check if sprint is currently active."""
        now = datetime.utcnow()
        return (
            self.status == "active" and 
            self.start_date <= now <= self.end_date
        )
    
    def add_task(self, task_id: int) -> None:
        """Add a task to the sprint."""
        if task_id not in self.task_ids:
            self.task_ids.append(task_id)
            self.updated_at = datetime.utcnow()
    
    def remove_task(self, task_id: int) -> None:
        """Remove a task from the sprint."""
        if task_id in self.task_ids:
            self.task_ids.remove(task_id)
            self.updated_at = datetime.utcnow()
    
    def update_status(self, new_status: str) -> None:
        """Update sprint status."""
        valid_statuses = {"planned", "active", "completed", "cancelled"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
        
        self.status = new_status
        self.updated_at = datetime.utcnow()
        
        # Auto-update dates for certain status changes
        if new_status == "active" and self.start_date > datetime.utcnow():
            self.start_date = datetime.utcnow()
        elif new_status == "completed":
            self.end_date = datetime.utcnow() 