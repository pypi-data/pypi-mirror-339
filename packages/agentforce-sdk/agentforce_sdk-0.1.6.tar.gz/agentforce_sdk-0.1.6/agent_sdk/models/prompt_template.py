"""Models for Salesforce prompt templates."""

from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class PromptInput:
    """A field in a prompt template."""
    name: str
    data_type: str
    description: str
    is_required: bool = False
    salesforce_field: Optional[str] = None
    salesforce_object: Optional[str] = None

@dataclass
class PromptTemplate:
    """A prompt template for Salesforce."""
    name: str
    description: str
    input_fields: List[PromptInput]
    output_fields: List[PromptInput]
    template_text: str
    
    def to_dict(self) -> Dict:
        """Convert the prompt template to a dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "input_fields": [
                {
                    "name": field.name,
                    "data_type": field.data_type,
                    "description": field.description,
                    "is_required": field.is_required,
                    "salesforce_field": field.salesforce_field,
                    "salesforce_object": field.salesforce_object
                }
                for field in self.input_fields
            ],
            "output_fields": [
                {
                    "name": field.name,
                    "data_type": field.data_type,
                    "description": field.description,
                    "is_required": field.is_required,
                    "salesforce_field": field.salesforce_field,
                    "salesforce_object": field.salesforce_object
                }
                for field in self.output_fields
            ],
            "template_text": self.template_text
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PromptTemplate':
        """Create a prompt template from a dictionary."""
        return cls(
            name=data["name"],
            description=data["description"],
            input_fields=[
                PromptInput(
                    name=field["name"],
                    data_type=field["data_type"],
                    description=field["description"],
                    is_required=field.get("is_required", False),
                    salesforce_field=field.get("salesforce_field"),
                    salesforce_object=field.get("salesforce_object")
                )
                for field in data["input_fields"]
            ],
            output_fields=[
                PromptInput(
                    name=field["name"],
                    data_type=field["data_type"],
                    description=field["description"],
                    is_required=field.get("is_required", False),
                    salesforce_field=field.get("salesforce_field"),
                    salesforce_object=field.get("salesforce_object")
                )
                for field in data["output_fields"]
            ],
            template_text=data["template_text"]
        ) 