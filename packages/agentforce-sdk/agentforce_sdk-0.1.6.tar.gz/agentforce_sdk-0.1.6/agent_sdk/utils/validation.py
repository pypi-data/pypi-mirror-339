"""Validation functions for AgentForce SDK."""

from typing import Dict, Any, List, Tuple, Optional

def validate_agent(agent_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate an agent configuration.
    
    Args:
        agent_data (dict): Agent configuration data
        
    Returns:
        tuple: (is_valid, error_messages)
    """
    errors = []
    
    # Check required fields
    required_fields = ['agent_api_name', 'AI_Agent_Description']
    field_display_names = {
        'agent_api_name': 'agent_api_name',
        'AI_Agent_Description': 'AI_Agent_Description'
    }
    
    for field in required_fields:
        if field not in agent_data or not agent_data[field]:
            display_name = field_display_names.get(field, field)
            errors.append(f"Missing required field: {display_name}")
    
    # Validate agent_type
    valid_agent_types = ['Internal', 'External']
    if 'agent_type' in agent_data and agent_data['agent_type'] not in valid_agent_types:
        errors.append(f"Invalid agent_type: {agent_data['agent_type']}. Must be one of {valid_agent_types}")
    
    # Validate topics
    if 'items' in agent_data:
        for i, topic in enumerate(agent_data['items']):
            is_valid, topic_errors = validate_topic(topic)
            if not is_valid:
                for error in topic_errors:
                    errors.append(f"Topic {i+1}: {error}")
    
    # Validate variables
    if 'variables' in agent_data:
        for i, variable in enumerate(agent_data['variables']):
            if 'name' not in variable or not variable['name']:
                errors.append(f"Variable {i+1}: Missing required field: name")
            
            if 'dataType' not in variable or not variable['dataType']:
                errors.append(f"Variable {i+1}: Missing required field: dataType")
    
    # Validate systemMessages
    if 'systemMessages' in agent_data:
        for i, message in enumerate(agent_data['systemMessages']):
            if 'message' not in message or not message['message']:
                errors.append(f"System message {i+1}: Missing required field: message")
            
            if 'type' not in message or not message['type']:
                errors.append(f"System message {i+1}: Missing required field: type")
    
    return len(errors) == 0, errors

def validate_topic(topic_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate a topic configuration.
    
    Args:
        topic_data (dict): Topic configuration data
        
    Returns:
        tuple: (is_valid, error_messages)
    """
    errors = []
    
    # Check required fields
    required_fields = ['Topic', 'ClassificationDescription', 'Scope']
    for field in required_fields:
        if field not in topic_data or not topic_data[field]:
            errors.append(f"Missing required field: {field}")
    
    # Validate actions
    if 'Actions' in topic_data:
        for i, action in enumerate(topic_data['Actions']):
            is_valid, action_errors = validate_action(action)
            if not is_valid:
                for error in action_errors:
                    errors.append(f"Action {i+1}: {error}")
    
    return len(errors) == 0, errors

def validate_action(action_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate an action configuration.
    
    Args:
        action_data (dict): Action configuration data
        
    Returns:
        tuple: (is_valid, error_messages)
    """
    errors = []
    
    # Check required fields
    if 'action_name' not in action_data or not action_data['action_name']:
        errors.append("Missing required field: action_name")
    
    # Validate inputs
    if 'inputs' in action_data:
        for i, input_param in enumerate(action_data['inputs']):
            if 'inputName' not in input_param or not input_param['inputName']:
                errors.append(f"Input {i+1}: Missing required field: inputName")
            
            if 'input_description' not in input_param or not input_param['input_description']:
                errors.append(f"Input {i+1}: Missing required field: input_description")
            
            if 'input_dataType' not in input_param or not input_param['input_dataType']:
                errors.append(f"Input {i+1}: Missing required field: input_dataType")
    
    # example_output is optional, but if provided, must be an object
    if 'example_output' in action_data and not isinstance(action_data['example_output'], dict):
        errors.append("example_output must be an object")
    
    return len(errors) == 0, errors 