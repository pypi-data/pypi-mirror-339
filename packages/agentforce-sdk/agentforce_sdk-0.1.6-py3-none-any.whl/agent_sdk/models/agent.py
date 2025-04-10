"""Agent models."""
from typing import Dict, List, Optional, Any, Union, Literal
from pydantic import BaseModel, Field, model_validator

from .topic import Topic
from .variable import Variable
from .system_message import SystemMessage


class Agent(BaseModel):
    """Agent class for managing agent definitions."""
    
    name: str = Field(..., description="Name of the agent")
    description: str = Field("", description="Description of the agent")
    agent_type: Literal["Internal", "External"] = Field("External", description="Type of agent (Internal or External)")
    company_name: Optional[str] = Field(None, description="Company name associated with the agent")
    domain: Optional[str] = Field(None, description="Domain URL associated with the agent")
    sample_utterances: List[str] = Field(default_factory=list, description="Sample utterances for the agent")
    topics: List[Topic] = Field(default_factory=list, description="List of topics in the agent")
    agent_template_type: str = Field("Employee", description="Template type of the agent")
    variables: List[Variable] = Field(default_factory=list, description="List of variables in the agent")
    system_messages: List[SystemMessage] = Field(default_factory=list, description="List of system messages in the agent")
    
    class Config:
        """Pydantic config."""
        
        extra = "allow"
    
    @model_validator(mode='after')
    def validate_agent(self) -> 'Agent':
        """Validate the agent model."""
        if not self.name:
            raise ValueError("Agent name is required")
            
        # Ensure company_name is not None for backward compatibility
        if self.company_name is None:
            self.company_name = ""
            
        return self
    
    def add_topic(self, topic: Union[Topic, Dict[str, Any]]) -> None:
        """Add a topic to the agent."""
        if isinstance(topic, Topic):
            self.topics.append(topic)
        elif isinstance(topic, dict):
            self.topics.append(Topic.from_dict(topic))
        else:
            raise TypeError("topic must be a Topic instance or dictionary")
    
    def add_system_message(self, system_message: Union[SystemMessage, Dict[str, Any]]) -> None:
        """Add a system message to the agent."""
        if isinstance(system_message, SystemMessage):
            self.system_messages.append(system_message)
        elif isinstance(system_message, dict):
            self.system_messages.append(SystemMessage.from_dict(system_message))
        else:
            raise TypeError("system_message must be a SystemMessage instance or dictionary")
    
    def add_variable(self, variable: Union[Variable, Dict[str, Any]]) -> None:
        """Add a variable to the agent."""
        if isinstance(variable, Variable):
            self.variables.append(variable)
        elif isinstance(variable, dict):
            self.variables.append(Variable.from_dict(variable))
        else:
            raise TypeError("variable must be a Variable instance or dictionary")
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        data = self.model_dump(exclude_none=True)
        
        # Convert nested objects to dictionaries
        if "topics" in data:
            data["topics"] = [topic.to_dict() for topic in self.topics]
        
        if "system_messages" in data:
            data["system_messages"] = [sm.to_dict() for sm in self.system_messages]
            
        if "variables" in data:
            data["variables"] = [var.to_dict() for var in self.variables]
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Agent':
        """Create from dictionary."""
        # Extract objects to create proper models
        topics_data = data.pop("topics", [])
        system_messages_data = data.pop("system_messages", [])
        variables_data = data.pop("variables", [])
        
        agent = cls(**data)
        
        # Add topics
        for topic_data in topics_data:
            agent.add_topic(topic_data)
            
        # Add system messages
        for sm_data in system_messages_data:
            agent.add_system_message(sm_data)
            
        # Add variables
        for var_data in variables_data:
            agent.add_variable(var_data)
        
        return agent
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        import json
        return json.dumps(self.to_dict(), indent=2)
    
    def from_json(self, json_str: str) -> 'Agent':
        """Create from JSON string."""
        import json
        data = json.loads(json_str)
        return self.from_dict(data)
    
    def set_name(self, value: str):
        """Set the agent name."""
        self.name = value
    
    def remove_topic(self, name: str) -> None:
        """Remove a topic by name."""
        self.topics = [topic for topic in self.topics if topic.name != name]
    
    def remove_variable(self, name: str) -> None:
        """Remove a variable by name."""
        self.variables = [var for var in self.variables if var.name != name]
    
    def remove_system_message(self, msg_type: str) -> None:
        """Remove system messages by type."""
        self.system_messages = [msg for msg in self.system_messages if msg.msg_type != msg_type]
    
    def save_to_file(self, file_path: str, indent: int = 2) -> None:
        """Save the agent configuration to a JSON file."""
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=indent)
    