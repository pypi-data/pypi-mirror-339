"""Variable models."""
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, model_validator


class Variable(BaseModel):
    """Variable class for agent."""
    
    name: str = Field(..., description="Name of the variable")
    value: Any = Field(None, description="Value of the variable")
    description: Optional[str] = Field(None, description="Description of the variable")
    
    # Fields for backward compatibility
    data_type: Optional[str] = Field(None, description="Data type of the variable (for backward compatibility)")
    default_value: Any = Field(None, description="Default value (for backward compatibility)")
    var_type: str = Field("custom", description="Variable type (for backward compatibility)")
    
    class Config:
        """Pydantic config."""
        
        extra = "allow"
    
    @model_validator(mode='before')
    @classmethod
    def validate_fields(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle field compatibility."""
        if isinstance(data, dict):
            # If legacy fields are used, map them to new fields
            if "default_value" in data and data.get("default_value") is not None and data.get("value") is None:
                data["value"] = data["default_value"]
                
            # If new fields are used, map them to legacy fields for backward compatibility
            if "value" in data and data.get("value") is not None and data.get("default_value") is None:
                data["default_value"] = data["value"]
                
        return data
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        data = self.model_dump(exclude_none=True)
        
        # Ensure legacy fields are included
        if "value" in data and "default_value" not in data:
            data["default_value"] = data["value"]
            
        if "data_type" not in data:
            data["data_type"] = "String"
            
        if "var_type" not in data:
            data["var_type"] = "custom"
            
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Variable':
        """Create from dictionary."""
        return cls.model_validate(data)

    def name(self) -> str:
        """Get the variable's name."""
        return self.name
    
    def name(self, value: str):
        """Set the variable's name."""
        self.name = value
    
    def data_type(self) -> str:
        """Get the variable's data type."""
        return self.value
    
    def data_type(self, value: str):
        """Set the variable's data type."""
        self.value = value
    
    def default_value(self) -> Any:
        """Get the variable's default value."""
        return self.value
    
    def default_value(self, value: Any):
        """Set the variable's default value."""
        self.value = value
    
    def type(self) -> str:
        """Get the variable's type."""
        return self.value
    
    def type(self, value: str):
        """Set the variable's type."""
        self.value = value 