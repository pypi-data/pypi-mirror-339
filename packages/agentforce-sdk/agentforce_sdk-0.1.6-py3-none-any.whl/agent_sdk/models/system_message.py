"""System message models."""
from typing import Dict, Optional, Any
from pydantic import BaseModel, Field, model_validator


class SystemMessage(BaseModel):
    """System message for agent."""
    
    name: Optional[str] = Field(None, description="Name of the system message")
    content: Optional[str] = Field(None, description="Content of the system message")
    description: Optional[str] = Field(None, description="Description of the system message")
    
    # Fields for backward compatibility
    message: Optional[str] = Field(None, description="Message content (for backward compatibility)")
    msg_type: Optional[str] = Field(None, description="Message type (for backward compatibility)")
    
    class Config:
        """Pydantic config."""
        
        extra = "allow"
    
    @model_validator(mode='before')
    @classmethod
    def validate_fields(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle field compatibility."""
        if isinstance(data, dict):
            # If legacy fields are used, map them to new fields
            if "message" in data and data.get("message") and not data.get("content"):
                data["content"] = data["message"]
                
            if "msg_type" in data and data.get("msg_type") and not data.get("name"):
                data["name"] = data["msg_type"]
                
            # If new fields are used, map them to legacy fields for backward compatibility
            if "content" in data and data.get("content") and not data.get("message"):
                data["message"] = data["content"]
                
            if "name" in data and data.get("name") and not data.get("msg_type"):
                data["msg_type"] = data["name"]
                
            # Ensure required fields have values
            if not data.get("content") and not data.get("message"):
                raise ValueError("Either 'content' or 'message' must be provided")
                
        return data
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        data = self.model_dump(exclude_none=True)
        
        # Ensure legacy fields are included
        if "content" in data and "message" not in data:
            data["message"] = data["content"]
            
        if "name" in data and "msg_type" not in data:
            data["msg_type"] = data["name"]
            
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SystemMessage':
        """Create from dictionary."""
        return cls.model_validate(data) 