from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class Output:
    """Represents an output for an action."""
    status: str
    details: Dict[str, Any]
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Output':
        """Create an Output instance from a dictionary."""
        return cls(
            status=data['status'],
            details=data.get('details', {})
        )
    
    def to_dict(self) -> Dict:
        """Convert the Output instance to a dictionary."""
        return {
            'status': self.status,
            'details': self.details
        } 