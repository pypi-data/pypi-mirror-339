from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class TeamMember(BaseModel):
    id: str
    name: str
    email: str
    role: str  # scrum_master, product_owner, team_member
    department: Optional[str] = None

class Department(BaseModel):
    id: str
    name: str
    manager_id: Optional[str] = None
    description: Optional[str] = None

class Scrum(BaseModel):
    id: str
    name: str
    department_id: str
    description: Optional[str] = None
    team_members: List[TeamMember] = Field(default_factory=list)
    active_sprint_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    def add_team_member(self, member: TeamMember) -> None:
        """Add a team member to the scrum team."""
        if not any(m.id == member.id for m in self.team_members):
            self.team_members.append(member)
            self.updated_at = datetime.utcnow()
    
    def remove_team_member(self, member_id: str) -> None:
        """Remove a team member from the scrum team."""
        self.team_members = [m for m in self.team_members if m.id != member_id]
        self.updated_at = datetime.utcnow()
    
    def get_team_member(self, member_id: str) -> Optional[TeamMember]:
        """Get a team member by their ID."""
        return next((m for m in self.team_members if m.id == member_id), None)
    
    def set_active_sprint(self, sprint_id: Optional[str]) -> None:
        """Set the active sprint for this scrum."""
        self.active_sprint_id = sprint_id
        self.updated_at = datetime.utcnow()
    
    def get_team_members_by_role(self, role: str) -> List[TeamMember]:
        """Get all team members with a specific role."""
        return [m for m in self.team_members if m.role == role] 