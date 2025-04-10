"""Input model for agent actions."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Input:
    """Input parameter for an action."""
    name: str
    description: str
    data_type: str
    required: bool = True

    def to_dict(self):
        """Convert the input to a dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "dataType": self.data_type,
            "required": self.required
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Input':
        """Create an Input instance from a dictionary."""
        return cls(
            name=data.get("name", ""),
            description=data.get("description", ""),
            data_type=data.get("dataType", "String"),
            required=data.get("required", True)
        ) 