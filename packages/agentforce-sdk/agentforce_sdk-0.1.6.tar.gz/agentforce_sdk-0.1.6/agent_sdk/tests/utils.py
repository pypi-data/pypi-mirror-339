"""Common utilities for AgentForce SDK tests."""

import os
import json
import tempfile
from typing import Dict, Any

# Sample data for tests
SAMPLE_AGENT_DATA = {
    "name": "TestAgent",
    "description": "Test agent for unit tests",
    "agent_type": "Internal",
    "agent_template_type": "Employee",
    "company_name": "Test Company",
    "domain": "login",
    "sample_utterances": [
        "This is a test utterance",
        "Another test utterance"
    ],
    "variables": [
        {
            "name": "test_variable",
            "data_type": "String",
            "default_value": "test_value",
            "var_type": "custom"
        }
    ],
    "system_messages": [
        {
            "message": "Welcome message for testing",
            "msg_type": "system"
        }
    ],
    "topics": [
        {
            "name": "Test Topic",
            "description": "A topic for testing",
            "scope": "public",
            "instructions": [
                "Test instruction 1",
                "Test instruction 2"
            ],
            "actions": [
                {
                    "name": "testAction",
                    "description": "A test action",
                    "inputs": [
                        {
                            "name": "testInput",
                            "description": "Test input description",
                            "data_type": "String",
                            "required": True
                        }
                    ],
                    "example_output": {
                        "status": "success",
                        "details": {
                            "message": "Test successful"
                        }
                    }
                }
            ]
        }
    ]
}

def create_temp_json_file(data: Dict[str, Any]) -> str:
    """Create a temporary JSON file for testing.
    
    Args:
        data (dict): Data to save in the JSON file
        
    Returns:
        str: Path to the temporary file
    """
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    
    return path 