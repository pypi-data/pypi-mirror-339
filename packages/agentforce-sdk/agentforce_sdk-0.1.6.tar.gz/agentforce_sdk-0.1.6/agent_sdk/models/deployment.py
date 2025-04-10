"""Deployment models."""
from typing import Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class Deployment(BaseModel):
    """Deployment class for tracking agent deployments."""
    
    id: str = Field(..., description="Deployment ID")
    agent_name: str = Field(..., description="Name of the deployed agent")
    status: str = Field("Pending", description="Status of the deployment")
    created_at: datetime = Field(default_factory=datetime.now, description="When the deployment was created")
    completed_at: Optional[datetime] = Field(None, description="When the deployment was completed")
    success: bool = Field(False, description="Whether the deployment was successful")
    error_message: Optional[str] = Field(None, description="Error message if deployment failed")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        """Pydantic config."""
        
        extra = "allow"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return self.model_dump(exclude_none=True)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Deployment':
        """Create from dictionary."""
        return cls.model_validate(data) 