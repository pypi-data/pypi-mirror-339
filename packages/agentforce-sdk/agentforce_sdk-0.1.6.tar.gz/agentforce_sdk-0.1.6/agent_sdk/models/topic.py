"""Topic models."""
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field

from .action import Action


class Topic(BaseModel):
    """Topic class for categorizing actions in an agent."""
    
    name: str = Field(..., description="Name of the topic")
    description: str = Field("", description="Description of the topic")
    scope: str = Field("", description="Scope of the topic")
    actions: List[Action] = Field(default_factory=list, description="List of actions in the topic")
    instructions: List[str] = Field(default_factory=list, description="Instructions for the topic")
    
    class Config:
        """Pydantic config."""
        
        extra = "allow"
    
    def add_action(self, action: Union[Action, Dict[str, Any]]) -> None:
        """Add an action to the topic."""
        if isinstance(action, Action):
            self.actions.append(action)
        elif isinstance(action, dict):
            self.actions.append(Action.from_dict(action))
        else:
            raise TypeError("action must be an Action instance or dictionary")
    
    def add_instruction(self, instruction: Union[str, List[str]]) -> None:
        """Add one or more instructions to the topic."""
        if isinstance(instruction, str):
            self.instructions.append(instruction)
        elif isinstance(instruction, list):
            self.instructions.extend(instruction)
        else:
            raise TypeError("instruction must be a string or list of strings")
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        data = self.model_dump(exclude_none=True)
        
        # Convert nested actions to dictionaries
        if "actions" in data:
            data["actions"] = [action.to_dict() for action in self.actions]
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Topic':
        """Create from dictionary."""
        # Extract actions to create proper Action objects
        actions_data = data.pop("actions", [])
        topic = cls(**data)
        
        # Add actions
        for action_data in actions_data:
            topic.add_action(action_data)
        
        return topic
    
    def create_action(self, name: str) -> Action:
        """Create and add a new action to the topic."""
        action = Action(name=name, description="")
        self.actions.append(action)
        return action
    
    def remove_action(self, name: str) -> None:
        """Remove an action by name."""
        self.actions = [action for action in self.actions if action.name != name]
    
    def remove_instruction(self, instruction: str) -> None:
        """Remove an instruction from the topic."""
        if instruction in self.instructions:
            self.instructions.remove(instruction)
    
    def get_action(self, name: str) -> Optional['Action']:
        """Get an action by name.
        
        Args:
            name (str): The name of the action to retrieve
            
        Returns:
            Action: The Action instance or None if not found
        """
        for action in self.actions:
            if action.name == name:
                return action
        return None
    
    def save(self) -> None:
        """Save the topic to the agent.
        
        This method is called automatically when modifying topic properties,
        but can be called manually if needed.
        """
        # The topic data is already saved in the agent's data structure,
        # so this method doesn't need to do anything in this implementation.
        pass 